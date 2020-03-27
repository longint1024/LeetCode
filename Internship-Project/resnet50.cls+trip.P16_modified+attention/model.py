import megbrain as mgb
import megskull as mgsk

from megskull.graph import FpropEnv, as_varnode
from megskull.graph.query import GroupNode
from megskull.opr.compatible.caffepool import CaffePooling2D
from megskull.opr.arith import ReLU
from megskull.opr.all import (
    DataProvider, Conv2D, Pooling2D, FullyConnected, BatchedMatMul,
    Softmax, Dropout, BatchNormalization, CrossEntropyLoss,
    ElementwiseAffine, WarpPerspective, WarpPerspectiveWeightProducer,
    WeightDecay, ChanwiseConv2DVanilla, Broadcast, Sqrt, ReLU, ReduceMax, ReduceMin)
from megskull.opr import all as O
from megskull.network import Network
from megskull.opr.netsrc import ParamProvider

import neupeak.model as npk
from neupeak.utils.cli import load_network
from common import config

import numpy as np
import sys
sys.setrecursionlimit(10000)


# {{{ base model

def create_bn_relu(prefix, f_in, ksize, stride, pad, num_outputs,
                   has_bn=True, has_relu=True,
                   conv_name_fun=None, bn_name_fun=None):
    conv_name = prefix
    if conv_name_fun:
        conv_name = conv_name_fun(prefix)

    f = Conv2D(conv_name, f_in, kernel_shape=ksize, stride=stride, padding=pad, output_nr_channel=num_outputs,
               nonlinearity=mgsk.opr.helper.elemwise_trans.Identity())

    if has_bn:
        bn_name = "bn_" + prefix
        if bn_name_fun:
            bn_name = bn_name_fun(prefix)
        f = BatchNormalization(bn_name, f, moving_average_fraction=0.9, data_parallel_all_reduce=True)
        f.eps = 1e-5

        f = ElementwiseAffine(bn_name + "_scaleshift", f, shared_in_channels=False)
        f.get_param_shape("k")

    if has_relu:
        f = ReLU(f)

    return f


def create_bottleneck(prefix, f_in, stride, num_outputs1, num_outputs2, has_proj=False):
    proj = f_in
    if has_proj:
        proj = create_bn_relu(prefix, f_in, ksize=1, stride=stride, pad=0, num_outputs=num_outputs2,
                              has_bn=True, has_relu=False,
                              conv_name_fun=lambda p: "interstellar{}_branch1".format(p),
                              bn_name_fun=lambda p: "bn{}_branch1".format(p))

    f = create_bn_relu(prefix, f_in, ksize=1, stride=stride, pad=0, num_outputs=num_outputs1,
                       has_bn=True, has_relu=True,
                       conv_name_fun=lambda p: "interstellar{}_branch2a".format(p),
                       bn_name_fun=lambda p: "bn{}_branch2a".format(p))

    f = create_bn_relu(prefix, f, ksize=3, stride=1, pad=1, num_outputs=num_outputs1,
                       has_bn=True, has_relu=True,
                       conv_name_fun=lambda p: "interstellar{}_branch2b".format(p),
                       bn_name_fun=lambda p: "bn{}_branch2b".format(p))

    f = create_bn_relu(prefix, f, ksize=1, stride=1, pad=0, num_outputs=num_outputs2,
                       has_bn=True, has_relu=False,
                       conv_name_fun=lambda p: "interstellar{}_branch2c".format(p),
                       bn_name_fun=lambda p: "bn{}_branch2c".format(p))

    f = f + proj

    return ReLU(f)
# f}}}


def create_smooth_label(label, shape, min_value, max_value):
    label = label.astype('int32')
    f = O.zeros(shape) + min_value
    val = O.zeros([shape[0]]) + max_value
    ind = O.Linspace(0, shape[0], shape[0], endpoint=False).astype('int32')
    f = f.set_ai[ind, label](val)
    return f

def create_channel_attention(prefix, f_in):
    batch_size = f_in.shape[0]
    C = f_in.shape[1]
    H = f_in.shape[2]
    W = f_in.shape[3]
    f_R = f_in.reshape(batch_size, C , -1) #directly reshaped to C*HW
    f_psoft = BatchedMatMul(f_R, f_R.dimshuffle(0,2,1))
    f_soft = Softmax(prefix+"softmax", f_psoft, axis=1)
    f_attention = BatchedMatMul(f_soft, f_R)
    f_channel = f_attention.reshape(batch_size, C, H, W)
    a = ParamProvider("attn_weight" + prefix, 0)
    return f_in + a * f_channel

def create_spatial_attention(prefix, f_in):
    batch_size = f_in.shape[0]
    C = f_in.partial_shape[1]
    H = f_in.shape[2]
    W = f_in.shape[3]
    C_output = C // 8
    f_R = f_in.reshape(batch_size, C , -1) #directly reshaped to C*HW
    f_K = Conv2D("Conv1x1_attn_K" + prefix, f_in, kernel_shape=1, output_nr_channel=C_output,
                nonlinearity=mgsk.opr.helper.elemwise_trans.Identity())
    f_Q = Conv2D("Conv1x1_attn_Q" + prefix, f_in, kernel_shape=1, output_nr_channel=C_output,
                nonlinearity=mgsk.opr.helper.elemwise_trans.Identity())
    f_K = f_K.reshape(batch_size, C_output, -1)
    f_Q = f_Q.reshape(batch_size, C_output, -1)
    attn = BatchedMatMul(f_Q.dimshuffle(0, 2, 1), f_K)
    attn_soft = Softmax('Softmax' + prefix, attn, axis=1)
    result = BatchedMatMul(f_R, attn_soft)
    f_spatial = result.reshape(batch_size, C, H, W)
    a = ParamProvider("attn_weight" + prefix, 0)
    return f_in + a * f_spatial

def create_sum_attention(prefix,f_in):
    f = create_channel_attention(prefix+"chan_attn",f_in)+create_spatial_attention(prefix+"spat_attn",f_in)
    return f

def create_triplet_hard_loss(feature, label, margin=0.3):
    feature.oflags.data_parallel_endpoint = True
    label.oflags.data_parallel_endpoint = True

    diff = feature.add_axis(0) - feature.add_axis(1)
    distance = O.Sqrt((diff ** 2).sum(axis=2) + 1e-8)

    mask = O.Equal((label.add_axis(0) - label.add_axis(1)), 0)

    p_matrix = distance * mask
    n_matrix = distance * (1-mask) + O.ZeroGrad(distance.max() * mask)

    dist_ap = O.ReduceMax(p_matrix, axis=1)
    dist_an = O.ReduceMin(n_matrix, axis=1)
    loss = O.ReLU(dist_ap - dist_an + margin).mean()
    return loss, dist_ap, dist_an


def get():
    data = DataProvider("data", shape=config.input_shape,
                        dtype='uint8').astype('float32')
    data = data.reshape(-1, config.nr_channel, *config.image_shape)
    data = data - O.ConstProvider(np.array([123.68, 116.779, 103.939], dtype=np.float32)).reshape(1, 3, 1, 1)

    label = DataProvider("label", shape=(config.minibatch_size, 1), dtype='int32')
    label = O.Broadcast(label, (label.shape[0], config.K)).reshape(-1)

    f = create_bn_relu("conv1", data, ksize=7, stride=2, pad=3, num_outputs=64)
    f = CaffePooling2D("pool1", f, window=3, stride=2, padding=0, mode="MAX")

    pre = [2, 3, 4, 5]
    stages = [3, 4, 6, 3]
    mid_outputs = [64, 128, 256, 512]
    enable_stride = [False, True, True, False]
    for p, s, o, es in zip(pre, stages, mid_outputs, enable_stride):
        for i in range(s):
            prefix = "{}{}".format(p, chr(ord("a") + i))
            stride = 1 if not es or i > 0 else 2
            has_proj = False if i > 0 else True
            f = create_bottleneck(prefix, f, stride, o, o * 4, has_proj)
            print("{}\t{}".format(prefix, f.partial_shape))
        if (p == 4):
            f = create_sum_attention(prefix, f)

    resnet_out = f
    feature = O.cblk.global_pooling(resnet_out, mode='MAX')
    feature = BatchNormalization('bn1', feature, moving_average_fraction=0.9, data_parallel_all_reduce=True)
    cls = FullyConnected('cls-ful', feature,
                         output_dim=config.nr_class,
                         nonlinearity=mgsk.opr.helper.elemwise_trans.Identity())
    softmax = Softmax('softmax', cls)

    loss_tri_l2, pos_l2, neg_l2 = create_triplet_hard_loss(feature, label)

    losses = dict()
    losses['loss_xent'] = CrossEntropyLoss(softmax, label)
    losses['loss_tri'] = loss_tri_l2
    loss_wowd = sum(losses.values())
    npk.utils.hint_loss_subgraph(list(losses.values()), loss_wowd)

    with GroupNode('weight_decay').context_reg():
        loss_wwd = O.WeightDecay(
            loss_wowd, {'conv*:W': 1e-5, 'interstellar*:W': 1e-5, '*_scaleshift:k': 1e-5})
    loss_weight_decay = loss_wwd - loss_wowd
    loss_weight_decay.vflags.data_parallel_reduce_method = 'sum'
    losses['loss_weight_decay'] = loss_weight_decay
    loss = loss_wwd

    net = Network(outputs=[feature], loss=loss)
    extra_outputs = losses.copy()
    extra_outputs.update(
        misclassify=O.cblk.misclassify(softmax, label),
        l2_po=pos_l2.mean(),
        l2_ne=neg_l2.mean(),
    )
    net.extra['extra_outputs'] = extra_outputs
    net.extra['extra_config'] = {
        'monitor_vars': sorted(extra_outputs.keys()),
    }
    param_network = load_network(
        's3://yht-share/base-model/resnet50_new_brain/resnet50_new.brainmodel'
    )
    npk.param_init.set_opr_states_from_network(
        net.loss_visitor.all_oprs,
        param_network
    )
    return net

# vim: foldmethod=marker

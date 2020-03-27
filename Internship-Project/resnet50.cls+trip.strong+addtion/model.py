import megbrain as mgb
import megskull as mgsk

from megskull.graph import FpropEnv, as_varnode
from megskull.graph.query import GroupNode
from megskull.opr import all as O
from megskull.network import Network

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

    f = O.Conv2D(conv_name, f_in, kernel_shape=ksize, stride=stride, padding=pad, output_nr_channel=num_outputs,
            nonlinearity=mgsk.opr.helper.elemwise_trans.Identity())

    if has_bn:
        bn_name = "bn_" + prefix
        if bn_name_fun:
            bn_name = bn_name_fun(prefix)
        f = O.BatchNormalization(bn_name, f, moving_average_fraction=0.9, eps_mode='ADDITIVE', data_parallel_all_reduce=True)

        f = O.ElementwiseAffine(bn_name + "_scaleshift", f, shared_in_channels=False)
        f.get_param_shape("k")

    if has_relu:
        f = O.ReLU(f)

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

    return O.ReLU(f)
# }}}


# <3> Label Smoothing
def create_smooth_label(label, shape, min_value, max_value):
    label = label.astype('int32')
    f = O.zeros(shape) + min_value
    val = O.zeros([shape[0]]) + max_value
    ind = O.Linspace(0, shape[0], shape[0], endpoint=False).astype('int32')
    f = f.set_ai[ind, label](val)
    return f


def create_triplet_hard_loss(feature, label, margin=0.3):
    feature.oflags.data_parallel_endpoint = True
    label.oflags.data_parallel_endpoint = True

    diff = feature.add_axis(0) - feature.add_axis(1)
    distance = O.Sqrt((diff ** 2).sum(axis=2) + 1e-8)

    assert label.partial_shape.ndim == 1
    mask = O.Equal((label.add_axis(0) - label.add_axis(1)), 0)

    p_matrix = distance * mask
    n_matrix = distance * (1-mask) + O.ZeroGrad(distance.max() * mask)

    dist_ap = O.ReduceMax(p_matrix, axis=1)
    dist_an = O.ReduceMin(n_matrix, axis=1)
    loss = O.ReLU(dist_ap - dist_an + margin).mean()
    return loss, dist_ap, dist_an


# <6> Center Loss
def create_center_loss(feature, label, center_lr, nr_class=config.nr_class):
    center_param = O.ParamProvider('center', np.zeros((nr_class, feature.partial_shape[-1]), dtype=np.float32))
    center_param.freezed = True
    center = O.ZeroGrad(center_param).ai[label, :]
    loss = (0.5 * ((feature - center) ** 2).sum(axis=1)).mean()

    batch_size = feature.shape[0]
    cnt = O.zeros(nr_class, dtype='int32').incr_ai[label](O.ones(batch_size, dtype='int32'))
    diff = O.zeros(nr_class, feature.partial_shape[-1]).incr_ai[label, :](center-feature)
    diff = diff / (cnt + 1.).add_axis(1)
    update_center_opr = O.AddUpdate(center_param, -diff, alpha=1, beta=center_lr)
    loss = O.ExtraDependency([loss, update_center_opr])
    return loss

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

def create_conv(prefix,f_in):
    f = create_bn_relu(prefix+'conv1',f_in,3,1,1,512)
    f = create_bn_relu(prefix+'conv2',f,1,1,1,2048)
    return f

def get():
    data = O.DataProvider("data", shape=config.input_shape,
                        dtype='uint8').astype('float32')
    data = data.reshape(-1, config.nr_channel, *config.image_shape)
    data = data - O.ConstProvider(np.array([123.68, 116.779, 103.939], dtype=np.float32)).reshape(1,3,1,1)

    label = O.DataProvider("label", shape=(
        config.minibatch_size, 1), dtype='int32')
    label = O.Broadcast(label, (label.shape[0], config.K)).reshape(-1)

    f = create_bn_relu("conv1", data, ksize=7, stride=2, pad=3, num_outputs=64)
    f = O.CaffePooling2D("pool1", f, window=3, stride=2, padding=0, mode="MAX")

    pre = [2, 3, 4, 5]
    stages = [3, 4, 6, 3]
    mid_outputs = [64, 128, 256, 512]
    # <4> Last Stride
    enable_stride = [False, True, True, False]
    for p, s, o, es in zip(pre, stages, mid_outputs, enable_stride):
        for i in range(s):
            prefix = "{}{}".format(p, chr(ord("a") + i))
            stride = 1 if not es or i > 0 else 2
            has_proj = False if i > 0 else True
            f = create_bottleneck(prefix, f, stride, o, o * 4, has_proj)
            print("{}\t{}".format(prefix, f.partial_shape))
        if (p==4):
            #f=create_sum_attention(prefix , f)
            f_add = f

    resnet_out = f
    feat = O.cblk.global_pooling(resnet_out, mode='MAX')
    f_add_conv = create_conv('addtion',f_add)
    f_add3 = O.cblk.global_pooling(f_add_conv, mode='MAX')
    feat = f_add3 + feat
    # <5> BNNeck
    feat_bn = O.BatchNormalization('neck', feat, eps_mode='ADDITIVE', data_parallel_all_reduce=True, moving_average_fraction=0.9)
    feat_bn = O.ElementwiseAffine("neck_scaleshift", feat_bn, shared_in_channels=False)
    feat_bn.param_manager['b'] = O.zeros(feat_bn.partial_shape[-1])

    cls = O.FullyConnected('cls-fc', feat_bn,
                         output_dim=config.nr_class,
                         nonlinearity=mgsk.opr.helper.elemwise_trans.Identity())
    cls.param_manager['b'] = O.zeros(config.nr_class)
    softmax = O.Softmax('softmax', cls)

    for x in [softmax, feat, feat_bn, label]:
        x.oflags.data_parallel_endpoint = True

    losses = dict()
    smooth_label = create_smooth_label(label, softmax.shape, 0.1 / config.nr_class, 0.9 + 0.1/config.nr_class)
    losses['loss_xent'] = O.CrossEntropyLoss(softmax, smooth_label, label_is_class_number=False)
    loss_tri_l2, pos_l2, neg_l2 = create_triplet_hard_loss(feat, label)
    losses['loss_tri'] = loss_tri_l2
    # center loss
    center_loss = create_center_loss(feat, label, center_lr=0.5)
    losses['loss_center'] = center_loss * 1e-3
    loss_wowd = sum(losses.values())
    npk.utils.hint_loss_subgraph(list(losses.values()), loss_wowd)

    with GroupNode('weight_decay').context_reg():
        loss_wwd = O.WeightDecay(loss_wowd, {'*':1e-3})
    loss_weight_decay = loss_wwd - loss_wowd
    loss_weight_decay.vflags.data_parallel_reduce_method = 'sum'
    losses['loss_weight_decay'] = loss_weight_decay
    loss = loss_wwd

    net = Network(outputs=[feat_bn], loss=loss)
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

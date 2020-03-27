from neupeak.utils.misc import stable_rng
from neupeak.utils import imgproc
from neupeak.dataset2 import BaseDataset

from meghair.utils import logconf, io
from meghair.utils.imgproc import imdecode
from meghair.utils.misc import ic01_to_i01c, i01c_to_ic01, list2nparray
import random

import cv2
import numpy as np
import pickle
import nori2 as nori
from tqdm import tqdm

from common import config

logger = logconf.get_logger(__name__)


# f{{{ augment
def augment(img, rng, do_training):
    if not do_training:
        size = (config.image_shape[1], config.image_shape[0])
        img = cv2.resize(img, size, interpolation=cv2.INTER_LINEAR)
    else:
        def random_crop(img, target_shape):
            h, w = img.shape[:2]
            th, tw = target_shape
            i = rng.randint(0, h - th)
            j = rng.randint(0, w - tw)
            return img[i:i+th, j:j+tw,:]

        def grayscale(img):
            w = list2nparray([0.114, 0.587, 0.299]).reshape(1, 1, 3)
            gs = np.zeros(img.shape[:2])
            gs = (img * w).sum(axis=2, keepdims=True)

            return gs

        def brightness_aug(img, val):
            alpha = 1. + val * (rng.rand() * 2 - 1)
            img = img * alpha

            return img

        def contrast_aug(img, val):
            gs = grayscale(img)
            gs[:] = gs.mean()
            alpha = 1. + val * (rng.rand() * 2 - 1)
            img = img * alpha + gs * (1 - alpha)

            return img

        def saturation_aug(img, val):
            gs = grayscale(img)
            alpha = 1. + val * (rng.rand() * 2 - 1)
            img = img * alpha + gs * (1 - alpha)

            return img

        def color_jitter(img, brightness, contrast, saturation):
            augs = [(brightness_aug, brightness),
                    (contrast_aug, contrast),
                    (saturation_aug, saturation)]
            random.shuffle(augs)

            for aug, val in augs:
                img = aug(img, val)

            return img

        def lighting(img, std):
            eigval = list2nparray([0.2175, 0.0188, 0.0045])
            eigvec = list2nparray([
                [-0.5836, -0.6948,  0.4203],
                [-0.5808, -0.0045, -0.8140],
                [-0.5675, 0.7192, 0.4009],
            ])
            if std == 0:
                return img

            alpha = rng.randn(3) * std
            bgr = eigvec * alpha.reshape(1, 3) * eigval.reshape(1, 3)
            bgr = bgr.sum(axis=1).reshape(1, 1, 3)
            img = img + bgr

            return img

        def horizontal_flip(img, prob):
            if rng.rand() < prob:
                return img[:, ::-1]
            return img

        img = cv2.resize(img, config.image_shape[::-1])
        img = horizontal_flip(img, 0.5)
        img = imgproc.pad_image_to_shape(img, (config.image_shape[0] + 20, config.image_shape[1] + 20))
        img = random_crop(img, config.image_shape)

        #img = color_jitter(img, brightness=0.4, contrast=0.4, saturation=0.4)
        #img = lighting(img, 0.1)
        #img = brightness_aug(img, 0.1)

    img = np.minimum(255, np.maximum(0, img))
    return img
# f}}}


class Dataset(BaseDataset):

    def __init__(self, dataset_name):
        super().__init__(dataset_name)
        self.minibatch_size = config.minibatch_size
        self.fragment_size = self.minibatch_size
        self.dataset_name = dataset_name
        self.dataset_path = config.dataset
        self.metas = []
        persons = io.load(self.dataset_path)
        self.instance_per_epoch = sum(len(v)//config.K for v in persons.values())

    def load(self):
        persons = io.load(self.dataset_path)
        keys = sorted(persons.keys())
        if self.dataset_name == 'train':
            self.metas = [persons[k] for k in keys]
        else:
            self.metas = [persons[k][-1:] for k in keys]
        return self

    def instance_generator(self, encoded=False):
        rng = self.rng
        nf = nori.Fetcher()
        do_training = (self.dataset_name == 'train')
        idxs = np.arange(len(self.metas))

        while True:
            rng.shuffle(idxs)
            for idx in idxs:
                meta = self.metas[idx]
                meta = [meta[x] for x in rng.choice(
                    np.arange(len(meta)), config.K, replace=(len(meta) < config.K))]

                def get_img(info):
                    img = nf.get(info[0])
                    img = imdecode(img)
                    if len(info) > 4:
                        img = img[info[1]:info[2], info[3]:info[4], :]
                    return img

                imgs = [get_img(x) for x in meta]
                imgs = [augment(x, rng, do_training) for x in imgs]
                imgs = [x.transpose(2, 0, 1)[np.newaxis] for x in imgs]
                imgs = np.concatenate(imgs)
                yield {
                    'data': imgs.astype('uint8'),
                    'label': np.array([idx], dtype='int32'),
                }

    @property
    def servable_name(self):
        dataset_dep_files = [
            config.real_path(f) for f in
            ['common.py', 'dataset.py']
        ]

        return config.make_servable_name(
            self.dataset_name, dataset_dep_files,
        )

# vim: foldmethod=marker

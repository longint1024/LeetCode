import os
import hashlib
import getpass
from neupeak.utils import get_caller_base_dir, get_default_log_dir, get_oss_model_dir


class Config:
    base_dir = get_caller_base_dir()
    log_dir = get_default_log_dir(base_dir)
    '''where to write all the logging information during training
    (includes saved models)'''
    log_model_dir = os.path.join(log_dir, 'models')
    oss_model_dir = get_oss_model_dir(base_dir)
    '''where to write model snapshots to'''
    log_file = os.path.join(log_dir, 'log.txt')
    exp_name = os.path.basename(log_dir)
    '''name of this experiment'''

    K = 4
    P = 32
    minibatch_size = P
    nr_channel = 3
    image_shape = (256, 128) # H, W

    dataset = 's3://reidData/meta/market_train_751.pkl'
    nr_class = 751
    nr_epoch = 120
    task_type = 'classification'

    @property
    def input_shape(self):
        # N, K, C, H, W
        return (self.minibatch_size, self.K, self.nr_channel) + (self.image_shape[0], self.image_shape[1])

    def real_path(self, path):
        ''':return: path relative to base_dir'''
        return os.path.join(self.base_dir, path)

    def make_servable_name(self, dataset_name, dep_files):
        '''make a unique servable name.
        .. note::
            The resulting servable name is composed by the content of
            dependency files and the original dataset_name given.
        :param dataset_name: an dataset identifier, usually the argument
            passed to dataset.py:get
        :type dataset_name: str
        :param dep_files: files that the constrution of the dataset depends on.
        :type dep_files: list of str
        '''

        def _md5(s):
            m = hashlib.md5()
            for _s in s:
                m.update(_s)
                m.update(m.digest())
            return m.hexdigest()

        parts = []
        for path in dep_files:
            with open(path, 'rb') as f:
                parts.append(f.read())
        return ('neupeak:' + getpass.getuser() + ':' + _md5(parts) + '.' + dataset_name)


config = Config()

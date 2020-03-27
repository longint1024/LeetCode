#!/usr/bin/env mdl
import os
import sys
import time
import magic
import argparse
from setproctitle import setproctitle

import model
import dataset as dataset_desc
import numpy as np
from common import config

import megbrain as mgb
import megskull
from megskull.utils import logconf
from meghair.utils import io
from meghair.utils.misc import ensure_dir

from neupeak.train.utils import TrainClock
from neupeak.utils.inference import get_fprop_env, FunctionMaker
from neupeak.train.logger.tensorboard_logger import TensorBoardLogger
from neupeak.train.logger.worklog_logger import WorklogLogger, log_rate_limited
from neupeak.utils.fs import change_dir, make_symlink_if_not_exists
from meghair.train.interaction import parse_devices
from neupeak.dataset2 import RemoteDataset, EpochDataset


logger = logconf.get_logger(__name__)


def get_learning_rate(clock: TrainClock):
    if clock.epoch < 20:
        lr = 3.0e-6+(3.5e-4-3.0e-6)/20*clock.epoch
    elif clock.epoch < 80:
        lr = 3.5e-4
    elif clock.epoch < 130:
        lr = 3.5e-5
    elif clock.epoch < 150:
        lr = 3.5e-6
    return lr


class Session:

    def __init__(self, config, devices, net=None, train_func=None):
        setproctitle(config.exp_name)

        # log dirs
        with change_dir(config.base_dir):
            make_symlink_if_not_exists(
                os.path.relpath(config.log_dir, config.base_dir),
                os.path.join(config.base_dir, 'train_log'),
                overwrite=True,
            )
        self.log_dir = config.log_dir
        ensure_dir(self.log_dir)
        logconf.set_output_file(os.path.join(self.log_dir, 'log.txt'))
        self.model_dir = config.log_model_dir
        ensure_dir(self.model_dir)

        self.net = net
        self.train_func = train_func
        self.clock = TrainClock()
        self.tb_loggers = []
        self.oss_model_dir = config.oss_model_dir

        self._func_maker = FunctionMaker.get_instance(devices=devices)
        logger.info(
            'using devices {}'.format(', '.join(self._func_maker.devices))
        )

    def make_func(self, train_state=False, fast_run=True, **kwargs):
        # Fprop: https://sharefs.svc.brainpp.cn/_brain/document/megdl/html/tutorial/megskull_tutorial.html#Fproping
        # FastRun: https://sharefs.svc.brainpp.cn/_brain/document/megdl/html/tutorial/misc_example.html#Fast-run-Mode
        if train_state:
            assert 'loss_var' in kwargs
            env = get_fprop_env(fast_run=fast_run, train_state=True)
            env.flags.train_exponential_moving_average = True
            self.train_func = self._func_maker.make_func(
                optimizable=True,
                env=env,
                **kwargs,
            )
            return self.train_func

        return self._func_maker.make_func(env=get_fprop_env(fast_run=fast_run))

    def tensorboards(self, *names):
        self.tb_loggers = [
            TensorBoardLogger(os.path.join(self.log_dir, d)) for d in names
        ]
        return self.tb_loggers

    def start(self):
        self.save_checkpoint('start')
        for b in self.tb_loggers:
            b.put_start(self.clock.step)

    def get_datasets(self, *dataset_names, use_local=False):
        datasets = {
            name: dataset_desc.Dataset(name)
            for name in dataset_names
        }
        if use_local:
            logger.info('use local dataset')
        else:
            # we use remote dataset by default
            logger.info('use remote dataset')
            datasets = {
                name: RemoteDataset(ds) for name, ds in datasets.items()
            }

        return {
            name: EpochDataset(ds.load()) for name, ds in datasets.items()
        }

    def monitor_param_histogram(self, histogram_logger, rms_logger, interval=200):
        # Watch var and grad rms
        def get_var_watcher(key, interval, clock):
            def cb(gpu_tensor):
                nonlocal interval, clock, histogram_logger, rms_logger
                if clock.step % interval == 0:
                    var_value = gpu_tensor.get_value()
                    histogram_logger.put_tensor_as_histogram(
                        key, var_value, clock.step)
                if clock.minibatch == 0:
                    var_value = gpu_tensor.get_value()
                    rms_logger.put_tensor_rms(key, var_value, clock.step)

            return mgb.callback_lazycopy(cb)

        loss_mgbvar = self.train_func.loss_mgbvar
        for param in self.net.loss_visitor.all_params:
            if param.freezed:
                continue
            name = param.name.replace(':', '/')  # tensorflow name convention
            param_var = self.train_func.get_mgbvar(param)
            grad_var = mgb.grad(loss_mgbvar, param_var)
            self.train_func.add_extra_outspec(
                (param_var, get_var_watcher(name, interval, self.clock))
            )
            self.train_func.add_extra_outspec(
                (grad_var, get_var_watcher(name+'/grad', interval, self.clock))
            )

    def save_checkpoint(self, name):
        # save network param, optimizer state and clock in a single checkpoint
        # checkpoint can be save in sharefs or oss
        ckp = {
            'network': self.net,
            'opt_state': self.train_func.optimizer_state.make_checkpoint(),
            'clock': self.clock.make_checkpoint(),
        }

        if self.oss_model_dir:
            ckp_path = os.path.join(self.oss_model_dir, name)
            # make a text file contains the oss path
            with open(os.path.join(self.model_dir, name), 'w') as f:
                f.write(ckp_path)
        else:
            ckp_path = os.path.join(self.model_dir, name)

        io.dump(ckp, ckp_path)

    def load_checkpoint(self, ckp_path):
        if ckp_path.startswith('s3://'):
            checkpoint = io.load(ckp_path, dict)
        ckp_path = os.path.realpath(ckp_path)

        # text file contains an oss path
        mf = magic.from_file(ckp_path, mime=True)
        mf = mf.decode('utf-8') if isinstance(mf, bytes) else mf
        if mf.startswith('text'):
            with open(ckp_path) as f:
                ckp_path = f.read().strip()

        checkpoint = io.load(ckp_path, dict)
        # restore network param, optimizer state and clock
        self.net.loss_visitor.set_all_stateful_opr_from(checkpoint['network'].loss_visitor)
        self.train_func.optimizer_state.restore_checkpoint(checkpoint['opt_state'])
        self.clock.restore_checkpoint(checkpoint['clock'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', default='*')
    parser.add_argument('--fast-run', action='store_true', default=False)
    parser.add_argument('--local', action='store_true', default=False)
    parser.add_argument('-c', '--continue', '--try-continue',
                        dest='continue_path', required=False)
    args = parser.parse_args()

    mgb.config.set_default_device(parse_devices(args.device)[0])
    net = model.get()

    # create session
    sess = Session(config, args.device, net=net)

    # The loggers
    worklog = WorklogLogger(os.path.join(sess.log_dir, 'worklog.txt'))
    # create tensorboard loggers
    train_tb, val_tb = sess.tensorboards("train.events", "val.events")

    # The training and validation functions
    train_func = sess.make_func(
        loss_var=net.loss_var, fast_run=args.fast_run, train_state=True
    )
    val_func = sess.make_func(
        # you might wanna disable fast_run for validation
        fast_run=args.fast_run, train_state=False
    )

    opt = megskull.optimizer.AdamV8(learning_rate=10)
    #opt = megskull.optimizer.Momentum(learning_rate=10, momentum=0.9)
    opt(train_func)

    # The datasets
    datasets = sess.get_datasets("train", "validation", use_local=args.local)
    # type: EpochDataset, EpochDataset
    train_ds, val_ds = datasets['train'], datasets['validation']
    val_ds_iter = iter(val_ds.minibatch_generator())

    # vars to monitor
    sess.monitor_param_histogram(train_tb, worklog, interval=40)
    monitor_vars = list(
        net.extra
        .get("extra_config", {})
        .get('monitor_vars', [])
    )
    outspec = {'loss': net.loss_var}
    outspec.update(net.extra.get("extra_outputs", {}))

    # after done all decorations, compile the function
    train_func.compile(outspec)
    val_func.compile(outspec)

    # restore checkpoint
    if args.continue_path and os.path.exists(args.continue_path):
        sess.load_checkpoint(args.continue_path)

    # Now start train
    clock = sess.clock
    sess.start()

    if not args.continue_path:
        train_tb.put_graph(net)

    log_output = log_rate_limited(min_interval=0.5)(worklog.put_line)

    for epoch in train_ds.epoch_generator():
        if clock.epoch >= config.nr_epoch:
            break
        time_epoch_start = tstart = time.time()

        lr = get_learning_rate(clock)
        opt.learning_rate = lr
        train_tb.put_scalar('learning_rate', lr, clock.step)

        for minibatch in epoch:
            tdata = time.time() - tstart

            out = train_func(**minibatch)
            cur_time = time.time()
            ttrain = cur_time - tstart
            time_passed = cur_time - time_epoch_start

            time_expected = time_passed / \
                (clock.minibatch + 1) * train_ds.minibatch_per_epoch
            eta = time_expected - time_passed

            outputs = [
                "e:{},{}/{}".format(clock.epoch, clock.minibatch,
                                    train_ds.minibatch_per_epoch),
                "{:.2g} mb/s".format(1./ttrain),
            ] + [
                'passed:{:.2f}'.format(time_passed),
                'eta:{:.2f}'.format(eta),
            ] + [
                "{}:{:.2g}".format(k, float(out[k])) for k in monitor_vars
            ]
            if tdata/ttrain > .05:
                outputs += ["dp/tot: {:.2g}".format(tdata/ttrain)]
            log_output(' '.join(outputs))

            for k, v in out.items():
                if k in monitor_vars:
                    train_tb.put_scalar(k, v, clock.step)

            if clock.minibatch % 100 == 0:
                vb = next(val_ds_iter)
                val_out = val_func(**vb)
                val_monitor_vars = [
                    (k, float(v)) for k, v in val_out.items()
                    if k in monitor_vars
                ]
                for k, v in val_monitor_vars:
                    val_tb.put_scalar(k, v, clock.step)

                log_output(
                    "Val: " +
                    " ".join([
                        "{}={:.2g}".format(k, v) for k, v in val_monitor_vars
                    ])
                )

            if clock.step % 100 == 0:
                train_tb.flush()
                val_tb.flush()

            clock.tick()
            tstart = time.time()

        train_tb.flush()
        val_tb.flush()

        clock.tock()

        if clock.epoch % 50 == 0 or clock.epoch == config.nr_epoch:
            sess.save_checkpoint('epoch-{}'.format(clock.epoch))
        sess.save_checkpoint('latest')

    logger.info("Training is done, exit.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt, exit.")
        sys.exit(1)

# vim: ts=4 sw=4 sts=4 expandtab

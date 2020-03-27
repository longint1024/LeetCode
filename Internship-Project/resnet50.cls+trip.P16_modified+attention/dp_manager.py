#!/usr/bin/env mdl
import os
import time
import traceback
from threading import Thread, Event

import rrun
import tabulate
from influxdb import InfluxDBClient
from meghair.utils import logconf
from meghair.utils.misc import ensure_dir
from neupeak.utils.fs import change_dir, make_symlink_if_not_exists

from dataset import Dataset
from common import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
influxdb = InfluxDBClient(host="dpflow-influxdb.i.brainpp.cn")
rrun_client = rrun.Client()
logger = logconf.get_logger(__name__)


class DPManager:
    jobs_per_worker = 4
    RRUN_STATE = dict(rrun.Runner.State.items())
    RRUN_STATE_NAME = {k: v for v, k in RRUN_STATE.items()}
    DEAD_STATE = [RRUN_STATE['KILLED'],
                  RRUN_STATE['FAILED'], RRUN_STATE['COMPLETED']]

    def __init__(self, dataset_name='train', jobs=4):
        ensure_dir(os.path.join(config.log_dir, 'serve_log'))
        self.dataset_name = dataset_name
        self.pipe_name = Dataset(dataset_name).servable_name
        self.max_jobs = jobs
        self._control_interval = 30
        self._decrease_cnt = 0
        self._stop = Event()
        self._thread = Thread(target=self._control_loop)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kill()
        self.stop()

    def gen_rrun_spec(self):
        spec = rrun.RunnerSpec()
        rrun.fill_runner_spec(spec, environments=True, uid_gid=True, share_dirs=True, work_dir=True)
        spec.name = '{}/datasets/{}'.format(os.path.basename(BASE_DIR), self.dataset_name)
        spec.labels['experiment'] = os.path.basename(BASE_DIR)
        spec.labels['usage'] = "datasets"
        spec.labels['dataset_name'] = self.dataset_name
        spec.labels['pipe_name'] = self.pipe_name

        spec.environments["OMP_NUM_THREADS"] = "1"
        spec.log_dir = os.path.join(config.log_dir, 'serve_log')
        spec.scheduling_hint.group = 'users'
        spec.preemptible = True
        spec.resources.cpu = self.jobs_per_worker
        spec.resources.memory_in_mb = 2 * self.jobs_per_worker * 1024
        spec.scheduling_hint.negative_tags[:] = ['gpu']
        spec.max_wait_time = 3600 * int(1e9)
        spec.commands[:] = ['bash', '-c', 'mdl {} serve --{} {}'.format(
            os.path.join(BASE_DIR, 'dstool.py'),
            self.dataset_name, self.jobs_per_worker)]
        return spec

    def get_rrun_status(self):
        request = rrun.ListRunnersRequest()
        request.labels['usage'] = "datasets"
        request.labels['pipe_name'] = self.pipe_name
        response = rrun_client.list_runners(request)
        return [x for x in response.runners if x.state not in self.DEAD_STATE]

    def get_dpflow_statistic(self):
        query = 'SELECT * FROM "diagnostic" WHERE "name"=\'{}\' AND time>now()-1m ORDER BY time DESC LIMIT 40000'.format(self.pipe_name)
        result = influxdb.query(query, database='dpflow')
        result = list(result.get_points())

        from datetime import datetime, timedelta
        from dateutil.parser import parse
        # ignore dead pipe
        result = [x for x in result if datetime.now() - parse(x['time'], ignoretz=True) > timedelta(seconds=60)]
        result = list({x['pipe_id']: x for x in result}.values())
        ins, outs = [x for x in result if x['direction'] == 'IN'], [x for x in result if x['direction'] == 'OUT']
        blocking_in, blocking_out = [x for x in ins if x['used_buffer'] > 0.99], [x for x in outs if x['used_buffer'] > 0.99]
        statistic = {
            'nr_in': len(ins),
            'nr_out': len(outs),
            'nr_blocking_in': len(blocking_in),
            'nr_blocking_out': len(blocking_out),
        }
        if len(ins):
            statistic['in_avg_buf'] = sum([x['used_buffer'] for x in ins]) / len(ins)
            statistic['in_min_buf'] = min([x['used_buffer'] for x in ins])
        if len(outs):
            statistic['out_avg_buf'] = sum([x['used_buffer'] for x in outs]) / len(outs)
        return statistic

    def increase(self):
        runners = self.get_rrun_status()
        if len(runners) * self.jobs_per_worker < self.max_jobs:
            spec = self.gen_rrun_spec()
            response = rrun_client.start_runner(rrun.StartRunnerRequest(spec=spec))
            logger.info('[+] {} start runner {}'.format(self.dataset_name, response.id))

    def decrease(self):
        self._decrease_cnt += 1
        runners = self.get_rrun_status()
        if len(runners) > 4 and self._decrease_cnt > 180. / self._control_interval:
            kill_id = runners[-1].id
            response = rrun_client.kill_runner(rrun.KillRunnerRequest(id=kill_id))
            logger.info('[-] {} kill runner {}'.format(self.dataset_name, kill_id))
            self._decrease_cnt = 0

    def kill(self):
        runners = self.get_rrun_status()
        for runner in runners:
            kill_id = runner.id
            response = rrun_client.kill_runner(rrun.KillRunnerRequest(id=kill_id))
            logger.info('[-] {} kill runner {}'.format(self.dataset_name, kill_id))

    def _control_loop(self):
        while not self._stop.is_set():
            try:
                statistic = self.get_dpflow_statistic()
                logger.info("{}\n".format(self.dataset_name) + tabulate.tabulate({k: [v] for k, v in statistic.items()}, headers="keys"))
                if statistic['nr_in'] == 0:
                    logger.info('there is no input_pipe')
                    #self.kill()
                elif statistic['nr_blocking_in'] == 0 and statistic['in_min_buf'] < 0.1:
                    self.increase()
                elif statistic['nr_blocking_out'] >= 2 * self.jobs_per_worker:
                    self.decrease()
                self._stop.wait(self._control_interval)
            except Exception as e:
                logger.error(e)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=int, default=80)
    parser.add_argument('--validation', type=int, default=8)
    args = parser.parse_args()

    with DPManager('train', args.train), DPManager('validation', args.validation):
        input("running ....")


# vim: ft=python ts=4 sts=4 sw=4 expandtab

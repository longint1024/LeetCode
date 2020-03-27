#!/usr/bin/env mdl
from dataset import Dataset
from common import config


def test(args):
    ds = Dataset('train').load()
    batch = next(ds.batch_generator(batch_size=4, encoded=False))
    batch = ds.decode(batch)
    for k, v in batch.items():
        print(k, v.shape)


def serve(args):
    import time
    import multiprocessing
    from meghair.utils.misc import add_rand_seed_entropy
    from neupeak.dataset2.utils import serve_dataset, generate_seed

    seed = generate_seed()
    add_rand_seed_entropy(seed)

    def my_serve_dataset(ds: Dataset, worker_id: int):
        return serve_dataset(ds, worker_id, ds.servable_name, encoded=False)

    settings = []
    if args.train:
        settings.append((Dataset('train').load(), args.train))
    if args.validation:
        settings.append((Dataset('validation').load(), args.validation))

    workers = [
        multiprocessing.Process(
            target=my_serve_dataset,
            args=(ds, worker_id, )
        )
        for ds, count in settings
        for worker_id in range(count)
    ]
    for w in workers:
        w.daemon = True
        w.start()

    while True:
        for w in workers:
            if not w.is_alive():
                raise RuntimeError("One of the workers died unexpectedly")
        time.sleep(10)


def webview(args):
    from neupeak.dataset2.utils import webview_dataset
    ds = Dataset(args.dataset).load()

    webview_dataset(
        ds, name=config.exp_name, batch_size=args.batch_size, port=args.port,
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    p = subparsers.add_parser('test')
    p.set_defaults(func=test)

    p = subparsers.add_parser('view')
    p.set_defaults(func=webview)
    p.add_argument('--dataset', default="train", help="dataset name (default: %(default)s)")
    p.add_argument('--port', type=int, default=12345, help="port number to serve web view (default: %(default)d)")
    p.add_argument('--batch-size', type=int, default=config.minibatch_size, help="batch size (default: %(default)d)")

    p = subparsers.add_parser('serve')
    p.set_defaults(func=serve)
    p.add_argument('--train', type=int, default=0, help="number of providers for training")
    p.add_argument('--validation', type=int, default=0, help="number of providers for validation")

    args = parser.parse_args()

    args.func(args)

# vim: ts=4 sw=4 sts=4 expandtab

# ReID Experiment Record

## Abstract
cross-domain ReID strong baseline+addtion

* name: baseline+addtion/resnet50.cls+trip.strong+addtion
* author: shaoxin
* basemodel: Trip.strong+addtion_path
* dataset: market_train_751
* target domain: DukeMTMC-reID
* loss: id_loss + trip_loss + center_loss

## Improvement
* Batch_size is modified to cross-domain tasks
* An addtion path has been added to improve its performance in cross-domain tasks

## Result
|    | dataset     |   epoch |   metric.mAP |   metric.top1 | owner      | setting      | task       |
|---:|:------------|--------:|-------------:|--------------:|:-----------|:-------------|:-----------|
|  1 | market-1501 |      10 |     0.168    |      0.347    | shaoxin    | single_query | human-reid |
|  2 | market-1501 |      20 |     0.240    |      0.434    | shaoxin    | single_query | human-reid |
|  3 | market-1501 |      30 |     0.268    |      0.469    | shaoxin    | single_query | human-reid |
|  4 | market-1501 |      40 |     0.260    |      0.454    | shaoxin    | single_query | human-reid |
|  5 | market-1501 |      50 |     0.285    |      0.489    | shaoxin    | single_query | human-reid |
|  0 | market-1501 |      60 |     0.288    |      0.493    | shaoxin    | single_query | human-reid |
|  6 | market-1501 |      70 |     0.283    |      0.488    | shaoxin    | single_query | human-reid |

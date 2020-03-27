# ReID Experiment Record

## Abstract
* cross domain:M->D
* modified-ReID baseline using id_loss + trip_loss + attention

* name: baseline+addtion/resnet50.cls+trip.P16_modified+attention
* author: shaoxin
* basemodel: resnet50
* dataset: market_train_751
* target domain: DukeMTMC-ReID
* loss: id_loss + trip_loss

## Iprovement
* maxpooling:the last average-pooling is changed to maxpooling
* attention machanism(although it seems useless)
* larger batchsize(P->128)
* new warm-up method
* new loss function location

## Result
epoch-120
top1: 0.4349
mAP: 0.2431

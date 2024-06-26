# Running Birdman's YOLOv7:
# Overview
This project focuses on developing an object detection system using Python and the YOLO (You Only Look Once) model specifically to detect House Finches in videos. The goal is to implement a robust solution capable of accurately identifying House Finches in video footage, which can be applied to wildlife monitoring, environmental studies, and birdwatching.

## Pre-Requisite:
Create a python virtual environment for better version control
With python, install the requirements within the YOLOv7/requirements.txt file:

      pip install -r requirements.txt

or

      python3 -m pip install -r requirements.txt


# Training:

Before you start training, head over to "YOLOv7/data" and edit the r-train.py.

You will need to specify the paths for:

      source_images_dir = '/data/Imgs'
      source_labels_dir = '/data/Labl'
      train_images_dir = '/data/train/images'
      train_labels_dir = '/data/train/labels'
      val_images_dir = '/data/val/images'
      val_labels_dir = '/data/val/labels'


Save the file and then run:

      python3 r-train.py

This will take images from "/data/Imgs" and their respective labels from "/data/Labl" and split them randomly for 70-30 for training and validation. 
Re-running this script will clear our the images in "/data/train/images" and "/data/val/images" and the labels in "/data/train/labels" and "/data/val/labels" and resplit the data randomly again.

Run this command or modify it to your computing ability:

      python3 train.py --workers 1 --device 0 --batch-size 10 --epochs 100 --img 640 360 --data data/house_finch_v0.yaml --hyp data/hyp.scratch.custom.yaml --cfg cfg/training/yolo_house_finch_v0.yaml --name *give_name* --weights weights/*your_weight*.pt

Description:

    --weights: initial weights path, default='yolo7.pt'
    --cfg: model.yaml path, default=''
    --data: data.yaml path, default='data/coco.yaml'
    --hyp: hyperparameters path, default='data/hyp.scratch.p5.yaml'
    --epochs: type=int, default=300
    --batch-s:total batch size for all GPUs, default=16
    --img-siz: [train, test] image sizes, default=[640, 640]
    --rect: :rectangular training
    --resume: resume most recent training, default=False
    --nosave: only save final checkpoint
    --notest: only test final epoch
    --noautoanchor: disable autoanchor check
    --evolve: evolve hyperparameters
    --bucket: gsutil bucket, default=''
    --cache-images: cache images for faster training
    --image-weights: use weighted image selection for training
    --device: cuda device, i.e. 0 or 0,1,2,3 or cpu, default=''
    --multi-scale: vary img-size +/- 50%%
    --single-cls: train multi-class data as single-class
    --adam: use torch.optim.Adam( optimizer
    --sync-bn: use SyncBatchNorm, only available in DDP mode
    --local_rank: DDP parameter, do not modify, default=-1
    --workers: maximum number of dataloader workers, default=8
    --project: save to project/name, default='runs/train'
    --entity: W&B entity, default=None
    --name: save to project/name, default='exp'
    --exist-ok: existing project/name ok, do not increment
    --quad: quad dataloader
    --linear-lr: linear LR
    --label-smoothing: Label smoothing epsilon, default=0.0
    --upload_dataset: Upload dataset as W&B artifact table
    --bbox_interval: Set bounding-box image logging interval for W&B, default=-1
    --save_period: Log model after every "save_period" epoch, default=-1
    --artifact_alias: version of dataset artifact to be us, default="latest"
    --freeze: Freeze layers, backbone of yolov7=50, first3=0 1 2, default=[0]
    --v5-metric: assume maximum recall as 1.0 in AP calculation



After training is complete, head over to "YOLOv7/runs/train" (assumimg default location) to see the new folder. Within that folder you will find metrics for the training seesion and find the weights within the "weights" folder.

# Testing on Real World Data

Run this command or modify it to your computing ability:

      python3 detect.py --weights weights/best_v5.pt --conf 0.5 --img-size 640 --source test/training_vid_02.mp4 --view-img --no-trace

Description:

    --source: source file/folder for images or videos, or use 0 for webcam, default=inference/images
    --img-size: inference size (pixels), default=640
    --conf-thres: object confidence threshold, default=0.25
    --iou-thres: IOU threshold for NMS, default=0.45
    --device: cuda device, i.e. 0 or 0,1,2,3 or cpu, default=
    --view-img: display results
    --save-txt: save results to *.txt
    --save-conf: save confidences in --save-txt labels
    --nosave: do not save images/videos
    --classes: filter by class: --class 0, or --class 0 2 3
    --agnostic-nms: class-agnostic NMS
    --augment: augmented inference
    --update: update all models
    --project: save results to project/name, default=runs/detect
    --name: save results to project/name, default=exp
    --exist-ok: existing project/name ok, do not increment
    --no-trace: don`t trace model

After testing, head over to "YOLOv7/runs/detect" (assuming default location) to see the results more accurately, using the "--view_img" flag also shows the results live. 
# Graphical user interface
- Run the ObjectDetectionAppWithUI.py to launch the GUI.
- Click the Upload Folder button to select a folder to analyze all of its contents (".mp4" files ONLY)
- It will do the prediction and output a result-selected video and a folder of text labels in the result folder.
- It will separate the frame of the predicted video based on the text labels, and the image will be on the Results folder, and in the Results folder there will be one folder for each video
- After it finishes detection, click the Analyze Folders to select a folder to view and update the UI

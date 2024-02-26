2024-26-02  Jorge Anzueto Arriaga  <JorgeArriaga12052001@gmail.com>

	Modified YOLOv7 from <https://github.com/WongKinYiu/yolov7>


	* Added file YOLOv7/cfg/training/yolo_house_finch_v0.yaml: Reduced the number of classes to three
	* Added file YOLOv7/data/house_finch_v0.yaml: Defined the relative path to the test and validation data.
  Defined the number of classes to detect to 3 and defined their names ('male_house_finch','female_house_finch','bird' )
	* Added directories YOLOv7/data/('Imgs', 'Labl', 'backup/Imgs', 'backup/Labl', 'train/images', 'train/labels', 'val/images', 'val/labels' ):
  'Imgs' and 'Labl' is where the images and THEIR CORRESPONDING labels will be placed. Labeling is really sensitive so do not replace the existing classes.txt within the 'Labl'
  directory. 'Imgs' and 'Labl' will have to contain all labeled images and their labels
  'backup' is there to for 'Imgs' and 'Labl' after each successful training. 
  'train' and 'val' directories are where images and THEIR CORRESPONDING labels will be randomly placed for training and validation
	* Added file YOLOv7/data/r-train.py: This python script will take images from 'Imgs' and its CORRESPONDING label from 'Labl' and place it randomly 
  to 'train' and 'val' directories. The train-validation split is 0.3, meaning that 30% of the data from 'Imgs' and their CORRESPONDING labels will be used
  for validation and the rest for training
  * Added file YOLOv7/weights: There are two weights ('yolov7.pt', 'best_v5.pt'). To start training from scratch use 'yolov7.pt'. 
  'best_v5.pt' is the best so far for identifying female_house_finch and male_house_finch.

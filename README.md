# Multi-Type-TD-TSR
Source Code of our Paper:
Multi-Type-TD-TSR Extracting Tables from Document Images using a Multi-stage Pipeline for Table Detection and Table Structure Recognition:

# Introduction
This github repository is work in progress

# Instructions
## Image Alignment Pre-Processing
For the image alignment pre-processing step there is one script available:

*  ```deskew.py```

To apply the image alignment pre-processing algorithm to all images in one folder, you need to execute:

    python3 deskew.py

with the following parameters

* ```--folder``` the input folder including document images
* ```--output``` the output folder for the deskewed images

## Table Structure Recognition (TSR)
For the table structure recognition we offer a simple script for different approaches

* ```tsr.py```

To apply a table structure recognition algorithm to all images in one folder, you need to execute:a

    python3 tsr.py

with the following parameters

* ```--folder``` path of the input folder including table images
* ```--type``` the table structure recognition type ```type in ["borderd", "unbordered", "partially", "partially_color_inv"] ```
* ```--img_output``` output folder path for the processed images
* ```--xml_output``` output folder path for the xml files including bounding boxes

## Table Detection and Table Structure Recognition (TSR)
To appy the table detection with a followed table structure recogniton 

* ```tdtsr.py```

To apply a table structure recognitio algorithm to all images in one folder, you need to execute:

    python3 tdtsr.py

with the following parameters

* ```--folder``` path of the input folder including table images
* ```--type``` the table structure recognition type ```type in ["borderd", "unbordered", "partially", "partially_color_inv"] ```
* ```--tsr_img_output``` output folder path for the processed table images
* ```--td_img_output``` output folder path for the produced table cutouts
* ```--xml_output``` output folder path for the xml files for tables and cells including bounding boxes
* ```--config``` path of detectron2 configuration file for table detection
* ```--yaml``` path of detectron2 yaml file for table detection
* ```--weights``` path of detectron2 model weights for table detection

## Evaluation
To evaluate the table structure recognition algorithm we provide the following script:

*  ```evaluate.py```

to apply the evaluation the table images and their labels in xml-format have to be the same name and should lie in a single folder.
The evaluation could be started by:

    python3 evaluate.py
  
with the following parameter

* ```--dataset``` dataset folder path containing table images and labels in .xml format

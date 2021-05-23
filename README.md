# Multi-Type-TD-TSR
Check it out on <a href="https://colab.research.google.com/github/Psarpei/Multi_Type_TD_TSR/blob/main/Table_Recognition.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
Source Code of our Paper:
Multi-Type-TD-TSR Extracting Tables from Document Images using a Multi-stage Pipeline for Table Detection and Table Structure Recognition:

## Multi-Type-TD-TSR: whole pipeline (left) and partially borrdered tables (right)
<img align="left" width="390" height="" src="gifs/whole_pipeline.gif">
<img align="right" width="390" height="" src="gifs/partially_bordered.gif">

<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

## Multi-Type-TD-TSR on Fully Bordered Tables (left) and Unboardered Tables (right)
<img align="left" width="390" height="" src="gifs/fully_bordered.gif">
<img align="right" width="390" height="" src="gifs/unboardered.gif">

<br/>
<br/>



# Introduction
This github repository is work in progress

# Table Structure Recognition Results
ICDAR 19 (Track B2)

|                 | IoU | IoU | IoU | IoU | Weighted|
 -----------------|:---:|-----|-----|-----|---------
|Team             | 0.6 | 0.7 | 0.8 | 0.9 | Average |
|CascadeTabNet    |0.438|0.354|0.19 |0.036|  0.232  |
|NLPR-PAL         |0.365|0.305|0.195|0.035|  0.206  |
|Multi-Type-TD-TSR|0.589|0.404|0.137|0.015|  0.253  |

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

To apply a table structure recognition algorithm to all images in one folder, you need to execute:

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

# Get Data

*  test dataset for table structure recognition including table images and annotations can be downloaded [here](https://drive.google.com/drive/folders/1COTV5f7dEAA4Txmxy3LVfcNHiPSc4Bmp?usp=sharing) 
* table detection detectron2 model weights and configuration files can be downloaded [here](https://drive.google.com/drive/folders/1ry5C9Qs5lyskZeDzBJNYCbNTN1LH1rjn?usp=sharing)

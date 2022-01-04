import numpy as np
import cv2
import argparse
import os
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

from detectron2.data import DatasetCatalog, MetadataCatalog

import pandas as pd

import json
import itertools

from TSR import table_structure_recognition_all as tsra
from TSR import table_structure_recognition_lines as tsrl
from TSR import table_structure_recognition_lines_wol as tsrlwol
from TSR import table_structure_recognition_wol as tsrwol
import table_detection as td

from document_xml import output_to_xml

if __name__ == "__main__":
    type_dict = {"borderd":tsrl, "unbordered":tsrwol, "partially":tsrlwol, "partially_color_inv":tsra}
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="Input folder")
    parser.add_argument("--tsr_img_output", help="Table structure recognition image output folder", default= "")
    parser.add_argument("--td_img_output", help="Table detection image output folder", default= "")
    parser.add_argument("--xml_output", help="Document XML output folder", default="")
    parser.add_argument("--type", help="borderd, unbordered, partially, partially_color_inv", default="partially")
    parser.add_argument("--config", help="detectron2 configuration file for table detection", default="")
    parser.add_argument("--yaml", help="detectron2.yaml file for table detection", default="")
    parser.add_argument("--weights", help="detectron2 model weights for table detection", default="")

    args = parser.parse_args()

    #create detectron config
    cfg = get_cfg(args.config)

    #set yaml
    cfg.merge_from_file(args.yaml)

    #set model weights
    cfg.MODEL.WEIGHTS = args.weights # Set path model .pth

    predictor = DefaultPredictor(cfg) 

    files = os.listdir(args.folder)

    for file in files:
        img = cv2.imread(args.folder + "/" + file)
        table_list, table_coords = table_detection.make_prediction(deskewed_image, predictor)
        list_table_boxes = []

        for table in table_list:
            boxes, table_processed = type_dict[args.type].recognize_structure(table)
            list_table_boxes.append(boxes)
            
            if args.tsr_img_output:
                cv2.imwrite(args.tsr_img_output + "/" + file, table_processed)
            if args.td_img_output:
                cv2.imwrite(args.td_img_output + "/" + file, table)
            if args.td_xml_output:
                print(args.xml_output + "/" + file[:-3])
                output_to_xml(list_table_boxes, args.xml_output + "/" + file[:-3])

import numpy as np
import cv2
import argparse
import os

from TSR import table_structure_recognition_all as tsra
from TSR import table_structure_recognition_lines as tsrl
from TSR import table_structure_recognition_lines_wol as tsrlwol
from TSR import table_structure_recognition_wol as tsrwol

from table_xml import output_to_xml

if __name__ == "__main__":
    type_dict = {"borderd":tsrl, "unbordered":tsrwol, "partially":tsrlwol, "partially_color_inv":tsra}
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="input folder")
    parser.add_argument("--img_output", help="image output folder", default= "")
    parser.add_argument("--xml_output", help="xml output folder", default="")
    parser.add_argument("--type", help="borderd,unbordered,partially,partially_color_inv", default="partially")

    args = parser.parse_args()

    files = os.listdir(args.folder)
    
    for file in files:
        print(file)
        print(args.folder)
        img = cv2.imread(args.folder + "/" + file)
        boxes, img_processed = type_dict[args.type].recognize_structure(img)
        print(args.img_output + "/" + file)
        if args.img_output:
            cv2.imwrite(args.img_output + "/" + file, img_processed)
        if args.xml_output:
            print(args.xml_output + "/" + file[:-3])
            output_to_xml(boxes, args.xml_output + "/" + file[:-3])

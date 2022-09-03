import cv2
from google.colab.patches import cv2_imshow
import numpy as np

def plot_prediction(img, predictor):
    
    outputs = predictor(img)

    # Blue color in BGR 
    color = (255, 0, 0) 
  
    # Line thickness of 2 px 
    thickness = 2

    for x1, y1, x2, y2 in outputs["instances"].get_fields()["pred_boxes"].tensor.to("cpu").numpy():
        # Start coordinate 
        # represents the top left corner of rectangle 
        start_point = int(x1), int(y1) 
  
        # Ending coordinate
        # represents the bottom right corner of rectangle 
        end_point = int(x2), int(y2) 
  
        # Using cv2.rectangle() method 
        # Draw a rectangle with blue line borders of thickness of 2 px 
        img = cv2.rectangle(np.array(img, copy=True), start_point, end_point, color, thickness)

    # Displaying the image
    print("TABLE DETECTION:")  
    cv2_imshow(img)

def make_prediction(img, predictor):
    
    #img = cv2.imread(img_path)
    outputs = predictor(img)

    table_list = []
    table_coords = []

    for i, box in enumerate(outputs["instances"].get_fields()["pred_boxes"].tensor.to("cpu").numpy()):
        x1, y1, x2, y2 = box
        table_list.append(np.array(img[int(y1):int(y2), int(x1):int(x2)], copy=True))
        table_coords.append([int(x1),int(y1),int(x2-x1),int(y2-y1)])
        print("TABLE", i, ":")
        cv2_imshow(img[int(y1):int(y2), int(x1):int(x2)])
        print()

    return table_list, table_coords

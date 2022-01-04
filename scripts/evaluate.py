import os
import xml.etree.ElementTree as ET
import cv2
import argparse

# without pre-processing
from TSR.table_structure_recognition_lines_wol import recognize_structure
# with pre-processing
# from table_structure_recognition_all import recognize_structure


def calc_iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


def check_bbox(bbox_pred, root, threshold):
    for child in root:
        if(child.tag == "object") and (child[0].text == "row"):
            for child2 in root:
                if(child2.tag == "object") and (child2[0].text == "column"):
                    xmin = int(child2[4][0].text)
                    ymin = int(child[4][1].text)
                    xmax = int(child2[4][2].text)
                    ymax = int(child[4][3].text)
                    bbox_tar = (xmin, ymin, xmax, ymax)
                    iou = calc_iou(bbox_pred, bbox_tar)
                    if(iou > threshold):
                        return 1
    return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help="dataset folder")

    args = parser.parse_args()

    weighted_avg = 0
    for thresh in range(6, 10):
        threshold = (thresh / 10)
        total = 0
        checks = 0

        folder = args.dataset
        files = os.listdir(folder)

        for i in range(0, len(files), 2):
            img = cv2.imread(folder + files[i])

            """
            cv2.imshow("img",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            """

            tree = ET.parse(folder + files[i+1])
            root = tree.getroot()
            try:
                boxes, img_new = recognize_structure(img)
            except:
                continue

            """
            cv2.imshow("img",img_new)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            """

            for j in range(len(boxes)):
                for k in range(len(boxes[0])):
                    if(boxes[j][k] == []):
                        continue
                    x1 = boxes[j][k][0][0]
                    y1 = boxes[j][k][0][1]
                    x2 = boxes[j][k][0][0] + boxes[j][k][0][2]
                    y2 = boxes[j][k][0][1] + boxes[j][k][0][3]
                    bbox_pred = (x1, y1, x2, y2)
                    total += 1
                    checks += check_bbox(bbox_pred, root, threshold)

        f1 = 0 if(checks == 0.0) else checks / total
        print(
            f"checks {checks}, total {total}, F1 {f1}, threshold {threshold}"
        )
        weighted_avg += f1 * threshold/3
    print("weighted_average", weighted_avg)

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract as tess
import pytesseract

def output_to_csv (finalboxes, img):
    testx = 0
    # from every single image-based cell/box the strings are extracted via pytesseract and stored in a list
    outer = []
    for i in range(len(finalboxes)):
        for j in range(len(finalboxes[i])):
            inner = ''
            if (len(finalboxes[i][j]) == 0):
                outer.append(' ')
            else:
                for k in range(len(finalboxes[i][j])):
                    y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], \
                                finalboxes[i][j][k][3]

                    finalimg = img[x:x + h, y:y + w]

                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                    border = cv2.copyMakeBorder(finalimg, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255, 255])
                    resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    dilation = cv2.dilate(resizing, kernel, iterations=1)
                    erosion = cv2.erode(dilation, kernel, iterations=2)

                    if(erosion.sum() != erosion.shape[0]*erosion.shape[1]*255):
                        out = pytesseract.image_to_string(erosion, config='')
                    else:
                        out = ""

                    if(out == ""):

                        out = pytesseract.image_to_string(erosion, config='--psm 7')
                        if(len(out[:-2]) >1):
                            out = ""

                    inner = inner + " " + out[:-2]
                outer.append(inner)

    # Creating a dataframe of the generated OCR list
    arr = np.array(outer)
    dataframe = pd.DataFrame(arr.reshape(len(finalboxes), len(finalboxes[0])))
    print(dataframe)
    data = dataframe.style.set_properties(align="left")
    # Converting dataframe into an excel-file
    data.to_excel("output.xlsx")
        

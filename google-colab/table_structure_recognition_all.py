import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


from google.colab.patches import cv2_imshow

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract as tess
import pytesseract


def recognize_structure(img):
    #tess.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    #print(img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_height, img_width = img.shape

    #print("img_height", img_height, "img_width", img_width)
    cv2_imshow(img,)

    # thresholding the image to a binary image
    thresh, img_bin = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
    #thresh, img_bin = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #img_bin = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,5,5)

    cv2_imshow(img_bin)

    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #invert = False
    invert = False
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        #print("x", x, "y", y, "w", w, "h", h)
        if (w < 0.9 * img_width and h < 0.9*img_height and (w > max(10,img_width / 30) and h > max(10,img_height / 30))):
        #if(w*h > 100 and (w < 0.9 * img_width and h < 0.9*img_height)):
            #invert = True
            invert = True
            #print("size", img_width * img_height)
            #image = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img_bin[y:y+h,x:x+w] = 255 - img_bin[y:y+h,x:x+w]

    cv2_imshow(img_bin)

    img_bin = 255 - img_bin if (invert) else img_bin

    cv2_imshow(img_bin)

    img_bin_inv = 255 - img_bin

    cv2_imshow(img_bin_inv)

    ############################################################################################################################################
    
    kernel_len_ver = max(10, img_height // 50)
    kernel_len_hor = max(10, img_width // 50)
    # Defining a vertical kernel to detect all vertical lines of image
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len_ver)) #shape (kernel_len, 1) inverted! xD
    #print("ver", ver_kernel)
    #print(ver_kernel.shape)

    # Defining a horizontal kernel to detect all horizontal lines of image
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len_hor, 1)) #shape (1,kernel_ken) xD
    #print("hor", hor_kernel)
    #print(hor_kernel.shape)


    # A kernel of 2x2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    #print(kernel)
    #print(kernel.shape)

    # Use vertical kernel to detect and save the vertical lines in a jpg
    image_1 = cv2.erode(img_bin_inv, ver_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=4)
    
    # Plot the generated image
    cv2_imshow(image_1)
    
    cv2_imshow(vertical_lines)

    # Use horizontal kernel to detect and save the horizontal lines in a jpg
    image_2 = cv2.erode(img_bin_inv, hor_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=5)
    # Plot the generated image
    cv2_imshow(image_2)
    
    cv2_imshow(horizontal_lines)

    
    # Combine horizontal and vertical lines in a new third image, with both having same weight.
    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    cv2_imshow(img_vh)

    # Eroding and thesholding the image
    img_vh = cv2.dilate(img_vh, kernel, iterations=3)
    cv2_imshow(img_vh)


    
    thresh, img_vh = (cv2.threshold(img_vh, 50, 255, cv2.THRESH_BINARY ))

    #print("last")
    cv2_imshow(img_vh)

    #print("img_bin")
    cv2_imshow(img_bin)
    
    #print("bitor")
    bitor = cv2.bitwise_or(img_bin, img_vh)
    cv2_imshow(bitor)

    
    img_median = bitor #cv2.medianBlur(bitor, 3)
    cv2_imshow(img_median)

    
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, img_height*2)) #shape (kernel_len, 1) inverted! xD
    vertical_lines = cv2.erode(img_median, ver_kernel, iterations=1)
    cv2_imshow(vertical_lines)

    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (img_width*2, 3)) #shape (kernel_len, 1) inverted! xD
    horizontal_lines = cv2.erode(img_median, hor_kernel, iterations=1)
    cv2_imshow(horizontal_lines)

    
    # A kernel of 2x2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    #print(kernel)
    #print(kernel.shape)

    # Combine horizontal and vertical lines in a new third image, with both having same weight.
    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    cv2_imshow(img_vh)

    cv2_imshow(~img_vh)

    # Eroding and thesholding the image
    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    cv2_imshow(img_vh)

    thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY )
    #cv2.imwrite("/Users/marius/Desktop/img_vh.jpg", img_vh)
    cv2_imshow(img_vh)
    
    #print("result")
    #bitor but then 5->4 or 3
    bitxor = cv2.bitwise_xor(img_bin, img_vh)
    bitnot = cv2.bitwise_not(bitxor)
    # Plotting the generated image
    cv2_imshow(bitnot)
    
    # Detect contours for following box detection
    contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))
    #print(contours[0])
    #print(len(contours[0]))
    #print(cv2.boundingRect(contours[0]))

    def sort_contours(cnts, method="left-to-right"):
        # initialize the reverse flag and sort index
        reverse = False
        i = 0
        # handle if we need to sort in reverse
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True
        # handle if we are sorting against the y-coordinate rather than
        # the x-coordinate of the bounding box
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1
        # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i], reverse=reverse))
        # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)


    # Sort all the contours by top to bottom.
    contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")

    # Creating a list of heights for all detected boxes
    heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]

    # Get mean of heights
    mean = np.mean(heights)

    # Create list box to store all boxes in
    box = []
    # Get position (x,y), width and height for every contour and show the contour on image
    #print("lencontours", len(contours))
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        #print("x", x, "y", y, "w", w, "h", h)
        if (w < 0.9*img_width and h < 0.9*img_height):
            image = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box.append([x, y, w, h])

    cv2_imshow(image)

    # Creating two lists to define row and column in which cell is located
    row = []
    column = []
    j = 0

    #print("len box", len(box))
    # Sorting the boxes to their respective row and column
    for i in range(len(box)):
        if (i == 0):
            column.append(box[i])
            previous = box[i]

        else:
            if (box[i][1] <= previous[1] + mean / 2):
                column.append(box[i])
                previous = box[i]

                if (i == len(box) - 1):
                    row.append(column)

            else:
                row.append(column)
                column = []
                previous = box[i]
                column.append(box[i])

    #print(column)
    #print(row)

    # calculating maximum number of cells
    countcol = 0
    index = 0
    for i in range(len(row)):
        current = len(row[i])
        #print("len",len(row[i]))
        if current > countcol:
            countcol = current
            index = i

    #print("countcol", countcol)

    # Retrieving the center of each column
    #center = [int(row[i][j][0] + row[i][j][2] / 2) for j in range(len(row[i])) if row[0]]
    center = [int(row[index][j][0] + row[index][j][2] / 2) for j in range(len(row[index]))]
    #print("center",center)

    center = np.array(center)
    center.sort()
    #print("center.sort()", center)
    # Regarding the distance to the columns center, the boxes are arranged in respective order

    finalboxes = []
    for i in range(len(row)):
        lis = []
        for k in range(countcol):
            lis.append([])
        for j in range(len(row[i])):
            diff = abs(center - (row[i][j][0] + row[i][j][2] / 4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(row[i][j])
        finalboxes.append(lis)

    
    return finalboxes, img_bin
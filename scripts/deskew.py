import numpy as np
import cv2
import argparse
import os
import sys

class Image():
    """Image operations"""
    def __init__(self, input_folder, file_name, output_folder) -> None:
        self.input_image_path = f"{input_folder}/{file_name}"
        self.output_image_path = f"{output_folder}/{file_name}"
        self.__read_image()
        self.__blur_image()
        self.__threshold_image()
        self.__get_coordinates()

    def __read_image(self) -> None:
        self.original_image = cv2.imread(self.input_image_path)

    def __blur_image(self) -> None:
        self.blur_image = cv2.medianBlur(self.original_image, 5) # MedianBlur used to remove black artefacts from the image

    def __threshold_image(self) -> None:
        self.grayscale_image = cv2.bitwise_not(cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)) # Grayscale convesion to ensure foreground is white and background is black
        self.threshold_image = cv2.threshold(
            self.grayscale_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] # Set all foreground pixels to 255 and background pixels to 0

    def __get_coordinates(self) -> None:
        self.coordinates = np.column_stack(np.where(self.threshold_image > 0)) # grab the (x, y) coordinates of all pixel values that are greater than zero and compute a bounding box

    def deskew_image(self):
        """
        Adapted from:
        https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
        """

        angle = cv2.minAreaRect(self.coordinates)[-1] # the `cv2.minAreaRect` function returns values in the range [-90, 0); as the rectangle rotates clockwise the returned angle trends to 0 -- in this special case we need to add 90 degrees to the angle
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        # rotate the image to deskew it
        height, width = self.blur_image.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        self.deskewed_image = cv2.warpAffine(
            self.original_image, rotation_matrix, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def write_image(self) -> None:
        cv2.imwrite(self.output_image_path, self.deskewed_image)



class Parser():
    """Defining and parsing command-line arguments"""
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser('deskew', 'python3 -m deskew --input input_folder --output output_folder', 'Deskew images')
        self.__add_arguments()

    def __add_arguments(self) -> None:
        """ Add arguments to the parser """
        self.parser.add_argument("--input", help="Input folder")
        self.parser.add_argument("--output", help="Output folder")
        return

    def parse_arguments(self, args: list) -> argparse.Namespace:
        """ Parse arguments """
        if args:
            return self.parser.parse_args(args)
        else:
            raise Exception


if __name__ == "__main__":
    parser = Parser()
    
    args = parser.parse_arguments(sys.argv[1:])

    files = os.listdir(args.folder)

    for file_ in files:
        print(file_)
        print(args.folder)
        image = Image(args.input, file_, args.output)
        image.deskew_image()
        image.write_image()

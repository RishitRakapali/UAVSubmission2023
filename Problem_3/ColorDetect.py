import cv2
import numpy as np


# Trouble with gray and black color. Still trying to detect
class Color:
    # Dictionary for hsv color ranges for masking image
    colorsRanges = {
        "red_Lower": [0, 50, 50],
        "red_Upper": [10, 255, 255],

        "blue_Lower": [110, 50, 50],
        "blue_Upper": [125, 255, 255],

        "green_Lower": [40, 20, 50],
        "green_Upper": [90, 255, 255],

        "yellow_Lower": [25, 50, 50],
        "yellow_Upper": [30, 255, 255],

        "orange_Lower": [11, 50, 50],
        "orange_Upper": [20, 255, 255],

        "pink_Lower": [142, 50, 50],
        "pink_Upper": [150, 255, 255],

        "purple_Lower": [130, 50, 50],
        "purple_Upper": [142, 255, 255],
    }


# Child of Color class - Main methods to find colors in the image
class Image(Color):
    # Constructor - initializes the path of the image, the source image, and the hsv values
    def __init__(self, imgPath):
        self.imgPath = imgPath
        self.srcImg = None
        self.hsv = None

        # Calls readImg method to set srcImg and hsv values
        self.readImg(imgPath)
        # Calls main method that finds colors in the image
        self.findImageColors(self.colorsRanges, self.hsv)

    # Determines image path,
    def readImg(self, imgPath):
        self.srcImg = cv2.imread(imgPath)
        self.hsv = cv2.cvtColor(self.srcImg, cv2.COLOR_BGR2HSV)
    # Display image to console
    def displayImg(self, img):
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # Counts black and white pixels in the image
    def whiteBlackPixels(self, img):
        number_of_white_pix = np.sum(img == 255)
        # number_of_black_pix = np.sum(img == 0)

        if number_of_white_pix >= 5000:
            return True
    # Masks the image given the hsv values
    def maskImg(self, hsv, lower_mask, upper_mask):
        self.hsv = cv2.cvtColor(self.srcImg, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(lower_mask), np.array(upper_mask))

        return mask
    # Main method to determine colors in the image
    def findImageColors(self, colorsRanges, hsv):
        # Array that stores the main colors
        imageColors = []

        # Keys and Values in the ColorsRanges dictionary
        rangeValues = colorsRanges.values()
        colors = colorsRanges.keys()

        # Indexes that loop through values in the dictionary
        lower_mask_index = 0
        upper_mask_index = 1

        # Masks image only to determine white pixels. If it finds more than 1000 pixels, stores white to imageColors
        # array
        whiteMask = self.maskImg(hsv, np.array([0, 0, 0]), np.array([255, 10, 255]))
        if np.sum(whiteMask == 255) > 1000:
            imageColors.append('white')

        # Loops through lower and upper hsv color ranges in the dictionary. Masks each image, and if it finds more than
        # 5k pixels it adds it to the imageColors list
        while lower_mask_index < (len(colorsRanges) - 1):
            lower_mask = list(rangeValues)[lower_mask_index]
            upper_mask = list(rangeValues)[upper_mask_index]

            mask = self.maskImg(hsv, lower_mask, upper_mask)

            if self.whiteBlackPixels(mask):
                detectedColor = list(colors)[lower_mask_index]
                imageColors.append(detectedColor.split("_")[0])

            lower_mask_index += 2
            upper_mask_index += 2


        print( ",".join(imageColors) )


def main():
    # Change image path here for input
    imgPath = "/Users/Rishit/PycharmProjects/AVHS_Robotics/UAVapplication/Problem_3/prob2_input3.png"

    # Initializes colorDetect as object of Image class, and calls __init__ function. __init__ function set of other
    # methods inside Image class to determine colors
    colorDetect = Image(imgPath)

    # Display masked image to console
    colorDetect.displayImg(colorDetect.srcImg)

# Main function
if __name__ == "__main__":
    main()

# Program mixes orange values to be very close to red values. Messes up the program for second input file.

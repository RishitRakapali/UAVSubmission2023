import numpy as np


class Pinpointing:
    # Set class variables as constants
    verticalFOV = 15.6
    horizontalFOV = 23.4
    resolutionX = 5471
    resolutionY = 3647
    centerPx = [2735.5, 1823.5]

    # Constructor - initializes the path of the image, all input data gets stored in a list, and conversion methods from
    # pixel to meters and meters to GPS are initialized
    def __init__(self, filePath):
        self.filePath = filePath
        self.inputData = None

        self.horizontalPxToMeters = None
        self.VerticalPxToMeters = None

        self.metersToLongitude = None
        self.metersToLatitude = None

        # Calls other methods to initialize vars
        self.readInput(self.filePath)
        self.pixeltometer()
        self.meterToGPS()
    # Read input line by line from input file, and stores in a list
    def readInput(self):
        file = open(self.filepath)

        line_list = []
        for line in file:
            line = line.strip()
            line_list.append(line)

        line_list[0] = line_list[0].split(" ")

        self.inputData = line_list

        file.close()
    # Write the output to console
    def writeOutput(self, differencesList):
        for x in range(len(differencesList)):
            print(*differencesList[x], sep=" ")
    # Formulas to convert pixels to meters
    # To calculate these formula I used trig ratios of right triangles
    # Easier way to read formula: ( (tan( horizontal FOV / 2 ) * height ) / (centerPixelXcoord / 2)) and
    # ( (tan( vertical FOV / 2 ) * height ) / (centerPixelYcoord / 2))
    # Result in 2 vars, which you can multiply pixls with to get it in meters
    def pixeltometer(self):
        height = float(self.inputData[0][0])

        self.horizontalPxToMeters = (np.tan((Pinpointing.horizontalFOV / 2) * np.pi/180) * height) / Pinpointing.centerPx[0]
        self.verticalPxToMeters = (np.tan((Pinpointing.verticalFOV / 2) * np.pi/180) * height) / Pinpointing.centerPx[1]

    # Formula to convert long and lat into meters
    # 1 degree long = 111320 meters
    # 1 degree lat = 111000 meters
    def meterToGPS(self):

        self.metersToLongitude = 111320

        self.metersToLatitude = 111000

    # Calculates the final GPS coordinates of input coordinates
    def finalGPSCoordinates(self):
        # Stores the final coordinates
        finalGPSCoords = []
        # Where the number of coordinates in list is located
        numOfCoords = int(self.inputData[0][3])

        # Skips the first list since it is not a coordinate
        for x in range(numOfCoords):
            if x == 0:
                continue

            # Splits coordinates into x and y values
            xPxCoordinate = self.inputData[x].split(" ")[0]
            yPxCoordinate = self.inputData[x].split(" ")[1]
            # Find difference between each input coordinate and center coordinate in pixels
            diffX = Pinpointing.centerPx[0] - float(xPxCoordinate)
            diffY = Pinpointing.centerPx[1] - float(yPxCoordinate)
            # Converts pixel differences into meters
            diffXinMeters = diffX * self.horizontalPxToMeters
            diffYinMeters = diffY * self.verticalPxToMeters
            # Converts meter differences into longitude and latitude
            diffXinGPS = diffXinMeters / self.metersToLongitude
            diffYinGPS = diffYinMeters / self.metersToLatitude
            # Find difference between each input coordinate and center coordinate in longitude and latitude
            finalGPSCoordX = float(self.inputData[0][1]) - diffXinGPS
            finalGPSCoordY = float(self.inputData[0][2]) - diffYinGPS

            # Stores each x and y in a list
            finalGPSCoords.append([finalGPSCoordX, finalGPSCoordY])

        # Return 2d list of all the x and y differences between center pixel and all input pixels
        return finalGPSCoords


def main():
    # Change input file path here to test different cases
    filepath = '/Users/Rishit/PycharmProjects/AVHS_Robotics/UAVapplication/Problem_2/prob2_input.txt'

    #Create obj of pinpoiting class
    objPinpointing = Pinpointing(filepath)

    #Calculatoes the final gps coordinates of the inputs
    finalGPSCoords = objPinpointing.finalGPSCoordinates()

    objPinpointing.writeOutput(finalGPSCoords)


# Main function
if __name__ == "__main__":
    main()



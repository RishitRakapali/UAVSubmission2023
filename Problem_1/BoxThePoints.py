import numpy as np

class BoxThePoints:
    def __init__(self, filepath):
        self.filepath = filepath
        self.inputData = None

        self.readInput()

    def readInput(self):
        file = open(self.filepath)

        line_list = []
        for line in file:
            line = line.strip()
            line_list.append(line)
        file.close()

        inputCoords = []

        for x in range(len(line_list)):
            if x == 0:
                continue
            inputCoords.append(line_list[x].split(" "))

        for lst in range(len(inputCoords)):
            for element in range(len(inputCoords[lst])):
                inputCoords[lst][element] = int(inputCoords[lst][element])

        self.inputData = inputCoords

    # Convex Hull is a useful way to get all the point that make a polygon, which compasses all other point
    # Basically like the goal for this problem but with a polygon instead of rectangle
    # significant reduces points from input coordinates, that potentially might increase run time
    def scanCoodinates(self):
        def crossProduct(o, a, b):
            # find the cross products of vectors, OA and OB
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        # Find the point with the lowest y coord (and leftmost x coord if it was tied with other y coord)
        startPoint = min(self.inputData, key=lambda point: (point[1], point[0]))

        # sort the points based on polar angle from srtart point
        sortedPoints = sorted(self.inputData, key=lambda point: (np.arctan2(point[1] - startPoint[1], point[0] - startPoint[0]), point))

        # Make list to store corners of the convex hull
        hull = [sortedPoints[0], sortedPoints[1]]

        # Iterate through sorted points starting after the 3rd point
        for i in range(2, len(sortedPoints)):
            # while the last 2 points in the hull and the current point make a non-convex turn
            # remove the last point from the hull until a convex turn is made
            while len(hull) > 1 and crossProduct(hull[-2], hull[-1], sortedPoints[i]) <= 0:
                hull.pop()
            # Add the current point to the hull - helpful to convex hull.
            hull.append(sortedPoints[i])
        # Return the list of points in the convex hull
        return hull

    # returns slope and b given 2 coords
    def equationOfALine(self, coords):
        #y = mx + b
        # coords in format of [[x, y], [x, y]]
        x1 = coords[0][0]
        y1 = coords[0][1]
        x2 = coords[1][0]
        y2 = coords[1][1]

        slope = 0
        numerator = (y2 - y1)
        denominator = (x2 - x1)
        if (x2 - x1) == 0:
            slope = None
            b = x1
        else:
            slope = (y2 - y1) / (x2 - x1)
            b = y1 - (slope * x1)

        return [slope, b]

    def findBorderLines(self, convexHull):
        print(self.inputData)
        print("Convex Hull:", convexHull)

        # Find all possible pairs of coordinates to create lines out of and stores it in coordPairForLines
        coordPairForLines = []
        for coord in range(len(convexHull)):
            if coord < len(convexHull) - 1:
                coordPairForLines.append( [convexHull[coord], convexHull[coord + 1]] )
            elif coord == len(convexHull) - 1:
                coordPairForLines.append( [convexHull[coord], convexHull[0]] )

        # uses equation of a line method to return all slopes and b values of each pair of coordinates
        # this will help determine the borders of the rectangle
        lines = []
        for coords in range(len(coordPairForLines)):
            coordinatePair = coordPairForLines[coords]
            print(coordinatePair)
            lines.append(BoxThePoints.equationOfALine(self, coordinatePair))
        print(lines)

        # Code not done: Next steps

        # 1. Find parallel lines: find the corresponding parallel line to each line determined in lines[]
        '''
            for each line find midpoint - check distance between midpoint of line and other cords on plane
            find the furthest point and create a parallel line that pass through that point with the same slope
        '''
        # 2. create rectangles by creating 2 perpendicular lines from corners to parallel line
        '''
            use 2 original coordinates, take inverse slope of that original line, and create 2 other parallel lines to create rectangle
        '''
        # 3. Determine area of each rectangle and find the smallest area
        '''
            Solve the intersecting perpendicular lines, by setting them equal to each other to find the other two corners
            Find area by using distance formula between coordinate, then using base * height
            Find smallest area
        '''
        # 4. Using top-left and top-right intersection points of the
        #    rectangle, use arc-tan on the slope to determine the tilt
        '''
            Use top-left and top-right coordinates of the rectangle, create triangle with x-axis
            use arctan on the slope to find degree tilt
        '''

def main():
    filepath = '/Users/Rishit/PycharmProjects/AVHS_Robotics/UAVapplication/Problem_1/prob1_input.txt'

    objBoxThePoints = BoxThePoints(filepath)

    convexHull = objBoxThePoints.scanCoodinates()

    objBoxThePoints.findBorderLines(convexHull)

# Main function
if __name__ == "__main__":
    main()
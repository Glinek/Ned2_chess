import cv2
import numpy as np

# Load the image
image = cv2.imread(r'F:\PjSB1 - Current, Hibernating projects\Current Projects\Niryo chess\tests\edgeDetectedImages\canny_edges.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Use HoughLinesP to detect lines
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

# Draw the lines on the image
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Save the result
cv2.imwrite('lines_detected.jpg', image)

# Display the result
cv2.imshow('Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
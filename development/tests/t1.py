import cv2
import numpy as np

# Load the image
#image = cv2.imread(r'F:\PjSB1 - Current, Hibernating projects\Current Projects\Niryo chess\tests\edgeDetectedImages\canny_edges2.jpg')
image = cv2.imread(r'/home/glinek/Programming/ChessRobot/Ned2_chess/development/boardPhotos-mk3/fixedBoardGreen2.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Use HoughLines to detect lines
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

# Draw the lines on the image
if lines is not None:
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Save the result
cv2.imwrite('lines_detected.jpg', image)

# Display the result
cv2.imwrite('Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
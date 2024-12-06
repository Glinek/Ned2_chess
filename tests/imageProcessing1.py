import cv2
import numpy as np

def detect_move(before_img_path, after_img_path):
    # Load the images
    before_img = cv2.imread(before_img_path)
    after_img = cv2.imread(after_img_path)

    # Convert images to grayscale
    before_gray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after_img, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between the images
    diff = cv2.absdiff(before_gray, after_gray)

    # Threshold the difference image
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours
    min_contour_area = 100  # Adjust this value based on your images
    contours = [c for c in contours if cv2.contourArea(c) > min_contour_area]

    # Draw contours on the images
    before_img_contours = before_img.copy()
    after_img_contours = after_img.copy()
    cv2.drawContours(before_img_contours, contours, -1, (0, 255, 0), 2)
    cv2.drawContours(after_img_contours, contours, -1, (0, 255, 0), 2)

    # Display the images with contours
    cv2.imshow('Before Move', before_img_contours)
    cv2.imshow('After Move', after_img_contours)
    cv2.imshow('Difference', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Return the contours for further processing if needed
    return contours

# Example usage
before_img_path = r'F:\PjSB1 - Current, Hibernating projects\Current Projects\Niryo chess\boards\board31.jpg'
after_img_path = r'F:\PjSB1 - Current, Hibernating projects\Current Projects\Niryo chess\boards\board32.jpg'
detect_move(before_img_path, after_img_path)
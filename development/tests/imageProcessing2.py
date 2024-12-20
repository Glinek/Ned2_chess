import cv2
import numpy as np

class EdgeDetection:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            raise ValueError("Image not found or unable to load.")
    
    def apply_canny(self, threshold1, threshold2):
        edges = cv2.Canny(self.image, threshold1, threshold2)
        return edges
    
    def apply_sobel(self, ksize=3):
        grad_x = cv2.Sobel(self.image, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(self.image, cv2.CV_64F, 0, 1, ksize=ksize)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        sobel = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return sobel
    
    def apply_laplacian(self):
        laplacian = cv2.Laplacian(self.image, cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)
        return laplacian
    
    def save_image(self, image):
        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Example usage:
if __name__ == "__main__":
    edge_detector = EdgeDetection(r'/home/glinek/Programming/ChessRobot/Ned2_chess/development/boardPhotos-mk3/fixedBoardGreen2.png')
    
    canny_edges = edge_detector.apply_canny(100, 200)
    edge_detector.save_image(canny_edges)
    
    sobel_edges = edge_detector.apply_sobel()
    #edge_detector.save_image(sobel_edges)
    
    laplacian_edges = edge_detector.apply_laplacian()
    #edge_detector.save_image(laplacian_edges)
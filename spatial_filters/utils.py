import cv2
import numpy

def get_image(image_path: str) -> numpy.ndarray:
    image = cv2.imread(image_path)
    return image.astype(int)

def save_image(image: numpy.ndarray, save_location: str) -> None:
    image = image.astype(numpy.uint8)
    cv2.imwrite(save_location, image)
import numpy as np
import cv2

def __get_image(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    return image.astype(int)

def __save_image(image: np.ndarray, save_location: str) -> None:
    image = image.astype(np.uint8)
    cv2.imwrite(save_location, image)

def negative_filter(image: np.ndarray, *_: None) -> np.ndarray:
    transformed_image = 255 - image
    return transformed_image
    
def gamma_correction_filter(image: np.ndarray, gamma) -> np.ndarray:
    transformed_image = (image / 255) ** float(gamma) * 255
    clipped_image = transformed_image.clip(0, 255)
    return clipped_image
    
filter_names = {
    "negative": negative_filter, 
    "gamma": gamma_correction_filter,
}

def apply_filter(name: str, image_path: str, output_path: str, *args):
    image = __get_image(image_path)
    output_image = filter_names[name](image, *args)
    __save_image(output_image, output_path)
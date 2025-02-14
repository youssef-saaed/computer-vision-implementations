from .utils import * 
import numpy as np

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
    image = get_image(image_path)
    output_image = filter_names[name](image, *args)
    save_image(output_image, output_path)
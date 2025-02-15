import numpy as np
from collections import defaultdict
from typing import Any
import cv2
from copy import deepcopy
import matplotlib.pyplot as plt

def __get_image(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    return image.astype(int)

def __save_image(image: np.ndarray, save_location: str) -> None:
    image = image.astype(np.uint8)
    cv2.imwrite(save_location, image)
    
def freq_dict_increment(dict: defaultdict, key: Any) -> None:
    dict[key] += 1

def add_padding(image: np.ndarray, padding_size: int) -> np.ndarray:
    padded_image_shape = (image.shape[0] + 2 * padding_size, image.shape[1] + 2 * padding_size, image.shape[2])
    padded_image = np.zeros(padded_image_shape, dtype=int)
    padded_image[padding_size: -padding_size, padding_size: -padding_size, :] = image[:, :, :]
    return padded_image

def apply_3d_convolution(image: np.ndarray, filter: np.ndarray) -> np.ndarray:
    if filter.shape[0] != filter.shape[1] or filter.shape[0] % 2 == 0:
        return image
    
    padding_size = (filter.shape[0] - 1) // 2
    padded_image = add_padding(image, padding_size)
    
    for i in range(padding_size, padded_image.shape[0] - padding_size):
        for j in range(padding_size, padded_image.shape[1] - padding_size):
            window_start_x = j - padding_size
            window_end_x = j + padding_size + 1
            window_start_y = i - padding_size
            window_end_y = i + padding_size + 1
            
            window = padded_image[window_start_y : window_end_y, window_start_x : window_end_x]
            for c in range(padded_image.shape[2]):
                image[i - padding_size, j - padding_size, c] = np.multiply(window[:, :, c], filter).sum()
    return image



def negative_filter(image: np.ndarray, *_: None) -> np.ndarray:
    transformed_image = 255 - image
    return transformed_image
    
def gamma_correction_filter(image: np.ndarray, gamma: Any) -> np.ndarray:
    transformed_image = (image / 255) ** float(gamma) * 255
    clipped_image = transformed_image.clip(0, 255)
    return clipped_image

def histogram_equalizer_filter(image: np.ndarray, alpha: Any = 1) -> np.ndarray:
    alpha = float(alpha)
    
    freq = [defaultdict(int), defaultdict(int), defaultdict(int)]
    
    for i in range(3):
        np.vectorize(lambda val: freq_dict_increment(freq[i], val))(image[:, :, i])
    
    mapping = [{}, {}, {}]
    cumulative_prob = [0, 0, 0]
    for i in range(256):
        for j in range(3):
            freq[j][i] /= image.shape[0] * image.shape[1]
            cumulative_prob[j] += freq[j][i]
            mapping[j][i] = cumulative_prob[j] * 255
    
    equalized_image = deepcopy(image)
    for i in range(3):
        equalized_image[:, :, i] = np.vectorize(lambda val: mapping[i][val])(image[:, :, i])
    
    return (1 - alpha) * image + alpha * equalized_image

def average_filter(image: np.ndarray, kernel_size: Any):
    kernel_size = int(kernel_size)
    filter = np.full((kernel_size, kernel_size), 1 / kernel_size ** 2)
    return apply_3d_convolution(image, filter)
        
    
    
filter_names = {
    "negative": negative_filter, 
    "gamma": gamma_correction_filter,
    "histeq": histogram_equalizer_filter,
    "average": average_filter,
}

def apply_filter(name: str, image_path: str, output_path: str, *args):
    image = __get_image(image_path)
    output_image = filter_names[name](image, *args)
    __save_image(output_image, output_path)
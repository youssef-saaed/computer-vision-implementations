import numpy as np
from collections import defaultdict
from typing import Any
import cv2
from copy import deepcopy

def __get_image(image_path: str) -> np.ndarray:
    """Load an image from the given path and convert it to int type."""
    image = cv2.imread(image_path)
    return image.astype(int)

def __save_image(image: np.ndarray, save_location: str) -> None:
    """Save an image to the given path after converting it to uint8."""
    image = image.astype(np.uint8)
    cv2.imwrite(save_location, image)

def freq_dict_increment(dict: defaultdict, key: Any) -> None:
    """Increment the frequency count of a given key in a defaultdict."""
    dict[key] += 1

def add_padding(image: np.ndarray, padding_size: int) -> np.ndarray:
    """Pad an image with zeros to maintain dimensions after filtering."""
    padded_image_shape = (image.shape[0] + 2 * padding_size, image.shape[1] + 2 * padding_size, image.shape[2])
    padded_image = np.zeros(padded_image_shape, dtype=int)
    padded_image[padding_size: -padding_size, padding_size: -padding_size, :] = image[:, :, :]
    return padded_image

def apply_3d_convolution(image: np.ndarray, filter: np.ndarray) -> np.ndarray:
    """Apply a 3D convolution filter to an image."""
    if filter.shape[0] != filter.shape[1] or filter.shape[0] % 2 == 0:
        return image  # Ensure filter is square and has an odd size
    
    padding_size = (filter.shape[0] - 1) // 2
    padded_image = add_padding(image, padding_size)
    
    # Use stride tricks for efficient window extraction
    windows = np.lib.stride_tricks.sliding_window_view(padded_image, filter.shape, axis=(0, 1))
    image = np.sum(windows * filter, axis=(-1, -2))
    return image



def negative_filter(image: np.ndarray, *_: None) -> np.ndarray:
    """Apply a negative filter to invert image colors."""
    return 255 - image

def gamma_correction_filter(image: np.ndarray, gamma: Any) -> np.ndarray:
    """Apply gamma correction to enhance brightness or contrast."""
    transformed_image = (image / 255) ** float(gamma) * 255
    return transformed_image.clip(0, 255)

def histogram_equalizer_filter(image: np.ndarray, alpha: Any = 1) -> np.ndarray:
    """Perform histogram equalization to improve contrast."""
    alpha = float(alpha)
    freq = [defaultdict(int), defaultdict(int), defaultdict(int)]
    
    # Compute pixel intensity frequencies for each channel
    for i in range(3):
        np.vectorize(lambda val: freq_dict_increment(freq[i], val))(image[:, :, i])
    
    # Compute cumulative distribution function (CDF) mapping
    mapping = [{}, {}, {}]
    cumulative_prob = [0, 0, 0]
    for i in range(256):
        for j in range(3):
            freq[j][i] /= image.shape[0] * image.shape[1]
            cumulative_prob[j] += freq[j][i]
            mapping[j][i] = cumulative_prob[j] * 255
    
    # Apply mapping to equalize the histogram
    equalized_image = deepcopy(image)
    for i in range(3):
        equalized_image[:, :, i] = np.vectorize(lambda val: mapping[i][val])(image[:, :, i])
    
    return (1 - alpha) * image + alpha * equalized_image

def average_filter(image: np.ndarray, kernel_size: Any) -> np.ndarray:
    """Apply an average (mean) filter for noise reduction."""
    kernel_size = int(kernel_size)
    filter = np.full((kernel_size, kernel_size), 1 / kernel_size ** 2)
    return apply_3d_convolution(image, filter)

def median_filter(image: np.ndarray, kernel_size: Any) -> np.ndarray:
    """Apply a median filter to remove noise while preserving edges."""
    kernel_size = int(kernel_size)
    if kernel_size % 2 == 0:
        return image  # Ensure odd-sized kernel
    
    padding_size = (kernel_size - 1) // 2
    padded_image = add_padding(image, padding_size)
    
    # Apply median filter to each pixel
    windows = np.lib.stride_tricks.sliding_window_view(padded_image, (kernel_size, kernel_size), axis=(0, 1))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for c in range(image.shape[2]):
                image[i, j, c] = np.sort(windows[i, j, c].reshape(-1))[padding_size]
    return image

def edge_detection_filter(image: np.ndarray, *_: None) -> np.ndarray:
    """Apply edge detection using a Laplacian kernel."""
    smoothed_image = average_filter(image, 3) 
    filter = np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1],
    ])
    return apply_3d_convolution(smoothed_image, filter)

def sharpening_filter(image: np.ndarray, intensity: Any = 0.3) -> np.ndarray:
    """Apply sharpening by enhancing detected edges."""
    intensity = float(intensity)
    edge_image = edge_detection_filter(image).clip(0, 255)  
    return (image + intensity * edge_image).clip(0, 255) 



# Dictionary of available filters
filter_names = {
    "negative": negative_filter, 
    "gamma": gamma_correction_filter,
    "histeq": histogram_equalizer_filter,
    "average": average_filter,
    "median": median_filter,
    "edge": edge_detection_filter,
    "sharp": sharpening_filter,
}

def apply_filter(name: str, image_path: str, output_path: str, *args):
    """Apply a selected filter to an image and save the result."""
    image = __get_image(image_path)
    output_image = filter_names[name](image, *args)
    __save_image(output_image, output_path)
    
def print_available_filters():
    """Displays available filters and their expected arguments."""
    print("Available filters and their arguments:")
    print("negative              -> No arguments")
    print("gamma [gamma]        -> Gamma correction factor (float)")
    print("histeq [alpha]       -> Histogram equalization weight (float, default=1)")
    print("average [kernel]     -> Kernel size for average filtering (odd int)")
    print("median [kernel]      -> Kernel size for median filtering (odd int)")
    print("edge                 -> No arguments (applies edge detection)")
    print("sharp [intensity]    -> Sharpening intensity (float, default=0.1)")

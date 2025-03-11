import numpy as np
import copy

# Defining Corners Hit and Miss Structure elements
__LEFT_TOP_CORNER = np.array([
    [0, 0, 0, 0, 0],
    [0, 2, 2, 2, 2],
    [0, 2, 1, 1, 1],
    [0, 2, 1, 0, 0],
    [0, 2, 1, 0, 0],        
])
__RIGHT_TOP_CORNER = np.array([
    [0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0],
    [1, 1, 1, 2, 0],
    [0, 0, 1, 2, 0],
    [0, 0, 1, 2, 0],        
])
__LEFT_BOTTOM_CORNER = np.array([
    [0, 2, 1, 0, 0],
    [0, 2, 1, 0, 0],
    [0, 2, 1, 1, 1],
    [0, 2, 2, 2, 2],
    [0, 0, 0, 0, 0],        
])
__RIGHT_BOTTOM_CORNER = np.array([
    [0, 0, 1, 2, 0],
    [0, 0, 1, 2, 0],
    [1, 1, 1, 2, 0],
    [2, 2, 2, 2, 0],
    [0, 0, 0, 0, 0],        
])

def __checker(image: np.ndarray, structure_element: np.ndarray, check_origin: bool) -> str:
    if image.dtype != np.uint8 or structure_element.dtype != np.uint8: # Check that both data type are 8-bit unsigned int
        return "Input should be in numpy.uint8 datatype"
    if len(image.shape) != 2 or len(structure_element.shape) != 2: # Check that both are 2D array
        return "Invalid image or structure element shape"
    if structure_element.shape[0] > image.shape[0] or structure_element.shape[1] > image.shape[1]: # Check that structure element fits inside the image
        return "Structure element is bigger than the image"
    if structure_element.shape[0] % 2 == 0 or structure_element.shape[1] % 2 == 0: # Check if the structure element size is odd
        return "This is a simple implementation that require odd structure element width and height"
    se_shape = structure_element.shape
    if check_origin and not structure_element[se_shape[0] // 2, se_shape[1] // 2]: # Check that structure element center is one
        return "This is a simple implementation that require to have 1 in the middle of structure element in dilation mode"
    return ""

def binarize(image: np.ndarray, threshold: int | float, invert: bool = False) -> np.ndarray: 
    if not invert:
        return (image > threshold).astype(np.uint8) # Binarize and Invert
    return (image < threshold).astype(np.uint8) # Binarize only

def dilate(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray:
    check_msg = __checker(image, structure_element, True)
    if check_msg:
        raise Exception(check_msg)
    
    N, M = image.shape
    n, m = structure_element.shape
    
    dilated_image = np.zeros((N + n - 1, M + m - 1), dtype=np.uint8)
    
    # Looping over each pixel in the image and if the pixel is high the high pixels in structure element is put in the dilated image
    for i in range(N):
        for j in range(M):
            dilated_image[i : i + n, j : j + m] |= image[i, j] & structure_element 
    
    return dilated_image

def erode(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray:
    check_msg = __checker(image, structure_element, False)
    if check_msg:
        raise Exception(check_msg)
    
    N, M = image.shape
    n, m = structure_element.shape
    
    eroded_image = np.zeros((N - n + 1, M - m + 1), dtype=np.uint8)
    
    # Looping over windows in the image and if not all high pixels of structure element is high in the image make this pixel low in eroded image
    for i in range(n // 2, N - n // 2):
        for j in range(m // 2, M - m // 2):
            # Window start and end in x and y
            y_1 = i - n // 2 
            y_2 = i + n // 2
            x_1 = j - m // 2
            x_2 = j + m // 2
            
            eroded_image[y_1, x_1] = not np.any(image[y_1 : y_2 + 1, x_1 : x_2 + 1] & structure_element ^ structure_element)
            
    return eroded_image

def opening(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray:
    eroded_image = erode(image, structure_element)
    dilated_image = dilate(eroded_image, structure_element)
    return dilated_image

def closing(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray:
    dilated_image = dilate(image, structure_element)
    eroded_image = erode(dilated_image, structure_element)
    return eroded_image
    
def hit_and_miss(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray:
    border_structure_element = (structure_element == 2).astype(np.uint8) # Extract border structure element
    structure_element = (structure_element == 1).astype(np.uint8) # Extract foreground structure element
    
    background = (1 - image) if image.max() <= 1 else (255 - image)
    eroded_foreground = erode(image, structure_element) 
    eroded_background = erode(background, border_structure_element)
    
    return eroded_background & eroded_foreground # Intersection between eroded background and foreground

def corner_detection(image: np.ndarray) -> np.ndarray:
    if image.shape[0] < 5 or image.shape[1] < 5:
        return image
    
    corners = hit_and_miss(image, __LEFT_TOP_CORNER)
    corners |= hit_and_miss(image, __RIGHT_TOP_CORNER)
    corners |= hit_and_miss(image, __LEFT_BOTTOM_CORNER)
    corners |= hit_and_miss(image, __RIGHT_BOTTOM_CORNER)
    return corners

def extract_boundaries(image: np.ndarray) -> np.ndarray:
    if image.shape[0] < 3 or image.shape[1] < 3:
        return image
    image = copy.deepcopy(image)
    structure_element = np.ones((3, 3), dtype=np.uint8)
    eroded_img = erode(image, structure_element)
    image[1:-1, 1:-1] = image[1:-1, 1:-1] - eroded_img # Difference between original image and eroded image
    return image
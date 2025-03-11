# Morphological Operations and Transformations

## Description
This is my implementation for fundamental morphological operations used in image processing, including dilation, erosion, opening, closing, hit-and-miss transformation, corner detection, and boundary extraction. These operations help analyze and manipulate binary images by modifying their structures.

## API Summary
### Functions:
- `binarize(image: np.ndarray, threshold: int | float, invert: bool = False) -> np.ndarray`
  - Converts an image into a binary format based on a threshold.
- `dilate(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray`
  - Expands bright regions by spreading high values according to the structuring element.
- `erode(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray`
  - Shrinks bright regions by ensuring all pixels under the structure element match.
- `opening(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray`
  - Performs erosion followed by dilation to remove small noise.
- `closing(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray`
  - Performs dilation followed by erosion to fill small holes.
- `hit_and_miss(image: np.ndarray, structure_element: np.ndarray) -> np.ndarray`
  - Detects specific patterns using erosion on foreground and background.
- `corner_detection(image: np.ndarray) -> np.ndarray`
  - Identifies corners in an image using predefined structure elements.
- `extract_boundaries(image: np.ndarray) -> np.ndarray`
  - Extracts object boundaries by subtracting the eroded image from the original.

## Example
```python
import numpy as np
from morphological_operations import binarize, dilate, erode, opening, closing, corner_detection, extract_boundaries

# Sample binary image
image = np.array([
    [0, 0, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0],
], dtype=np.uint8)

# Define a simple structuring element
structuring_element = np.ones((3, 3), dtype=np.uint8)

# Apply morphological operations
binary_img = binarize(image, threshold=0.5)
dilated_img = dilate(binary_img, structuring_element)
eroded_img = erode(binary_img, structuring_element)
opened_img = opening(binary_img, structuring_element)
closed_img = closing(binary_img, structuring_element)
corners = corner_detection(binary_img)
boundaries = extract_boundaries(binary_img)
```

## Dependencies
- Python 3.x
- NumPy

## Limitations
- Structuring elements must have **odd** dimensions.
- The hit-and-miss transform relies on predefined corner structures, limiting its flexibility for detecting arbitrary shapes.
- Input images must be **2D numpy arrays** with values of `0` and `1` (binary images).

## Notes
- The `corner_detection` function detects only specific corner types based on predefined structuring elements.
- The `hit_and_miss` function uses `2`s in the structuring element to represent the background, which may need adjustments for different applications.
- This implementation assumes binary images (0 and 1); grayscale images should be binarized first using the `binarize` function.


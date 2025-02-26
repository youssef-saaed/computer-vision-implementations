# Image Filtering Utility

## Overview
This project provides an image filtering utility that applies various spatial filters to images. The filtering operations include common image processing techniques such as sharpening, edge detection, histogram equalization, and more. The implementation is done using NumPy and OpenCV.

## Features
- Apply a variety of image filters to enhance or process images.
- Supports multiple filters, including negative transformation, gamma correction, and convolution-based filters.
- Efficient padding and convolution techniques using NumPy.
- Command-line interface for easy usage.

## Included Filters
| Filter Name | Description | Arguments |
|------------|-------------|-----------|
| `negative` | Inverts the image colors. | None |
| `gamma` | Adjusts brightness and contrast using gamma correction. | `gamma` (float) |
| `histeq` | Enhances contrast using histogram equalization. | `alpha` (float, default=1) |
| `average` | Applies an average filter for noise reduction. | `kernel_size` (odd int) |
| `median` | Applies a median filter to remove noise while preserving edges. | `kernel_size` (odd int) |
| `edge` | Detects edges using a Laplacian kernel. | None |
| `sharp` | Enhances edges for sharpening effect. | `intensity` (float, default=0.3) |

## Installation
Ensure you have Python installed along with the necessary dependencies:
```sh
pip install numpy opencv-python
```

## Usage
Run the script via the command line:
```sh
python runner.py [Filter Name] [Image File Name] [Filter Arguments]
```

### Example Usage
- Apply a negative filter:
  ```sh
  python runner.py negative image.jpg
  ```
- Apply gamma correction with `gamma=2.2`:
  ```sh
  python runner.py gamma image.jpg 2.2
  ```
- Apply histogram equalization with `alpha=0.8`:
  ```sh
  python runner.py histeq image.jpg 0.8
  ```
- Apply an average filter with a 5x5 kernel:
  ```sh
  python runner.py average image.jpg 5
  ```
- Apply edge detection:
  ```sh
  python runner.py edge image.jpg
  ```

## Directory Structure
```
project_root/
│-- filters.py       # Contains all filter implementations
│-- runner.py        # CLI script to apply filters
│-- input/           # Folder to store input images
│-- output/          # Folder to store processed images
│-- README.md        # Documentation file
```

## Notes
- The input images should be placed inside the `input/` directory.
- The output images will be saved inside the `output/` directory with the same filename as input.
- Kernel size for average and median filters must be an odd integer.
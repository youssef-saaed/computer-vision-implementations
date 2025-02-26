# Frequency Domain Filtering

## Description
This is my implementation of frequency domain filtering from scratch. The goal is to gain a deep understanding of how filtering works in the frequency domain by manually implementing the Fourier Transform, Inverse Fourier Transform, and various filtering techniques. The implementation does not use optimized FFT algorithms but instead follows the standard Fourier Transform process.

## API Usage

### Running the Script
To apply a filter to an image, use the `runner.py` script with the following command:

```bash
python runner.py [input] [output] [type] [method] [distance 1] [distance 2 (optional)]
```

### Arguments
- `input`: Name of the image in the `input` folder.
- `output`: Name of the processed image to be saved in the `output` folder.
- `type`: The type of filtering to be applied. Available options:
  - `low-pass`
  - `high-pass`
  - `band-pass`
  - `band-stop`
- `method`: The filtering method to be used. Available options:
  - `ideal`
  - `gaussian`
  - `butterworth`
- `distance 1`: Threshold for low-pass and high-pass filters or starting distance for band-pass and band-stop filters.
- `distance 2` (optional): Ending distance for band-pass and band-stop filters.

### Example Usage
To apply a Gaussian low-pass filter with a threshold of 50:
```bash
python runner.py input.jpg output.jpg low-pass gaussian 50
```
To apply a Butterworth band-pass filter with thresholds 30 and 80:
```bash
python runner.py input.jpg output.jpg band-pass butterworth 30 80
```

## Limitations
- This implementation uses the regular Fourier Transform rather than an optimized Fast Fourier Transform (FFT), making it computationally expensive.
- **Do not try images larger than 100x100 pixels**, as processing larger images will be extremely slow.

## Dependencies
- Python 3
- NumPy
- OpenCV (cv2)

To install the required dependencies, run:
```bash
pip install numpy opencv-python
```

## Notes
This implementation was built as a learning exercise to understand frequency domain filtering fully. While it works, optimized implementations using FFT are recommended for practical use.


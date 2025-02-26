import numpy as np
import cv2

def shift_image(image: np.ndarray) -> np.ndarray:
    mask = np.ones(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (i + j) % 2:
                mask[i][j] *= -1
    return image * mask
    

def fourier_transform(image: np.ndarray) -> np.ndarray:
    N, M = image.shape[:2]
    
    x = np.arange(N).reshape((N, 1))
    y = np.arange(M).reshape((1, M))
    
    image = shift_image(image)
    
    frequency_img = np.zeros(image.shape, dtype=complex)
    
    for u in range(N):
        for v in range(M):
            theta = 2 * np.pi * (u * x / N + v * y / M)
            frequency_img[u][v] = np.sum(image * np.exp(-1j * theta))
    
    return frequency_img / (N * M)

def inverse_fourier_transform(frequencies: np.ndarray) -> np.ndarray:
    N, M = frequencies.shape[:2]
    
    x = np.arange(N).reshape((N, 1))
    y = np.arange(M).reshape((1, M))
    
    image = np.zeros(frequencies.shape, dtype=int)
    
    for i in range(N):
        for j in range(M):
            theta = 2 * np.pi * (i * x / N + j * y / M)
            image[i][j] = np.real(np.sum(frequencies * np.exp(1j * theta)))
    
    return np.clip(shift_image(image), 0, 255).astype(np.uint8)



def generic_filter(frequencies: np.ndarray, solver: str, band_type: str, d0: int = 60, d1: int = 1000, order: int = 2) -> np.ndarray:
    available_solvers = ["ideal", "guassian", "butterworth"]
    available_band_types = ["low-pass", "high-pass", "band-pass", "band-stop"]
    
    if solver not in available_solvers:
        raise AssertionError("Solver is not found. Available solvers:", *available_solvers)
    if band_type not in available_band_types:
        raise AssertionError("Band type is not found. Available band types:", *available_band_types)   
    if d0 >= d1:
        raise AssertionError("d0 should be strictly less than d1")
    
    mask = np.zeros(frequencies.shape, dtype=complex) 
    N, M = frequencies.shape[:2]
    center = (N / 2, M / 2)
    
    for u in range(N):
        for v in range(M):
            d = ((u - center[0]) ** 2 + (v - center[1]) ** 2) ** 0.5
            if band_type == "low-pass":
                if solver == "ideal":
                    mask[u, v] = 1 if d <= d0 else 0
                elif solver == "guassian":
                    mask[u, v] = np.exp(-d ** 2 / (2 * d0 ** 2))
                elif solver == "butterworth":
                    mask[u, v] = 1 / (1 + (d / d0) ** (2 * order))
            elif band_type == "high-pass":
                if solver == "ideal":
                    mask[u, v] = 1 if d >= d0 else 0
                elif solver == "guassian":
                    mask[u, v] = 1 - np.exp(-d ** 2 / (2 * d0 ** 2))
                elif solver == "butterworth":
                    mask[u, v] = 1 - 1 / (1 + (d / d0) ** (2 * order))
            elif band_type == "band-pass":
                if solver == "ideal":
                    mask[u, v] = 1 if d >= d0 and d <= d1 else 0
                elif solver == "guassian":
                    mask[u, v] = min(1 - np.exp(-d ** 2 / (2 * d0 ** 2)), np.exp(-d ** 2 / (2 * d1 ** 2)))
                elif solver == "butterworth":
                    mask[u, v] = min(1 - 1 / (1 + (d / d0) ** (2 * order)), 1 / (1 + (d / d1) ** (2 * order)))
            elif band_type == "band-stop":
                if solver == "ideal":
                    mask[u, v] = 1 if d <= d0 or d >= d1 else 0
                elif solver == "guassian":
                    mask[u, v] = max(np.exp(-d ** 2 / (2 * d0 ** 2)), 1 - np.exp(-d ** 2 / (2 * d1 ** 2)))
                elif solver == "butterworth":
                    mask[u, v] = max(1 / (1 + (d / d0) ** (2 * order)), 1 - 1 / (1 + (d / d1) ** (2 * order)))
        
    return mask * frequencies

def read_image(filepath: str) -> np.ndarray:
    img = cv2.imread(filepath)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_filter(image: np.ndarray, solver: str, band_type: str, d0: int, d1: int) -> np.ndarray:
    frequencies = fourier_transform(image)
    filtered_frequencies = generic_filter(frequencies, solver, band_type, d0, d1)
    return inverse_fourier_transform(filtered_frequencies)

def save_image(image: np.ndarray, dest: str) -> None:
    cv2.imwrite(dest, image)
            
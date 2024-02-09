import cv2
import numpy as np
def adjust_brightness_contrast(img, brightness=0, contrast=100):
    """
    Adjusts the brightness and contrast of an image.
    brightness: Int value [-100, 100]
    contrast: Int value [0, 300], where 100 means no change
    """
    alpha = float(contrast) / 100
    beta = brightness
    adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return adjusted_img

def resize_image(image, scale_percent=50):
    """
    Resizes an image by a given percentage.
    scale_percent: Percentage to resize by
    """
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

def edgeDetection(image, blur_kernel_size, edge_param1, edge_param2):
    """
    Preprocesses an image with resizing, brightness/contrast adjustment, Gaussian blurring, and Canny edge detection.
    """
    img = cv2.GaussianBlur(image, (blur_kernel_size, blur_kernel_size), 0)
    edges = cv2.Canny(img, edge_param1, edge_param2)
    return edges
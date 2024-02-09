import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_processing import *
def rotate_image(image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        return rotated
def rotate_image_automatic(image):
    def preprocessing(image):
        scale_percent = 50  # Image resize percentage for viewing convenience. 
        #   - outer board circle 50
        #   - inner board circle 50
                            # Range: 1-100. Lower values reduce the image size, speeding up processing but may lose details.
        blur_kernel_size = 25  # Size of the Gaussian blur kernel. Must be an odd number. 
        #   - outer board circle 15
        #   - inner board circle 15
                            # Range: Typically 1-21. Larger values increase the blur effect, smoothing out more noise but can blur edges.

        edge_param1 = 100  # First threshold for the Canny edge detector. 
        #   - outer board circle 0
        #   - inner board circle 0
                        # Range: 0-255. Lower values detect more edges, including false positives.

        edge_param2 = 40  # Second threshold for the Canny edge detector. 
        #   - outer board circle 255
        #   - inner board circle 100
                        # Range: 0-255. Values typically 2-3 times edge_param1. Higher values reduce detection of weaker edges.

        brightness_factor = 0  # Brightness adjustment. 
        #   - outer board circle 50
        #   - inner board circle 0
                                # Range: -100 (darker) to 100 (brighter). 0 means no change.

        contrast_factor = 100  # Contrast adjustment. 
        #   - outer board circle 100
        #   - inner board circle 100
                            # Range: 0-300, where 100 means no change. Values >100 increase contrast, <100 decrease contrast.


        # Preprocess the image
        resizedImage = resize_image(image, scale_percent)
        brightImage = adjust_brightness_contrast(resizedImage, brightness_factor, contrast_factor)

        processed_img = edgeDetection(brightImage, blur_kernel_size, edge_param1, edge_param2)
        processed_img = cv2.Canny(processed_img, 50, 150, apertureSize=3)
        # Use Hough Line Transform to find lines
        
        return processed_img

    def get_angle(lines):
        unique_lines = []
        seen_theta = set()
        
        if lines is not None:
            for rho, theta in lines[:, 0]:
                degrees = np.rad2deg(theta)
                # Check for unique theta within specified range
                if ((0 <= degrees <= 18) or (162 <= degrees <= 180)) and degrees not in seen_theta:
                    seen_theta.add(degrees)  # Mark this theta as seen
                    unique_lines.append([rho, theta])  # Add unique line to the list

        
        if unique_lines:
            unique_lines = np.array(unique_lines, dtype=np.float32).reshape(-1, 1, 2)
        # Calculate the average angle of the lines
        angles = []
        for rho, theta in unique_lines[:, 0]:
            degrees = np.rad2deg(theta)
            if (0 <= degrees <= 18) or (162 <= degrees <= 180):
                angles.append(degrees if degrees <= 90 else degrees - 180)  # Adjust angles > 90 to negative to average correctly
                
        if angles:
            
            avg_angle = sum(angles) / len(angles)
            print(avg_angle)
            return avg_angle  # Make sure to return the negative of the average angle for correct rotation direction
        return 0

        
        
    processed_img = preprocessing(image)
    lines = cv2.HoughLines(processed_img, 1, np.pi / 180, 300)
    lines = cv2.HoughLines(processed_img, 1, np.pi / 180, 220)
    angle = get_angle(lines)
    
    return angle

if __name__ == "__main__": # Usage example
    # Load image
    image = cv2.imread("scanned_form_rotate.jpg")
    image = rotate_image(image, -10)

    plt.imshow(image)
    plt.show()
    anlge = rotate_image_automatic(image)
    rotated_img = rotate_image(image, anlge)

    plt.imshow(rotated_img)
    plt.show()
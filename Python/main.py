import cv2
from db import save_score, get_scores
from image_process import warpDartboard, rotateDartboard
from score_calculator import calculate_score
def main():
    # Placeholder for image capture logic
    perfectDartboard = cv2.imread("dartboard.png")
    emptyDartboard = example_dart = cv2.imread("real_dartboard.jpg")
    dartboardWithDart = cv2.imread("example_dart-3.jpg")


    warpedEmptyDartboard, harmongraphy, height, width = warpDartboard.warp_image_empty(perfectDartboard, emptyDartboard)
    
    warpedDartboardwithDart = warpDartboard.warp_image(dartboardWithDart, harmongraphy, height, width)
    
    
    
    # Main application logic
    # - Process image
    # - Calculate score
    # - Save score to DB
    pass

if __name__ == "__main__":
    main()

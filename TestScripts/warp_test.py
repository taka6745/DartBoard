import cv2
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Image
import sys
sys.path.append('C:\\Users\\lukey\\OneDrive\\Documents\\Darts\\Dartboard\\Python')
sys.path.append('C:\\Users\\lukey\\OneDrive\\Documents\\Darts\\Dartboard\\')

from image_initialiser import *
from TestData import *

frontal_board = cv2.imread("C:\\Users\\lukey\\OneDrive\\Documents\\Darts\\Dartboard\\dartboard.png")
tilted_board = cv2.imread("C:\\Users\\lukey\\OneDrive\\Documents\\Darts\\Dartboard\\real_dartboard.png")

homography = warp_homography(frontal_board, tilted_board)

warp_image(frontal_board, tilted_board, homography)
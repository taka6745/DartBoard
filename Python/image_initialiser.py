import cv2
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Image

def warp_homography(frontal_board, tilted_board):

    #Find features of each grayscale image
    keypoints1, descriptors1, keypoints2, descriptors2 = ascertain_features(500, frontal_board, tilted_board)
    #display_features(keypoints1, keypoints2, frontal_board, tilted_board)

    #Match features
    matches = match_features(descriptors1, descriptors2)

    #Extract location of good matches and find homography
    homography = find_homography(matches, keypoints1, keypoints2)
    return homography

def ascertain_features(max_features, frontal_board, tilted_board):
    orb = cv2.ORB_create(max_features)
    keypoints1, descriptors1 = orb.detectAndCompute(frontal_board, None)
    keypoints2, descriptors2 = orb.detectAndCompute(tilted_board, None)
    return keypoints1, descriptors1, keypoints2, descriptors2


def display_features(keypoints1, keypoints2, frontal_board, tilted_board):

    dart_display = cv2.drawKeypoints(frontal_board, keypoints1, outImage=np.array([]), color = (255, 0, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    dart_tilt_display = cv2.drawKeypoints(tilted_board, keypoints2, outImage=np.array([]), color = (255, 0, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    plt.figure(figsize=[20,10])
    plt.subplot(121); plt.axis('off'); plt.imshow(dart_display); plt.title("Original Form");
    plt.subplot(122); plt.axis('off'); plt.imshow(dart_tilt_display); plt.title("Scanned Form");
    plt.show()

def match_features(descriptors1, descriptors2):

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

    # Converting to list for sorting as tuples are immutable objects.
    matches = list(matcher.match(descriptors1, descriptors2, None))

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * 0.1)
    matches = matches[:numGoodMatches]
    return matches

def draw_matches(keypoints1, keypoints2, matches, frontal_board, tilted_board):
    # Draw top matches
    im_matches = cv2.drawMatches(frontal_board, keypoints1, tilted_board, keypoints2, matches, None)

    plt.figure(figsize=[40, 10])
    plt.imshow(im_matches);plt.axis("off");plt.title("Original Form")

def find_homography(matches, keypoints1, keypoints2):
    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)
    return h

def warp_image(frontal_board, tilted_board, h):

    height, width, _ = frontal_board.shape
    print(width, height, _, h)
    im2_reg = cv2.warpPerspective(tilted_board, h, (width, height))

    # Display results
    plt.figure(figsize=[20, 10])
    plt.subplot(121);plt.imshow(frontal_board);    plt.axis("off");plt.title("Original Form")
    plt.subplot(122);plt.imshow(im2_reg);plt.axis("off");plt.title("Scanned Form")
    plt.show()
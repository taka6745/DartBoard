import cv2
import numpy as np
import matplotlib.pyplot as plt
"""
Warmp_image_empty
input: faceOnImage, dartboardTilted
output: img_warped, h, height, width

warp_image
input: image, harmonography, dartboardHeight, dartboardWidth
output: img_warped
"""
def warp_image_empty(faceOnImage, dartboardTilted):
    MAX_NUM_FEATURES = 500
    orb = cv2.ORB_create(MAX_NUM_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(faceOnImage, None)
    keypoints2, descriptors2 = orb.detectAndCompute(dartboardTilted, None)

    dart_display = cv2.drawKeypoints(faceOnImage, keypoints1, outImage=np.array([]), color = (255, 0, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    dart_tilt_display = cv2.drawKeypoints(dartboardTilted, keypoints2, outImage=np.array([]), color = (255, 0, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

    # Converting to list for sorting as tuples are immutable objects.
    matches = list(matcher.match(descriptors1, descriptors2, None))

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * 0.1)
    matches = matches[:numGoodMatches]
    # Draw top matches
    im_matches = cv2.drawMatches(faceOnImage, keypoints1, dartboardTilted, keypoints2, matches, None)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)

    # Use homography to warp image
    height, width, _ = faceOnImage.shape
    img_warped = cv2.warpPerspective(dartboardTilted, h, (width, height)) # h is the homography
    return img_warped, h, height, width
    
def warp_image(image, harmonography, dartboardHeight, dartboardWidth):
    # Use homography to warp image
    img_warped = cv2.warpPerspective(image, harmonography, (dartboardWidth, dartboardHeight)) # h is the homography
    return img_warped


if __name__ == "__main__": # Usage example

    faceOnImage = cv2.imread("dartboard.png")
    dartboardTilted = cv2.imread("real_dartboard.png")
    fixed, harmonography, dartboardHeight, dartboardWidth = warp_image_empty(faceOnImage, dartboardTilted)
    
    plt.imshow(fixed)
    plt.show()
    
    example_dart = cv2.imread("example_dart-3.jpg")
    new_image = warp_image(example_dart, harmonography, dartboardHeight, dartboardWidth)
    
    plt.imshow(new_image)
    plt.show()
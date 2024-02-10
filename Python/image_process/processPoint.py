from image_processing import *
from bounding import *
import math
def circleFinder(emptyWarpedRotatedImage):
    scale_percent = 50  
    #   - outer board circle 50
    #   - inner board circle 50

    blur_kernel_size = 21 
    #   - outer board circle 15
    #   - inner board circle 15
                        

    edge_param1 = 100
    #   - outer board circle 0
    #   - inner board circle 0


    edge_param2 = 150
    #   - outer board circle 255
    #   - inner board circle 100
                    

    brightness_factor = -50
    #   - outer board circle 50
    #   - inner board circle 0


    contrast_factor = 200
    #   - outer board circle 100
    #   - inner board circle 100

    # Preprocess the image
    resizedImage = resize_image(emptyWarpedRotatedImage, scale_percent)
    adjustedImage = adjust_brightness_contrast(resizedImage, brightness_factor, contrast_factor)
    processed_img = edgeDetection(adjustedImage, blur_kernel_size, edge_param1, edge_param2)
    
    dpVisual = 1.0
    minDistVisual = 10000000
    minRadiusVisual = 100
    maxRadiusVisual = 10000

    # Assuming 'processed_img' is already defined from previous preprocessing steps
    def detect_circles(processed_img, dp=1.5, minDist=100, minRadius=20, maxRadius=150):
        circles = cv2.HoughCircles(processed_img, cv2.HOUGH_GRADIENT, dp, minDist,
                                param1=50, param2=30, minRadius=minRadius, maxRadius=maxRadius)
        return circles

    # Detect circles
    circles = detect_circles(processed_img, dp=dpVisual, minDist=minDistVisual, minRadius=minRadiusVisual, maxRadius=maxRadiusVisual)
    height, width = processed_img.shape
    return circles, height, width

def scoreFinder(circles, x, y, scale_factor=2):
    if circles is not None and len(circles) > 0:
        # Assuming the first circle is the outer boundary of the dartboard
        circle = circles[0][0]
        center = (int(circle[0] * scale_factor), int(circle[1] * scale_factor))
        radius = int(circle[2] * scale_factor)

        # Calculate the angle from the dart's point to the center of the dartboard
        dx = x - center[0]
        dy = center[1] - y  # Invert dy because y-coordinates increase downwards in image
        angle_rad = math.atan2(dy, dx)

        # Convert angle to degrees and adjust so that 0 degrees is directly up
        angle_deg = math.degrees(angle_rad) % 360
        # Adjust angle to make 0 degrees at the top, in the middle of the 20 sector

        # Calculate sector based on the angle
        sector_angle = 360 / 20
        sector_number = int(angle_deg / sector_angle)
        # Mapping sector number to actual dartboard numbering
        sector_map = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
        sector = sector_map[sector_number]

        return sector
    return None
        

def drawDartboardSectorsAndPoint(img, circles, x, y, scale_factor):
    # Check if at least one circle was detected
    if circles is not None and len(circles) > 0:
        # Assuming the first circle is the outer boundary of the dartboard
        circle = circles[0][0]
        center = (int(circle[0] * scale_factor), int(circle[1] * scale_factor))
        radius = int(circle[2] * scale_factor)

        # Draw the outer circle of the dartboard
        cv2.circle(img, center, radius, (255, 0, 0), thickness=10)

        # Number of sectors on a standard dartboard
        num_sectors = 20
        sector_angle = 360 / num_sectors

        for i in range(num_sectors):
            # Calculate start and end angle for each sector
            start_angle_rad = np.radians(i * sector_angle - sector_angle / 2)  # Adjusting for "20" at the top
            end_angle_rad = np.radians((i + 1) * sector_angle - sector_angle / 2)

            # Calculate start and end points for each sector line
            start_point = (int(center[0] + radius * np.cos(start_angle_rad)), int(center[1] - radius * np.sin(start_angle_rad)))
            end_point = (int(center[0] + radius * np.cos(end_angle_rad)), int(center[1] - radius * np.sin(end_angle_rad)))

            # Draw line for each sector
            cv2.line(img, center, start_point, (0, 255, 255), thickness=2)
            cv2.line(img, center, end_point, (0, 255, 255), thickness=2)

            # Fill each sector with color (alternating for visibility)
            if i % 2 == 0:
                cv2.fillPoly(img, [np.array([center, start_point, end_point], np.int32)], (0, 255, 0))
            else:
                cv2.fillPoly(img, [np.array([center, start_point, end_point], np.int32)], (0, 0, 255))

        # Scale and mark the specified point
        point_scaled = (int(x), int(y))
        cv2.circle(img, point_scaled, 10, (0, 0, 0), -1)  # Black dot

    return img


if __name__ == "__main__":
    # Load images
    perfectDartboard = cv2.imread("dartboard.png")
    emptyDartboard = cv2.imread("real_dartboard.png")

    # dartboardWithDart = cv2.imread("./images/3.png")
    # dartboardWith2Darts = cv2.imread("./images/4.png")

    dartboardWithDart = cv2.imread("real_dartboard.png")
    dartboardWith2Darts = cv2.imread("./images/3.png")

    # Warp images
    warpedEmptyDartboard, homography, height, width = warp_image_empty(perfectDartboard, emptyDartboard)
    warpedDartboardwithDart = warp_image(dartboardWithDart, homography, height, width)
    warpeddartboardWith2Darts = warp_image(dartboardWith2Darts, homography, height, width)
    # Rotate images
    angle = rotate_image_automatic(warpedDartboardwithDart)
    rotatedDartboardWithDart = rotate_image(warpedDartboardwithDart, angle)
    rotatedDartboardEmpty = rotate_image(warpedEmptyDartboard, angle)
    rotated2Darts = rotate_image(warpeddartboardWith2Darts, angle)
    con = dartDetector(rotated2Darts, rotatedDartboardWithDart)



    # Find the minimum enclosing triangle
    triangle_vertices = find_min_enclosing_triangle(con)
    # Draw the minimum enclosing triangle on the image
    point = find_triangle_point(triangle_vertices)
    #convert point to normal array
    point = point[0]
    circles, height, width = circleFinder(rotatedDartboardEmpty)
    drawDartboardSectorsAndPoint(rotatedDartboardEmpty,circles, point[0], point[1], 2)
    print(scoreFinder(circles, point[0], point[1]))
    # Show the result
    plt.imshow(cv2.cvtColor(rotatedDartboardEmpty, cv2.COLOR_BGR2RGB))
    plt.title("Detected Circles on Dartboard")
    plt.axis("off")
    plt.show()
    
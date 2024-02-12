# Compute absolute difference between the two images
difference = cv2.absdiff(currentImage, previousImage)

# Threshold the difference to get a binary mask of the darts
_, mask = cv2.threshold(difference, 150, 255, cv2.THRESH_BINARY)

# Apply morphological operations to clean up the mask
kernel = np.ones((3, 3), np.uint8)
mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

# Convert the mask to the correct type if necessary
mask_cleaned = mask_cleaned.astype(np.uint8)
# Ensure mask_cleaned is a single-channel, 8-bit image
if mask_cleaned.dtype != np.uint8:
    mask_cleaned = mask_cleaned.astype(np.uint8)

# If mask_cleaned might be multi-channel (which it shouldn't be if it's a binary mask, but just in case):
if len(mask_cleaned.shape) > 2 and mask_cleaned.shape[2] > 1:
    mask_cleaned = cv2.cvtColor(mask_cleaned, cv2.COLOR_BGR2GRAY)



# Assuming 'mask_cleaned' is your binary image processed earlier
contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize variables to store the min and max coordinates
min_x, min_y = np.inf, np.inf
max_x, max_y = -np.inf, -np.inf

# Iterate through each contour
for contour in contours:
    # Get the bounding rectangle for each contour
    x, y, w, h = cv2.boundingRect(contour)

    # Update the min and max coordinates based on the rectangle
    min_x, min_y = min(min_x, x), min(min_y, y)
    max_x, max_y = max(max_x, x + w), max(max_y, y + h)

# Print the coordinates of the bounding box
print(f"Bounding Box Coordinates: Top-Left ({min_x}, {min_y}), Bottom-Right ({max_x}, {max_y})")

# Draw the bounding box on the image
cv2.rectangle(currentImage, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

# Display the image with the bounding box
plt.imshow(cv2.cvtColor(currentImage, cv2.COLOR_BGR2RGB))
plt.title("Dart Positions with Bounding Box")
plt.axis("off")
plt.show()

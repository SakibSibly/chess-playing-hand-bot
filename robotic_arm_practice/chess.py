import cv2
import numpy as np

# Load the image
image = cv2.imread("fin.jpg")

if image is None:
    print("Error: Could not load image. Check the file path.")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to reduce noise (for better Canny edge detection)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 200)

# Find contours on the edges
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the original image to draw contours on
contoured_image = image.copy()

# Assume the grid is 8x8, so we expect 64 squares (you may need to adjust if different)
square_size = 60  # Adjust according to your image

# Iterate through the contours
for contour in contours:
    # Get the bounding box of each contour (x, y, w, h)
    x, y, w, h = cv2.boundingRect(contour)

    # Only consider squares of appropriate size
    if w < square_size or h < square_size:
        continue

    # Check if the contour is on a "black" square (alternating squares)
    if (x // square_size + y // square_size) % 2 == 1:  # If the sum is odd, it's a black square
        # Draw the black square contour in green
        cv2.drawContours(contoured_image, [contour], -1, (0, 255, 0), 2)

# Optionally, resize for better viewing
resized_image = cv2.resize(contoured_image, (500, 500))

# Show the result
cv2.imshow("Black Grid Squares", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

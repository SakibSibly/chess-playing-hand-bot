import cv2
import numpy as np

# Load the image
image = cv2.imread("fin.jpg")

if image is None:
    print("Error: Could not load image. Check the file path.")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to reduce noise
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply adaptive thresholding to enhance contrast between black and white regions
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
)

# Optionally, you can use a fixed threshold to distinguish white/black
# _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Apply morphological operations to clean up the image (remove small noise)
kernel = np.ones((5, 5), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Find contours on the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the original image to draw contours on
contoured_image = image.copy()

# Draw all contours (external ones) in green
cv2.drawContours(contoured_image, contours, -1, (0, 255, 0), 2)

# Find the largest external contour (most likely to be the chessboard)
largest_contour = max(contours, key=cv2.contourArea)

# Get the bounding box of the largest contour
x, y, w, h = cv2.boundingRect(largest_contour)

# Draw the bounding box on the original image (for visualization)
cv2.rectangle(contoured_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Crop the region inside the bounding box
cropped_image = image[y:y+h, x:x+w]

# Optionally, resize for better viewing
resized_cropped_image = cv2.resize(cropped_image, (500, 500))

# Show the results
cv2.imshow("Contoured Image", contoured_image)
cv2.imshow("Cropped Image", resized_cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

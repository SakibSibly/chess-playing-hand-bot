import cv2
import numpy as np

def remove_shadows(image):
    """
    Preprocess the image to remove shadows using HSV conversion and morphological operations.
    """
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Extract the Value channel (brightness)
    v_channel = hsv[:, :, 2]

    # Apply adaptive thresholding to normalize brightness
    normalized = cv2.equalizeHist(v_channel)

    # Convert back to HSV and merge with original H and S channels
    hsv[:, :, 2] = normalized
    processed_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    # cv2.imshow("Shadow-Removed Difference", processed_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return processed_image

def detect_difference(image1, image2):
    """
    Detects differences between two chessboard images after shadow removal.
    """
    # Remove shadows from both images
    img1 = remove_shadows(image1)
    img2 = remove_shadows(image2)

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred1 = cv2.GaussianBlur(gray1, (5, 5), 0)
    blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)

    # Use Canny edge detection
    edges1 = cv2.Canny(blurred1, 50, 150)
    edges2 = cv2.Canny(blurred2, 50, 150)

    # Compute absolute difference
    diff = cv2.absdiff(edges1, edges2)

    # Apply thresholding to highlight changes
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Find contours of the differences
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw detected differences
    result = image2.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    # Display the result
    cv2.imshow("Shadow-Removed Difference", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Load two chessboard images before and after a move
image_before = cv2.imread("chessboard_before.jpg")
image_after = cv2.imread("chessboard_after.jpg")

# Detect differences after shadow removal
detect_difference(image_before, image_after)

# remove_shadows(image_after)

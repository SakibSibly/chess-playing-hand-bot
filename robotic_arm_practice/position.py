import cv2
import numpy as np

# Load images (before and after the move)
image1 = cv2.imread("chessboard_before.jpg")  # Before move
image2 = cv2.imread("chessboard_after.jpg")   # After move

def mark_chessboard_squares(image):
    """
    Detects and marks black and white squares on the chessboard.
    White squares will be marked red (🔴) and black squares green (🟢).
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to separate the board from the background
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours of the squares
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area, assuming the largest are the squares
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Create a copy to draw on
    marked_image = image.copy()

    # Loop through all contours to find the squares
    square_side = 60  # Square size (adjust according to your image)

    for contour in contours:
        # Get the bounding box for each square
        x, y, w, h = cv2.boundingRect(contour)
        
        if w < square_side or h < square_side:
            continue  # Ignore small noise
        
        # Define the center of the square
        center = (x + w // 2, y + h // 2)

        # Check if it's a white or black square
        if (x + y) % 2 == 0:  # White square (alternating logic)
            cv2.rectangle(marked_image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red for white squares
        else:
            cv2.rectangle(marked_image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green for black squares

    return marked_image

# Mark chessboard squares in both images
marked_before = mark_chessboard_squares(image1)
marked_after = mark_chessboard_squares(image2)

# Show results
cv2.imshow("Before Move - Chessboard Squares", marked_before)
cv2.imshow("After Move - Chessboard Squares", marked_after)
cv2.waitKey(0)
cv2.destroyAllWindows()

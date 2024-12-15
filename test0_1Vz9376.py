import cv2
import numpy as np

def detect_chessboard(image):
    """Detect the chessboard and perform perspective correction."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort by largest area (assuming the chessboard is the largest rectangle)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  # If the contour has 4 points, assume it's the chessboard
            return approx.reshape((4, 2))
    
    return None

def warp_chessboard(image, corners):
    """Apply perspective transformation to get a top-down view of the chessboard."""
    # Define the target 8x8 grid size
    side_length = 400  # Adjust as needed
    pts1 = np.float32(corners)
    pts2 = np.float32([[0, 0], [side_length, 0], [side_length, side_length], [0, side_length]])
    
    # Perspective transformation
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(image, matrix, (side_length, side_length))
    return warped

def annotate_chessboard(image):
    """Annotate the chessboard with cell names."""
    rows, cols = 8, 8
    cell_size = image.shape[0] // rows  # Assuming the image is square
    
    annotated_image = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    color = (0, 255, 0)  # Green for annotations
    
    for row in range(rows):
        for col in range(cols):
            # Calculate cell coordinates
            x_start, y_start = col * cell_size, row * cell_size
            x_end, y_end = (col + 1) * cell_size, (row + 1) * cell_size
            
            # Get chessboard notation
            column_letter = chr(ord('a') + col)
            row_number = 8 - row
            cell_name = f"{column_letter}{row_number}"
            
            # Annotate the cell
            text_size = cv2.getTextSize(cell_name, font, font_scale, thickness)[0]
            text_x = x_start + (cell_size - text_size[0]) // 2
            text_y = y_start + (cell_size + text_size[1]) // 2
            cv2.putText(annotated_image, cell_name, (text_x, text_y), font, font_scale, color, thickness)
    
    return annotated_image

def main():
    # Read the input image
    image = cv2.imread("state2.jpg")
    if image is None:
        print("Failed to load image.")
        return
    
    # Detect the chessboard
    corners = detect_chessboard(image)
    if corners is None:
        print("Chessboard not detected.")
        return
    
    # Warp the chessboard for a top-down view
    warped = warp_chessboard(image, corners)
    
    # Annotate the chessboard
    annotated = annotate_chessboard(warped)
    
    # Show the annotated chessboard
    cv2.imshow("Annotated Chessboard", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

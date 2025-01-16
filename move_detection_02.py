import cv2
import numpy as np

def detect_move(initial_img_path, final_img_path):
    # Load images
    initial_img = cv2.imread(initial_img_path)
    final_img = cv2.imread(final_img_path)
    
    if initial_img is None or final_img is None:
        raise ValueError("Could not load one or both images")

    # Convert to grayscale
    initial_gray = cv2.cvtColor(initial_img, cv2.COLOR_BGR2GRAY)
    final_gray = cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
    
    # Enhance image contrast
    initial_gray = cv2.equalizeHist(initial_gray)
    final_gray = cv2.equalizeHist(final_gray)
    
    # Apply Gaussian blur to reduce noise
    initial_gray = cv2.GaussianBlur(initial_gray, (5, 5), 0)
    final_gray = cv2.GaussianBlur(final_gray, (5, 5), 0)

    # Find chessboard corners
    board_size = (7, 7)  # Internal corners are 7x7
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    ret1, corners1 = cv2.findChessboardCorners(initial_gray, board_size, None)
    ret2, corners2 = cv2.findChessboardCorners(final_gray, board_size, None)

    if not ret1 or not ret2:
        # Try adaptive thresholding if initial attempt fails
        initial_thresh = cv2.adaptiveThreshold(initial_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                             cv2.THRESH_BINARY, 11, 2)
        final_thresh = cv2.adaptiveThreshold(final_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                           cv2.THRESH_BINARY, 11, 2)
        
        ret1, corners1 = cv2.findChessboardCorners(initial_thresh, board_size, None)
        ret2, corners2 = cv2.findChessboardCorners(final_thresh, board_size, None)
        
        if not ret1 or not ret2:
            raise ValueError("Chessboard corners not detected. Please ensure good lighting and clear images.")

    # Refine corner detection
    corners1 = cv2.cornerSubPix(initial_gray, corners1, (11, 11), (-1, -1), criteria)
    corners2 = cv2.cornerSubPix(final_gray, corners2, (11, 11), (-1, -1), criteria)

    # Calculate square size from corners
    square_size_x = int((corners1[-1][0][0] - corners1[0][0][0]) / 7)
    square_size_y = int((corners1[-1][0][1] - corners1[0][0][1]) / 7)
    
    # Create 8x8 grid of square centers
    squares = []
    top_left_x = corners1[0][0][0] - square_size_x
    top_left_y = corners1[0][0][1] - square_size_y
    
    for row in range(8):
        for col in range(8):
            center_x = int(top_left_x + col * square_size_x + square_size_x/2)
            center_y = int(top_left_y + row * square_size_y + square_size_y/2)
            squares.append((center_x, center_y))

    # Analyze squares for changes
    source = None
    destination = None
    
    for i, (x, y) in enumerate(squares):
        roi_size = min(square_size_x, square_size_y) // 3
        
        # Extract and compare square regions
        initial_roi = initial_gray[
            max(0, y - roi_size):min(initial_gray.shape[0], y + roi_size),
            max(0, x - roi_size):min(initial_gray.shape[1], x + roi_size)
        ]
        final_roi = final_gray[
            max(0, y - roi_size):min(final_gray.shape[0], y + roi_size),
            max(0, x - roi_size):min(final_gray.shape[1], x + roi_size)
        ]
        
        if initial_roi.size == 0 or final_roi.size == 0:
            continue
            
        # Compare using mean intensity and difference threshold
        initial_mean = np.mean(initial_roi)
        final_mean = np.mean(final_roi)
        diff = abs(initial_mean - final_mean)
        
        if diff > 30:  # Threshold for significant change
            if initial_mean < final_mean:
                destination = i
            else:
                source = i

    # Convert indices to chess notation
    def index_to_chess_notation(index):
        row = 7 - (index // 8)  # Flip row index since chess notation starts from bottom
        col = index % 8
        return f"{chr(col + ord('a'))}{row + 1}"

    if source is not None and destination is not None:
        source_notation = index_to_chess_notation(source)
        destination_notation = index_to_chess_notation(destination)
        return f"{source_notation}{destination_notation}"
    else:
        return "No move detected"

# Example usage
try:
    move = detect_move("Initial_Image.jpg", "Final_Image2.jpg")
    print("Detected move:", move)
except ValueError as e:
    print("Error:", str(e))
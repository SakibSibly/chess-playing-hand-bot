import cv2
# import numpy as np

def detect_move(initial_img_path, final_img_path):
    # Load images
    initial_img = cv2.imread(initial_img_path)
    final_img = cv2.imread(final_img_path)

    # Convert to grayscale
    initial_gray = cv2.cvtColor(initial_img, cv2.COLOR_BGR2GRAY)
    final_gray = cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)

    # Threshold images
    _, initial_thresh = cv2.threshold(initial_gray, 128, 255, cv2.THRESH_BINARY_INV)
    _, final_thresh = cv2.threshold(final_gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Detect chessboard grid (manual or using findChessboardCorners)
    board_size = (8, 8)
    ret1, corners1 = cv2.findChessboardCorners(initial_gray, board_size)
    ret2, corners2 = cv2.findChessboardCorners(final_gray, board_size)

    if not ret1 or not ret2:
        raise ValueError("Chessboard corners not detected. Ensure the chessboard is visible.")

    # Divide into 8x8 grid and analyze changes
    source, destination = None, None
    for i, corner in enumerate(corners1):
        x, y = int(corner[0][0]), int(corner[0][1])
        # Crop squares from the grid
        initial_square = initial_thresh[y:y+10, x:x+10]
        final_square = final_thresh[y:y+10, x:x+10]

        # Compare square content
        initial_non_empty = cv2.countNonZero(initial_square) > 0
        final_non_empty = cv2.countNonZero(final_square) > 0

        if initial_non_empty and not final_non_empty:
            source = i
        elif not initial_non_empty and final_non_empty:
            destination = i

    # Convert indices to chessboard notation
    def index_to_chess_notation(index):
        row = index // 8
        col = index % 8
        return f"{chr(col + ord('a'))}{8 - row}"

    if source is not None and destination is not None:
        source_notation = index_to_chess_notation(source)
        destination_notation = index_to_chess_notation(destination)
        return f"{source_notation}{destination_notation}"
    else:
        return "No move detected."

# Example usage
move = detect_move("initial_image.jpg", "final_image.jpg")
print("Detected move:", move)

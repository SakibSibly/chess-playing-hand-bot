import cv2
import numpy as np

# Constants
RESIZED_DIM = (700, 700)  # Resize window for easy selection
CHESSBOARD_SIZE = (8, 8)  # 8x8 virtual chessboard
SQUARE_SIZE = 50  # Each square size in pixels
FRAME_WIDTH, FRAME_HEIGHT = 1280, 720  # Camera resolution

# Capture video from camera
cap = cv2.VideoCapture(0)  # 0 is default webcam
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)

selected_corners = []  # Store selected points
calibrated = False
perspective_matrix = None
previous_frame = None  # Store the previous frame for movement detection

# Function to get square name (A1 to H8)
def get_square_name(row, col):
    columns = "ABCDEFGH"
    return f"{columns[col]}{8 - row}"

# Mouse callback function for selecting chessboard corners
def select_corners(event, x, y, flags, param):
    global calibrated, perspective_matrix

    if event == cv2.EVENT_LBUTTONDOWN and len(selected_corners) < 4:
        selected_corners.append((x, y))
        print(f"Corner {len(selected_corners)} selected: ({x}, {y})")

        if len(selected_corners) == 4:
            calibrated = True
            print("Calibration Complete! Tracking will start.")

# Set up window for selection
cv2.namedWindow("Camera Feed")
cv2.setMouseCallback("Camera Feed", select_corners)

print("Click on the four corners of the chessboard. Press 'q' when done.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, RESIZED_DIM)

    # Mark selected corners
    for (x, y) in selected_corners:
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # If four corners are selected, compute perspective transform
    if calibrated and perspective_matrix is None:
        selected_corners_np = np.array(selected_corners, dtype=np.float32)
        width = CHESSBOARD_SIZE[0] * SQUARE_SIZE
        height = CHESSBOARD_SIZE[1] * SQUARE_SIZE
        dst_corners = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)
        perspective_matrix = cv2.getPerspectiveTransform(selected_corners_np, dst_corners)

    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if len(selected_corners) != 4:
    print("Error: You must select exactly four corners.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Virtual chessboard with labeled squares
virtual_chessboard = np.zeros((height, width, 3), dtype=np.uint8)
for row in range(CHESSBOARD_SIZE[1]):
    for col in range(CHESSBOARD_SIZE[0]):
        color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
        top_left = (col * SQUARE_SIZE, row * SQUARE_SIZE)
        bottom_right = ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE)

        cv2.rectangle(virtual_chessboard, top_left, bottom_right, color, -1)

        # Add label (A1 to H8)
        label = get_square_name(row, col)
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = top_left[0] + (SQUARE_SIZE - text_size[0]) // 2
        text_y = top_left[1] + (SQUARE_SIZE + text_size[1]) // 2
        text_color = (0, 255, 0) if color == (255, 255, 255) else (255, 255, 255)
        cv2.putText(virtual_chessboard, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

# Start tracking movements
print("Tracking Started! Move a piece and see the detected square.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, RESIZED_DIM)

    # Warp frame to get top-down view
    warped_frame = cv2.warpPerspective(frame, perspective_matrix, (width, height))

    # Overlay the virtual chessboard
    blended_frame = cv2.addWeighted(warped_frame, 0.7, virtual_chessboard, 0.3, 0)

    # Convert to grayscale for motion detection
    gray_frame = cv2.cvtColor(warped_frame, cv2.COLOR_BGR2GRAY)
    
    if previous_frame is not None:
        diff = cv2.absdiff(previous_frame, gray_frame)
        _, threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Detect movement
        movement_detected = np.any(threshold > 0)

        if movement_detected:
            # Find where movement happened
            movement_indices = np.column_stack(np.where(threshold > 0))
            for (y, x) in movement_indices:
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if 0 <= row < 8 and 0 <= col < 8:
                    square_name = get_square_name(row, col)
                    print(f"Move detected at {square_name}")

    previous_frame = gray_frame.copy()  # Update previous frame

    # Show output
    cv2.imshow("Chessboard Tracking", blended_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

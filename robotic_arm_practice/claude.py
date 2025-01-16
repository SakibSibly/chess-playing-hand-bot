import cv2
import numpy as np

# Constants
IMAGE_NAME = "chessboard_before.jpg"  # Input image
RESIZED_DIM = (700, 700)  # Resize image for selection
CHESSBOARD_SIZE = (8, 8)  # Virtual chessboard (8x8)
SQUARE_SIZE = 50  # Each square size in pixels

# Load and resize the image
original_image = cv2.imread(IMAGE_NAME)
if original_image is None:
    print("Error: Could not load image.")
    exit()

image = cv2.resize(original_image, RESIZED_DIM)
selected_corners = []  # Store selected points

# Mouse callback function to select 4 corners
def select_corners(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(selected_corners) < 4:
        selected_corners.append((x, y))
        print(f"Corner {len(selected_corners)} selected: ({x}, {y})")
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Mark selected points
        cv2.imshow("Select 4 Corners", image)

# Step 1: Select four corners manually
cv2.imshow("Select 4 Corners", image)
cv2.setMouseCallback("Select 4 Corners", select_corners)

print("Click on the four corners of the chessboard area. Press 'q' when done.")
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') and len(selected_corners) == 4:
        break

cv2.destroyAllWindows()

# Ensure four corners were selected
if len(selected_corners) != 4:
    print("Error: You must select exactly four corners.")
    exit()

# Convert selected corners to NumPy array
selected_corners = np.array(selected_corners, dtype=np.float32)

# Step 2: Define the destination points for a perfect 8x8 grid
width = CHESSBOARD_SIZE[0] * SQUARE_SIZE
height = CHESSBOARD_SIZE[1] * SQUARE_SIZE

dst_corners = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

# Compute the perspective transform matrix
perspective_matrix = cv2.getPerspectiveTransform(selected_corners, dst_corners)

# Create a virtual chessboard
virtual_chessboard = np.zeros((height, width, 3), dtype=np.uint8)

# Chessboard notation (A1 to H8)
columns = "ABCDEFGH"
labels = [[f"{columns[col]}{8-row}" for col in range(8)] for row in range(8)]

for row in range(CHESSBOARD_SIZE[1]):
    for col in range(CHESSBOARD_SIZE[0]):
        color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
        top_left = (col * SQUARE_SIZE, row * SQUARE_SIZE)
        bottom_right = ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE)
        
        # Draw square
        cv2.rectangle(virtual_chessboard, top_left, bottom_right, color, -1)

        # Add square label (A1 to H8)
        label = labels[row][col]
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = top_left[0] + (SQUARE_SIZE - text_size[0]) // 2
        text_y = top_left[1] + (SQUARE_SIZE + text_size[1]) // 2
        text_color = (0, 255, 0) if color == (255, 255, 255) else (255, 255, 255)
        cv2.putText(virtual_chessboard, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

# Step 3: Warp the virtual chessboard to match selected region
warped_chessboard = cv2.warpPerspective(virtual_chessboard, cv2.getPerspectiveTransform(dst_corners, selected_corners), RESIZED_DIM)

# Overlay the virtual chessboard on the original image
mask = cv2.cvtColor(warped_chessboard, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

image[mask > 0] = warped_chessboard[mask > 0]

# Step 4: Show final image
cv2.imshow("Labeled Virtual Chessboard", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

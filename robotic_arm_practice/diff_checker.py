# from PIL import Image, ImageChops

# img1, img2 = Image.open('m_01.jpg'), Image.open('m_02.jpg')

# diff = ImageChops.difference(img1, img2)

# if diff.getbbox():
#     diff.show()
# else:
#     print("NO DIFF")

# ####################### Claude #####################################

# # import cv2
# # import numpy as np

# # def detect_grid(image):
# #     """Detect the 4x4 grid in the image and return its corners."""
# #     # Convert to grayscale
# #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
# #     # Binary threshold
# #     _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
# #     # Find contours
# #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
# #     # Find the largest contour (should be the grid)
# #     grid_contour = max(contours, key=cv2.contourArea)
    
# #     # Get bounding rectangle
# #     x, y, w, h = cv2.boundingRect(grid_contour)
    
# #     return x, y, w, h

# # def detect_pieces(image, grid_bounds):
# #     """Detect white pieces in the image within the grid."""
# #     x, y, w, h = grid_bounds
    
# #     # Convert to grayscale
# #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
# #     # Apply threshold to isolate white pieces
# #     _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    
# #     # Find contours of white pieces
# #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
# #     pieces = []
# #     cell_width = w / 4
# #     cell_height = h / 4
    
# #     for contour in contours:
# #         area = cv2.contourArea(contour)
# #         if area > 100:  # Filter out small noise
# #             M = cv2.moments(contour)
# #             if M["m00"] != 0:
# #                 cx = int(M["m10"] / M["m00"])
# #                 cy = int(M["m01"] / M["m00"])
                
# #                 # Convert to grid coordinates
# #                 col = int((cx - x) / cell_width)
# #                 row = int((cy - y) / cell_height)
                
# #                 if 0 <= row < 4 and 0 <= col < 4:
# #                     pieces.append((row, col))
    
# #     return pieces

# # def create_board_state(pieces):
# #     """Create a 4x4 board state array from piece positions."""
# #     board = [[0] * 4 for _ in range(4)]
# #     for row, col in pieces:
# #         board[row][col] = 1
# #     return board

# # def convert_to_chess_notation(row, col):
# #     """Convert grid coordinates to chess notation."""
# #     col_letter = chr(ord('a') + col)
# #     row_number = 8 - row
# #     return f"{col_letter}{row_number}"

# # def decode_move(board1, board2):
# #     """Decode the chess move by comparing two board states."""
# #     # Find positions that changed
# #     from_pos = None
# #     to_pos = None
    
# #     for row in range(4):
# #         for col in range(4):
# #             if board1[row][col] != board2[row][col]:
# #                 if board1[row][col] == 1:
# #                     from_pos = (row, col)
# #                 else:
# #                     to_pos = (row, col)
    
# #     if from_pos and to_pos:
# #         move_from = convert_to_chess_notation(from_pos[0], from_pos[1])
# #         move_to = convert_to_chess_notation(to_pos[0], to_pos[1])
# #         return move_from + move_to
    
# #     return None

# # def process_chess_images(image1_path, image2_path):
# #     """Process two chess board images and return the move."""
# #     # Read images
# #     img1 = cv2.imread(image1_path)
# #     img2 = cv2.imread(image2_path)
    
# #     # Detect grid in both images
# #     grid1 = detect_grid(img1)
# #     grid2 = detect_grid(img2)
    
# #     # Detect pieces in both images
# #     pieces1 = detect_pieces(img1, grid1)
# #     pieces2 = detect_pieces(img2, grid2)
    
# #     # Create board states
# #     board1 = create_board_state(pieces1)
# #     board2 = create_board_state(pieces2)
    
# #     # Decode the move
# #     move = decode_move(board1, board2)
# #     return move

# # # Example usage
# # image1_path = "/home/sakibsibly/Desktop/robotic_arm_practice/m_01.jpg"
# # image2_path = "/home/sakibsibly/Desktop/robotic_arm_practice/m_02.jpg"
# # move = process_chess_images(image1_path, image2_path)
# # print(f"Chess move: {move}")  # Should print: c7c8

# ################################# 2 #############################
# # import cv2
# # import numpy as np

# # def detect_grid_and_pieces(image_path):
# #     # Read the image
# #     img = cv2.imread(image_path)
# #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
# #     # Threshold to detect pieces (white circles)
# #     _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    
# #     # Find contours of the pieces
# #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
# #     # Filter contours to find the white pieces
# #     pieces = []
# #     for contour in contours:
# #         area = cv2.contourArea(contour)
# #         if area > 100:  # Filter small noise
# #             M = cv2.moments(contour)
# #             if M["m00"] != 0:
# #                 cx = int(M["m10"] / M["m00"])
# #                 cy = int(M["m01"] / M["m00"])
# #                 pieces.append((cx, cy))
    
# #     # Get image dimensions
# #     height, width = gray.shape
    
# #     # Calculate grid cell size (assuming 4x4 grid)
# #     cell_width = width // 4
# #     cell_height = height // 4
    
# #     # Convert piece coordinates to grid positions
# #     grid_positions = []
# #     for px, py in pieces:
# #         grid_x = px // cell_width
# #         grid_y = py // cell_height
# #         grid_positions.append((grid_x, grid_y))
    
# #     return grid_positions

# # def convert_to_chess_notation(grid_x, grid_y, base_col='c', base_row=7):
# #     # Convert grid coordinates to chess notation
# #     col = chr(ord(base_col) + grid_x)
# #     row = base_row - grid_y
# #     return f"{col}{row}"

# # def detect_chess_move(image1_path, image2_path):
# #     # Get positions from both images
# #     pos1 = detect_grid_and_pieces(image1_path)
# #     pos2 = detect_grid_and_pieces(image2_path)
    
# #     # Find the different positions
# #     if len(pos1) >= 1 and len(pos2) >= 1:
# #         # Convert start position to chess notation
# #         start_x, start_y = pos1[0]
# #         start_pos = convert_to_chess_notation(start_x, start_y)
        
# #         # Convert end position to chess notation
# #         end_x, end_y = pos2[0]
# #         end_pos = convert_to_chess_notation(end_x, end_y)
        
# #         return f"{start_pos}{end_pos}"
    
# #     return "Move not detected"

# # # Example usage
# # def process_chess_move(image1_path, image2_path):
# #     move = detect_chess_move(image1_path, image2_path)
# #     print(f"Detected chess move: {move}")
# #     return move

# # # # Example usage
# # image1_path = "/home/sakibsibly/Desktop/robotic_arm_practice/m_01.jpg"
# # image2_path = "/home/sakibsibly/Desktop/robotic_arm_practice/m_02.jpg"
# # move = process_chess_move(image1_path, image2_path)
# # print(f"Chess move: {move}")  # Should print: c7c8


# ####################### ChatGPT #####################
# import cv2
# import numpy as np

# def preprocess_image(image_path):
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     img = cv2.GaussianBlur(img, (5, 5), 0)
#     _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
#     return thresh

# def find_differences(before, after):
#     diff = cv2.absdiff(before, after)
#     contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     positions = []
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         positions.append((x + w//2, y + h//2))  # Get the center of the detected change
    
#     return positions

# def map_to_chess_notation(positions, reference_grid):
#     if len(positions) != 2:
#         return "Invalid move detected"

#     start, end = sorted(positions)  # Assuming top-left to bottom-right sorting
#     start_square = reference_grid.get(start, "??")
#     end_square = reference_grid.get(end, "??")

#     return f"{start_square}{end_square}"

# # Load images
# before_img = preprocess_image("m_01.jpg")
# after_img = preprocess_image("m_02.jpg")

# # Find move positions
# move_positions = find_differences(before_img, after_img)

# # Define a sample 4x4 mapping for the given board section
# reference_grid = {
#     (0, 0): "c8", (1, 0): "d8", (2, 0): "e8", (3, 0): "f8",
#     (0, 1): "c7", (1, 1): "d7", (2, 1): "e7", (3, 1): "f7",
#     (0, 2): "c6", (1, 2): "d6", (2, 2): "e6", (3, 2): "f6",
#     (0, 3): "c5", (1, 3): "d5", (2, 3): "e5", (3, 3): "f5",
# }

# # Convert detected positions to chess notation
# move_notation = map_to_chess_notation(move_positions, reference_grid)

# print("Detected move:", move_notation)


###############################
import cv2
import numpy as np

# Load Images
before_img = cv2.imread("m_01.jpg")
after_img = cv2.imread("m_02.jpg")

def preprocess_image(image):
    """ Convert to grayscale, apply thresholding, and remove noise """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh

# Preprocess both images
before = preprocess_image(before_img)
after = preprocess_image(after_img)

# Compute absolute difference to detect changes
diff = cv2.absdiff(before, after)

# Find contours of the changed areas (moved pieces)
contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def get_cell_position(contours):
    """ Get cell positions based on detected changes """
    positions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        center_x, center_y = x + w // 2, y + h // 2
        positions.append((center_x, center_y))
    return positions

move_positions = get_cell_position(contours)

# Sort to find start and end positions
if len(move_positions) != 2:
    print("Error: Could not detect exactly one move")
else:
    start_pos, end_pos = sorted(move_positions)  # Sorting based on x, y positions

# **Mapping to Chess Notation**
# Define chessboard coordinates for a 4x4 section (c7 to f4)
grid_mapping = {
    (0, 0): "c7", (1, 0): "d7", (2, 0): "e7", (3, 0): "f7",
    (0, 1): "c6", (1, 1): "d6", (2, 1): "e6", (3, 1): "f6",
    (0, 2): "c5", (1, 2): "d5", (2, 2): "e5", (3, 2): "f5",
    (0, 3): "c4", (1, 3): "d4", (2, 3): "e4", (3, 3): "f4",
}

def map_position_to_square(position, grid_size=4):
    """ Converts detected (x, y) positions to chess squares """
    x, y = position
    cell_x = min(int(x / (before.shape[1] / grid_size)), grid_size - 1)
    cell_y = min(int(y / (before.shape[0] / grid_size)), grid_size - 1)
    return grid_mapping.get((cell_x, cell_y), "??")

start_square = map_position_to_square(start_pos)
end_square = map_position_to_square(end_pos)

# **Final Move String**
move_string = f"{start_square}{end_square}"
print("Detected Move:", move_string)

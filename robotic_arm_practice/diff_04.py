import cv2
import numpy as np

def preprocess_image(image):
    """Convert to grayscale, apply thresholding, and remove noise"""
    if image is None:
        raise ValueError("Failed to load image")
        
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    thresh = cv2.adaptiveThreshold(
        blurred, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )
    
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return thresh

def get_piece_positions(image):
    """Get positions of pieces in a single image"""
    # Find contours in the image
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    positions = []
    min_area = 100
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                positions.append((center_x, center_y))
    
    return positions

def map_position_to_square(position, image_shape, grid_size=4):
    """Converts detected (x, y) positions to chess squares"""
    x, y = position
    img_height, img_width = image_shape
    
    cell_width = img_width / grid_size
    cell_height = img_height / grid_size
    
    cell_x = int(x / cell_width)
    cell_y = int(y / cell_height)
    
    cell_x = max(0, min(cell_x, grid_size - 1))
    cell_y = max(0, min(cell_y, grid_size - 1))
    
    cols = ['a', 'b', 'c', 'd']
    rows = ['8', '7', '6', '5']
    
    try:
        notation = f"{cols[cell_x]}{rows[cell_y]}"
        return notation
    except IndexError:
        return "??"

def find_unique_positions(pos1, pos2):
    """Find positions that appear in only one of the lists"""
    set1 = set(pos1)
    set2 = set(pos2)
    return list(set1 - set2), list(set2 - set1)

def detect_chess_move(image1_path, image2_path):
    """Main function to detect chess move from two images"""
    # Load Images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    
    if img1 is None or img2 is None:
        return "Error: Failed to load images"
    
    if img1.shape != img2.shape:
        return "Error: Images have different dimensions"
    
    try:
        # Preprocess both images
        proc1 = preprocess_image(img1)
        proc2 = preprocess_image(img2)
        
        # Get piece positions in both images
        pos1 = get_piece_positions(proc1)
        pos2 = get_piece_positions(proc2)
        
        if len(pos1) == 0 or len(pos2) == 0:
            return "Error: No pieces detected"
            
        # Find unique positions in each image
        unique1, unique2 = find_unique_positions(pos1, pos2)
        
        if len(unique1) != 1 or len(unique2) != 1:
            return f"Error: Invalid number of position changes detected ({len(unique1)}, {len(unique2)})"
        
        # Get chess notation for both positions
        pos1_notation = map_position_to_square(unique1[0], proc1.shape)
        pos2_notation = map_position_to_square(unique2[0], proc2.shape)
        
        if "?" in pos1_notation or "?" in pos2_notation:
            return "Error: Could not map positions to valid squares"
        
        # Compare vertical positions to determine move direction
        _, y1 = unique1[0]
        _, y2 = unique2[0]
        
        # If y1 is smaller (higher on board) than y2, image1 shows the starting position
        # Otherwise, image2 shows the starting position
        if y1 < y2:
            return f"{pos1_notation}{pos2_notation}"
        else:
            return f"{pos2_notation}{pos1_notation}"
        
    except Exception as e:
        return f"Error: {str(e)}"

def process_move(image1_path, image2_path):
    """Process and print the detected move"""
    move = detect_chess_move(image1_path, image2_path)
    print("Detected Move:", move)
    return move

process_move("/home/sakibsibly/Desktop/robotic_arm_practice/move_1.jpg", "/home/sakibsibly/Desktop/robotic_arm_practice/move_2.jpg")

import cv2
import numpy as np

def preprocess_image(image):
    """Convert to grayscale, apply thresholding, and remove noise"""
    if image is None:
        raise ValueError("Failed to load image")
        
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Increase blur kernel size for better noise reduction
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Use adaptive thresholding instead of fixed threshold
    thresh = cv2.adaptiveThreshold(
        blurred, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )
    
    # Apply morphological operations to clean up the image
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return thresh

def get_cell_position(contours, image_shape):
    """Get cell positions based on detected changes"""
    positions = []
    min_area = 100  # Minimum area to consider as valid movement
    
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
    
    # Calculate cell dimensions
    cell_width = img_width / grid_size
    cell_height = img_height / grid_size
    
    # Calculate grid position
    cell_x = int(x / cell_width)
    cell_y = int(y / cell_height)
    
    # Ensure coordinates are within bounds
    cell_x = max(0, min(cell_x, grid_size - 1))
    cell_y = max(0, min(cell_y, grid_size - 1))
    
    # Chess notation mapping (c7 to f4)
    cols = ['c', 'd', 'e', 'f']
    rows = ['7', '6', '5', '4']
    
    try:
        notation = f"{cols[cell_x]}{rows[cell_y]}"
        return notation
    except IndexError:
        return "??"

def detect_chess_move(before_path, after_path):
    """Main function to detect chess move from two images"""
    # Load Images
    before_img = cv2.imread(before_path)
    after_img = cv2.imread(after_path)
    
    # Check if images are loaded successfully
    if before_img is None or after_img is None:
        return "Error: Failed to load images"
    
    # Check if images have the same dimensions
    if before_img.shape != after_img.shape:
        return "Error: Images have different dimensions"
    
    try:
        # Preprocess both images
        before = preprocess_image(before_img)
        after = preprocess_image(after_img)
        
        # Compute absolute difference to detect changes
        diff = cv2.absdiff(before, after)
        
        # Find contours of the changed areas
        contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Get positions of changes
        move_positions = get_cell_position(contours, before.shape)
        
        # Validate number of detected positions
        if len(move_positions) != 2:
            return f"Error: Detected {len(move_positions)} positions instead of 2"
        
        # Sort positions by y-coordinate first, then x-coordinate
        # This ensures correct start and end position detection
        move_positions.sort(key=lambda p: (p[1], p[0]))
        start_pos, end_pos = move_positions
        
        # Map positions to chess notation
        start_square = map_position_to_square(start_pos, before.shape)
        end_square = map_position_to_square(end_pos, before.shape)
        
        if "?" in start_square or "?" in end_square:
            return "Error: Could not map positions to valid squares"
        
        return f"{start_square}{end_square}"
        
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
def process_move(before_path, after_path):
    move = detect_chess_move(before_path, after_path)
    print("Detected Move:", move)
    return move

process_move("/home/sakibsibly/Desktop/robotic_arm_practice/m_01.jpg", "/home/sakibsibly/Desktop/robotic_arm_practice/m_02.jpg")

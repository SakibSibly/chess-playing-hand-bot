# Adjusted code to process the uploaded image with improved grid detection and saved results

import cv2
import numpy as np

# Read the input image
image_path = 'chessBoard.jpeg'  # Path to uploaded image
test_image = cv2.imread(image_path)

# Check if the image is loaded successfully
if test_image is None:
    raise ValueError("Error loading image!")

# Convert BGR to Gray
gray_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to reduce noise
gray_image = cv2.GaussianBlur(gray_image, (3, 3), 50)

# Prepare the edges matrix using Canny Edge Detection
lower_threshold = 20
upper_threshold = 3 * lower_threshold  # Upper threshold should typically be higher than the lower one
test_edges = cv2.Canny(gray_image, lower_threshold, upper_threshold)

# Perform morphological dilation on the edges
SE = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # Structuring element
dilate_iterations = 5  # Number of dilation iterations
bin_dilation = cv2.morphologyEx(test_edges, cv2.MORPH_DILATE, SE, iterations=dilate_iterations)

# Add white borders for better flood-fill handling
image_corners = [
    [(0, 0), (bin_dilation.shape[1], 0)],  # Top-left to top-right
    [(bin_dilation.shape[1], 0), (bin_dilation.shape[1], bin_dilation.shape[0])],  # Top-right to bottom-right
    [(bin_dilation.shape[1], bin_dilation.shape[0]), (0, bin_dilation.shape[0])],  # Bottom-right to bottom-left
    [(0, bin_dilation.shape[0]), (0, 0)]  # Bottom-left to top-left
]
line_thickness = 200
for corner in image_corners:
    cv2.line(bin_dilation, tuple(corner[0]), tuple(corner[1]), 255, line_thickness)

# Perform flood fill at the four corners
fill_offset_x = 200
fill_offset_y = 200
fill_color = 255  # Fill color is white
target_cols = bin_dilation.shape[1]
target_rows = bin_dilation.shape[0]
cv2.floodFill(bin_dilation, None, (fill_offset_x, fill_offset_y), fill_color)
cv2.floodFill(bin_dilation, None, (fill_offset_x, target_rows - fill_offset_y), fill_color)
cv2.floodFill(bin_dilation, None, (target_cols - fill_offset_x, fill_offset_y), fill_color)
cv2.floodFill(bin_dilation, None, (target_cols - fill_offset_x, target_rows - fill_offset_y), fill_color)

# Invert the image to prepare the mask
cube_mask = cv2.bitwise_not(bin_dilation)

# Perform morphological operations to enhance the mask
close_iterations = 50
cube_mask = cv2.morphologyEx(cube_mask, cv2.MORPH_DILATE, SE, iterations=close_iterations)
cube_mask = cv2.morphologyEx(cube_mask, cv2.MORPH_ERODE, SE, iterations=close_iterations)

# Find contours in the mask
contours, hierarchy = cv2.findContours(cube_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Get the bounding rectangle for the largest contour
bounding_rect = cv2.boundingRect(contours[0])

vertical_grids = 8

horizontal_grids = 8



# Update grid dimensions based on 8x8 configuration

grid_width = float(bounding_rect[2]) / horizontal_grids

grid_height = float(bounding_rect[3]) / vertical_grids



# grid_counter = 1

columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


# Draw 8x8 grids and number them

for j in range(vertical_grids):  # Row index

    yo = j * grid_height

    for i in range(horizontal_grids):  # Column index

        xo = i * grid_width

        # Determine the grid box (x, y, width, height)

        grid_box = (bounding_rect[0] + xo, bounding_rect[1] + yo, int(grid_width), int(grid_height))

        

        # Draw the grid rectangle

        cv2.rectangle(test_image, (int(grid_box[0]), int(grid_box[1])),

                      (int(grid_box[0] + grid_box[2]), int(grid_box[1] + grid_box[3])),

                      (0, 0, 255), 2)

        

        # Generate the grid label (e.g., a1, b2)

        grid_label = f"{columns[i]}{8 - j}"  # Columns (a-h), Rows (1-8 in reverse order)

        

        # Position for the grid label text

        text_position = (int(grid_box[0] + 0.3 * grid_box[2]), int(grid_box[1] + 0.7 * grid_box[3]))

        

        # Draw the label on the image

        cv2.putText(test_image, grid_label, text_position, 

                    cv2.FONT_HERSHEY_SIMPLEX, 5.0, (255, 0, 0), 4, cv2.LINE_8, False)

# Save the final output
cv2.imwrite('./grid_detected_final.png', test_image)


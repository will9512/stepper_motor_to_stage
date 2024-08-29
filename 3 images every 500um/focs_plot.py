import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# Specify the directory containing the images
image_folder = "Z:\\Aleyegn_dev\\3 images every 500um"

# Get all image file names from the directory and sort them by the first digit in the filename
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.jpg')],
                     key=lambda x: int(x.split('_')[2]))

# Initialize lists to hold the Z positions and focus scores
z_positions = []
focus_scores = []

# Function to calculate the focus score using variance of Laplacian
def focus_score(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

# Loop through the images, calculate focus scores and determine Z positions
for image_file in image_files:
    # Extract the first digit from the filename (assuming it's the first part before the first underscore)
    z_step = int(image_file.split('_')[2])  # Adjust this index based on actual filename format
    z_position = z_step * 0.5  # Each step is 0.5 mm (500 µm converted to mm)

    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read the image in grayscale
    
    score = focus_score(image)
    focus_scores.append(score)
    z_positions.append(z_position)

# Plot the focus scores against Z positions
plt.figure(figsize=(12, 8))
plt.plot(z_positions, focus_scores, marker='o')
plt.title('Focus Score vs Z Position')
plt.xlabel('Z Position (mm)')
plt.ylabel('Focus Score')
plt.xticks(np.arange(min(z_positions), max(z_positions) + 1, 1.0))  # X-axis ticks every 1 mm
plt.grid(True)

# Save the plot to the specified path
plot_path = os.path.join(image_folder, "focus_score_plot.png")
plt.savefig(plot_path)
plt.close()

print(f"Plot saved to: {plot_path}")

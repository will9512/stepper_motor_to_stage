import serial
import vmbpy
from PIL import Image
import numpy as np

# Set up the serial connection to the Arduino
arduino = serial.Serial(port='COM20', baudrate=9600, timeout=1)  # Replace COM3 with your Arduino's port

# Set up the VmbPy system
vmb = vmbpy.VmbSystem.get_instance()

def capture_images(camera, image_count, num_images=3):
    # Open the camera
    with camera:
        for i in range(num_images):
            # Capture a single frame
            frame = camera.get_frame()

            # Retrieve image data as a NumPy array
            img_data = frame.as_numpy_ndarray()

            # Check the dimensions and format of the image data
            print(f"Image data shape: {img_data.shape}, dtype: {img_data.dtype}")

            # Convert grayscale or other single-channel images
            if len(img_data.shape) == 2:  # Grayscale image (height, width)
                image = Image.fromarray(img_data, mode='L')
            elif len(img_data.shape) == 3 and img_data.shape[2] == 1:  # Single-channel image with (height, width, 1)
                image = Image.fromarray(img_data.squeeze(), mode='L')
            elif len(img_data.shape) == 3 and img_data.shape[2] == 3:  # RGB image (height, width, 3)
                image = Image.fromarray(img_data, mode='RGB')
            else:
                raise ValueError("Unexpected image format!")

            # Save the image to a file
            filename = f'captured_image_{image_count}_{i}.jpg'
            image.save(filename)
            print(f'Captured and saved image as {filename}')

def main():
    with vmb:
        # Get the first available camera
        cameras = vmb.get_all_cameras()
        if not cameras:
            print("No cameras found!")
            return

        camera = cameras[0]
        image_count = 0

        while True:
            # Listen for "CAPTURE" command from Arduino
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()
                if line == "CAPTURE":
                    # Capture 3 images
                    capture_images(camera, image_count, num_images=3)
                    image_count += 1

                    # Notify Arduino that the images have been captured
                    arduino.write(b'DONE\n')

if __name__ == "__main__":
    main()

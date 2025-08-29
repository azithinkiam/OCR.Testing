import os
import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageFilter
import re

# image_path = "c:\\temp\\4.png"
# image_path = "c:\\temp\\7.png"
# image_path = "c:\\temp\\8.png"
image_path = "c:\\temp\\42.png"
file_path = "c:\\temp\\"
config = "--oem 3 --psm 11"

def save_png_filenames(folder_path, output_file):
    try:
        # Open the output file in write mode
        with open(output_file, 'w') as file:
            # Loop through the files in the specified folder
            for filename in os.listdir(folder_path):
                # Check if the file is a PNG (case-insensitive)
                if filename.lower().endswith('.png'):
                    # Write the filename to the text file
                    file.write(f"{filename}\n")
                    image = Image.open(folder_path + '\\' + filename)

                    # Preprocessing: convert to grayscale, apply threshold and GB
                    image = image.convert('L')  # Grayscale
                    image = image.point(lambda x: 0 if x < 155 else 255, '1')  # Simple threshold 
                    image.save('c:\\temp\\tempGRAYSCALE.png')
                    image = cv2.imread("c:\\temp\\tempGRAYSCALE.png")

                    # Apply Gaussian blur to reduce noise and improve OCR accuracy
                    image = cv2.GaussianBlur(image, (5, 5), 0)

                    # Save the image after preprocessing for verification
                    cv2.imwrite("c:\\temp\\preprocessed_image.png", image)

                    string = pytesseract.image_to_string(image, config=config)

                    # Split the filtered string at newline characters
                    lines = string.split('\n')

                    for l in lines[:]:  # Iterate over a copy to allow removal
                        if len(l) < 3:
                            lines.remove(l)
                    print(lines)

                    # Save results to UTF-8 encoded files
                    with open("c:\\temp\\output_string0.txt", "w", encoding="utf-8") as f0:
                        for line in lines:
                            f0.write(line + '\n')
        print(f"\nPNG filenames have been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
save_png_filenames('c:\\temp', 'c:\\temp\\output.txt')


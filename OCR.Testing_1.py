from PIL import Image, ImageFilter
import pytesseract
import cv2
import numpy as np
import os

# If tesseract is not in your PATH, you need to specify its location manually:
# Example for Windows: r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """ Preprocess the image to enhance OCR accuracy. """

    image = Image.open(image_path)

    # Preprocessing: convert to grayscale, apply threshold and GB
    image = image.convert('L')  # Grayscale
    image = image.point(lambda x: 0 if x < 155 else 255, '1')  # Simple threshold 
    image.save('c:\\temp\\tempGRAYSCALE.png')
    # Load the image using OpenCV
    image = cv2.imread("c:\\temp\\tempGRAYSCALE.png")
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to remove noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    
    # Apply adaptive thresholding to binarize the image (high contrast)
    threshold_image = cv2.adaptiveThreshold(blurred_image, 255, # cv2.ADAPTIVE_THRESH_MEAN_C,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY,
                                            15, 5)
    
    # Optionally, apply dilation to make text more solid
    kernel = np.ones((2, 2), np.uint8)
    dilated_image = cv2.dilate(threshold_image, kernel, iterations=1)
    
    cv2.imwrite(image_path + '_', dilated_image)
    
    return dilated_image

def extract_text_from_image(image_path, lang='eng'):
    """ Extract text from image with enhanced accuracy. """
    try:
        # Preprocess the image (clean it up for OCR)
        processed_image = preprocess_image(image_path)
        
        # Save the preprocessed image temporarily to a file
        temp_image_path = 'c:\\temp\\temp_processed_image.png'
        cv2.imwrite(temp_image_path, processed_image)

        # Use pytesseract to extract text from the preprocessed image
        extracted_text = pytesseract.image_to_string(temp_image_path, lang=lang, config='--oem 3 --psm 11')

        # Delete the temporary image file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        # Whitelist characters: only allow alphanumeric and basic punctuation
        whitelist = "NESW0123456789.\n\r\t"
        filtered_text = ''.join(c for c in extracted_text if c in whitelist)

        # Split filtered_text at newline characters
        filtered_lines = filtered_text.split('\n')

        for line in filtered_lines[:]:
            if len(line) < 3:
                filtered_lines.remove(line)

        for i, line in enumerate(filtered_lines[:]):
            # Check for presence of N, W, S, or E in filtered_lines and '.' in those lines
            directions = {'N', 'W', 'S', 'E'}
            if any(d in line for d in directions):
                if '.' in line:
                    new_line = line.replace('.', '')
                    filtered_lines[i] = new_line
        return filtered_lines

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
folder_path = 'c:\\temp\\'
for filename in os.listdir(folder_path):
    # Check if the file is a PNG (case-insensitive)
    if filename.lower().endswith('.png'):
        # Write the filename to the text file
        text = extract_text_from_image(folder_path + filename)

        if text:
            print('\n---\nTEXT FOUND in ' + folder_path + filename + ':')
            print(str(text) + '\n---\n')
        else:
            print("No text extracted from " + folder_path + filename)
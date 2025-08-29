import cv2
import pytesseract
import re

# Load image
image = cv2.imread('c:\\temp\\temp\\7.png')

# Check if image was loaded successfully
if image is None:
    raise FileNotFoundError("Image file not found at c:\\temp\\temp\\42.png")

# Convert to grayscale for better OCR accuracy
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use pytesseract to extract text
text = pytesseract.image_to_string(gray)

# Use pytesseract to detect orientation and script
osd = pytesseract.image_to_osd(gray)

# Extract angle from OSD result
angle_match = re.search(r'(?<=Rotate: )\d+', osd)
if angle_match:
    angle = int(angle_match.group(0))
    print(f"Detected text angle: {angle} degrees")
else:
    print("Could not detect text angle.")

# Display the extracted text
print("Extracted Text:")
print(text)
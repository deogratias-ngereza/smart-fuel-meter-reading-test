import pytesseract
from PIL import Image
import json
import os

current_directory = os.getcwd()

# Define the file paths
image_paths = [
    current_directory+"/sample1.jpeg",
    current_directory+"/sample2.jpeg"
]
# Specify the correct Tesseract installation path
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to extract meter details
def extract_meter_details(image_path):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Use Tesseract OCR to extract text
        extracted_text = pytesseract.image_to_string(img, config='--psm 6')

        # Parse extracted text for relevant details
        details = {
            "sale": None,
            "litre": None,
            "price": None,
            "error": None
        }
        
        # Split text into lines and look for values
        lines = extracted_text.split("\n")
        for line in lines:
            if "SALE" in line.upper():
                try:
                    details["sale"] = float(line.split()[0])
                except:
                    pass
            elif "LITER" in line.upper() or "LITRE" in line.upper():
                try:
                    details["litre"] = float(line.split()[0])
                except:
                    pass
            elif "PRICE" in line.upper():
                try:
                    details["price"] = float(line.split()[0])
                except:
                    pass

        # Check if all details are extracted
        if None in [details["sale"], details["litre"], details["price"]]:
            details["error"] = "Failed to extract some or all meter details."

        return details

    except Exception as e:
        return {"error": str(e)}

# Process each image
results = {}
for image_path in image_paths:
    results[image_path] = extract_meter_details(image_path)

# Convert results to JSON
results_json = json.dumps(results, indent=4)
results_json
print(results_json)
import pdfplumber
import pytesseract
from PIL import Image


# Function to perform OCR on images using Tesseract
def extract_text_tesseract_from_image(image):
    try:
        return pytesseract.image_to_string(image, lang='eng')  # Use 'heb' for Hebrew if needed
    except Exception as e:
        return f"Error during OCR: {str(e)}"


# Function to convert PDF to images and extract text using Tesseract
def extract_text_from_pdf_with_ocr(pdf_file_path):
    extracted_text = ''
    with pdfplumber.open(pdf_file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            try:
                # Convert each page to an image
                page_image = page.to_image(resolution=300)

                # Check if the page image has an 'image' attribute
                if hasattr(page_image, 'original'):
                    image = page_image.original  # Get the PIL image from the 'original' attribute

                    # Extract text using Tesseract
                    page_text = extract_text_tesseract_from_image(image)
                    extracted_text += f"\n--- Page {page_num} ---\n"
                    extracted_text += page_text
                else:
                    print(f"No image available for page {page_num}.")
            except Exception as e:
                print(f"Error processing page {page_num}: {str(e)}")
    return extracted_text


# Test with the provided file path
pdf_file_path = r"testing_database/חישוב גבולות.pdf"  # Update with actual path
extracted_text_tesseract = extract_text_from_pdf_with_ocr(pdf_file_path)

# Print the result or save to a file if needed
print("Extracted text using Tesseract OCR:\n", extracted_text_tesseract)

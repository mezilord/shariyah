import os
import tempfile
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image


# Function to extract text from a PDF file
def extract_text_from_pdf(doc):
    with tempfile.TemporaryDirectory() as temp_images:
        text_of_all_pages_of_doc = ""
        pages = convert_from_bytes(doc.read())
        for i, page in enumerate(pages):
            image_path = os.path.join(temp_images, f"{doc.name}_page_{i + 1}.png")
            page.save(image_path, "PNG")
            text_of_all_pages_of_doc += pytesseract.image_to_string(page)
    return text_of_all_pages_of_doc

# Function to extract text from an image file
def extract_text_from_image(image_file):
    text = pytesseract.image_to_string(Image.open(image_file))
    return text

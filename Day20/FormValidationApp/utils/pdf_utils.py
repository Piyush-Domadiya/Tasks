import numpy as np
import cv2
import fitz  # PyMuPDF – no external Poppler needed

def convert_pdf_to_image(file_path):
    """
    Converts the first page of a PDF file to an OpenCV image (numpy array).
    Uses PyMuPDF (fitz) which works without any external tools.
    """
    try:
        # Open the PDF
        doc = fitz.open(file_path)

        if len(doc) == 0:
            print("PDF has no pages.")
            return None

        # Get first page
        page = doc[0]

        # Render at 300 DPI for good OCR quality (default is 72 DPI)
        zoom = 300 / 72  # ~4.17x zoom
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # Convert pixmap to numpy array
        img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )

        # Convert RGB to BGR for OpenCV (PyMuPDF gives RGB)
        if pix.n == 4:  # RGBA
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
        else:  # RGB
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        doc.close()
        return img_bgr

    except Exception as e:
        print(f"Error converting PDF to image: {e}")
        return None

import cv2
import numpy as np
import fitz  # PyMuPDF – for both PDF→Image AND text extraction
import traceback

def pdf_to_image(file_path):
    """
    Step 1: Convert first page of PDF to an OpenCV image at 300 DPI.
    """
    doc = fitz.open(file_path)
    if len(doc) == 0:
        return None
    page = doc[0]
    zoom = 300 / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    doc.close()
    return img_bgr

def extract_text_from_pdf_region(pdf_path, box_pixel, dpi=300):
    """
    Step 2: Extract text from a specific rectangle region of the filled PDF.
    """
    try:
        scale = 72 / dpi
        x, y, w, h = box_pixel

        # Very small padding (1 pixel) to include as much as possible
        pad = 1
        rect = fitz.Rect(
            x * scale + pad,
            y * scale + pad,
            (x + w) * scale - pad,
            (y + h) * scale - pad
        )

        doc = fitz.open(pdf_path)
        page = doc[0]
        text = page.get_text("text", clip=rect)
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"PyMuPDF get_text error: {e}")
        return ""

def detect_highlighted_boxes(original_img):
    """
    Step 3: Detect highlighted/shaded fields in the original form.
    Increased sensitivity to catch various shades of gray and yellow.
    """
    hsv = cv2.cvtColor(original_img, cv2.COLOR_BGR2HSV)
    
    # --- GRAY input field boxes ---
    # Widened range: V from 100 to 245 to catch light/dark gray, S < 60
    gray_mask = cv2.inRange(hsv, np.array([0, 0, 100]), np.array([180, 60, 245]))

    # We only care about the gray shaded areas indicating required fields
    combined = gray_mask

    # Cleanup - Close gaps but don't Open (Open removes small objects)
    kernel = np.ones((5, 5), np.uint8)
    combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_h, img_w = original_img.shape[:2]
    boxes = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Minimum area 10 to catch very small gray checkboxes
        if 23 < area < (img_h * img_w * 0.5):
            x, y, w, h = cv2.boundingRect(cnt)
            # Filter: set to 25x25 as requested by the user
            # AND exclude the logo area (bottom left: FARROW logo)
            is_logo_area = (x < img_w * 0.35 and y > img_h * 0.85)
            if w >= 23 and h >= 23 and y < (img_h * 0.96) and not is_logo_area:
                boxes.append((x, y, w, h))

    # Sort top-to-bottom
    boxes.sort(key=lambda b: (b[1], b[0]))
    return boxes

def align_images(img_to_align, template_img):
    """
    Advanced Feature Matching (ORB) to align the filled form perfectly
    with the original template. Handles zoom, shift, and rotation from scanning.
    """
    # Convert to grayscale
    gray1 = cv2.cvtColor(img_to_align, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=5000)
    keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

    # Match features (Brute-Force Matcher with Hamming distance)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(descriptors1, descriptors2)

    # Sort matches by distance (best matches first)
    matches = sorted(matches, key=lambda x: x.distance)

    # Keep top 15% matches
    num_good_matches = int(len(matches) * 0.15)
    matches = matches[:num_good_matches]

    if len(matches) < 10:
        # If alignment fails, fallback to simple resize
        print("Warning: ORB Alignment failed, falling back to resize.")
        h1, w1 = template_img.shape[:2]
        return cv2.resize(img_to_align, (w1, h1), interpolation=cv2.INTER_AREA)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find Homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography to warp image
    height, width = template_img.shape[:2]
    aligned_img = cv2.warpPerspective(img_to_align, h, (width, height))
    
    return aligned_img

def process_forms(original_pdf_path, filled_pdf_path, result_path):
    """
    Compare forms and create results.
    """
    orig_img = pdf_to_image(original_pdf_path)
    filled_img = pdf_to_image(filled_pdf_path)

    if orig_img is None or filled_img is None:
        raise Exception("Could not convert PDF to image")

    # Step: Align the filled image perfectly with the original
    filled_img_aligned = align_images(filled_img, orig_img)

    original_display = orig_img.copy()
    filled_display = filled_img_aligned.copy()

    # Detect boxes (must be detected on ORIGINAL)
    required_boxes = detect_highlighted_boxes(orig_img)

    # Save debug image
    debug_img = orig_img.copy()
    for idx, (x, y, w, h) in enumerate(required_boxes):
        cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(debug_img, f"#{idx+1}", (x+2, y+12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    cv2.imwrite(result_path.replace('.jpg', '_detected_boxes.jpg'), debug_img)

    missing_fields = []

    import re
    
    for i, box in enumerate(required_boxes):
        x, y, w, h = box
        
        # 1. Text Check
        text = extract_text_from_pdf_region(filled_pdf_path, box, dpi=300)
        # Strip invisible non-breaking spaces or weird characters
        clean_text = re.sub(r'\s+', '', text)
        is_empty = (len(clean_text) == 0)
        
        # 2. Pixel Change Check (for tick marks / handwriting)
        if is_empty:
            # Crop exactly the same area (now guaranteed aligned)
            orig_roi = cv2.cvtColor(orig_img[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
            filled_roi = cv2.cvtColor(filled_img_aligned[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
            
            # Find dark pixels (text, lines, ink) - threshold 180 (below 180 is dark)
            _, dark_orig = cv2.threshold(orig_roi, 180, 255, cv2.THRESH_BINARY_INV)
            _, dark_filled = cv2.threshold(filled_roi, 180, 255, cv2.THRESH_BINARY_INV)
            
            # Dilate original dark pixels to account for slight alignment shifts in borders/text
            kernel = np.ones((5, 5), np.uint8)  # Increased kernel to 5x5 for more tolerance
            dark_orig_dilated = cv2.dilate(dark_orig, kernel, iterations=1)
            
            # New dark pixels: dark in filled BUT NOT dark in orig
            new_dark = cv2.bitwise_and(dark_filled, cv2.bitwise_not(dark_orig_dilated))
            
            # If > 1.5% area is NEW dark pixels, something was written or checked
            if cv2.countNonZero(new_dark) > (w * h * 0.015):
                is_empty = False

        if is_empty:
            cv2.rectangle(filled_display, (x, y), (x+w, y+h), (0, 0, 255), 4)
            missing_fields.append({
                "id": i + 1,
                "location": {"x": int(x), "y": int(y), "w": int(w), "h": int(h)},
                "status": "Missing"
            })

    # --- Professional Side-by-Side Layout ---
    label_h = 80
    margin = 60
    center_space = 100
    
    dw, dh = original_display.shape[1], original_display.shape[0]
    total_w = margin * 2 + dw * 2 + center_space
    total_h = dh + label_h + margin * 2
    
    # White background
    canvas = np.zeros((total_h, total_w, 3), dtype=np.uint8)
    canvas[:] = 255
    
    # Header bar function
    def draw_header(h_canvas, text):
        h_canvas[:] = (45, 45, 45) # Professional charcoal gray
        cv2.putText(h_canvas, text, (40, 55), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3)

    label1 = np.zeros((label_h, dw, 3), dtype=np.uint8)
    draw_header(label1, "ORIGINAL TEMPLATE")
    
    label2 = np.zeros((label_h, dw, 3), dtype=np.uint8)
    draw_header(label2, "PROCESSED FILLED FORM")

    # Paste Left
    canvas[margin:margin+label_h, margin:margin+dw] = label1
    canvas[margin+label_h:margin+label_h+dh, margin:margin+dw] = original_display
    
    # Paste Right
    rx = margin + dw + center_space
    canvas[margin:margin+label_h, rx:rx+dw] = label2
    canvas[margin+label_h:margin+label_h+dh, rx:rx+dw] = filled_display
    
    # Center divider line
    line_x = margin + dw + (center_space // 2)
    cv2.line(canvas, (line_x, margin), (line_x, total_h - margin), (108, 92, 231), 5)

    cv2.imwrite(result_path, canvas)
    return missing_fields

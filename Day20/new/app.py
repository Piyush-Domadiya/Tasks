import os
import cv2
import numpy as np
import uuid
import hashlib
import json
from flask import Flask, request, render_template, url_for
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Base directory for the 'new' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure folders inside static
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
RESULT_FOLDER = os.path.join(BASE_DIR, "static", "results")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

HASH_FILE = os.path.join(BASE_DIR, "hashes.json")

def get_file_hash(file_bytes):
    """Calculate MD5 hash of file content"""
    return hashlib.md5(file_bytes).hexdigest()

def get_stored_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hash(file_hash, file_path):
    hashes = get_stored_hashes()
    hashes[file_hash] = file_path
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f)

def pdf_to_image(pdf_path, session_id):
    """Convert first page of PDF to image and save to uploads with session_id"""
    pages = convert_from_path(pdf_path, dpi=300)
    img_path = os.path.join(UPLOAD_FOLDER, f"temp_{session_id}.png")
    pages[0].save(img_path)
    img = cv2.imread(img_path)
    return img

def align_images(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(5000)
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)

    if des1 is None or des2 is None:
        return cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])

    h, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC)

    if h is None:
        return cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    aligned = cv2.warpPerspective(img2, h, (img1.shape[1], img1.shape[0]))
    return aligned

def detect_boxes(original_img):
    gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        area = w*h
        if 2000 < area < 50000:
            boxes.append((x,y,w,h))

    boxes = sorted(boxes, key=lambda b:(b[1],b[0]))
    return boxes

def compare_forms(original_pdf, filled_pdf, session_id):
    original_img = pdf_to_image(original_pdf, f"orig_{session_id}")
    filled_img = pdf_to_image(filled_pdf, f"fill_{session_id}")

    aligned = align_images(original_img, filled_img)
    boxes = detect_boxes(original_img)

    result = aligned.copy()
    missing = 0

    for (x,y,w,h) in boxes:
        orig_roi = cv2.cvtColor(original_img[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
        fill_roi = cv2.cvtColor(aligned[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(orig_roi, fill_roi)
        non_zero = cv2.countNonZero(diff)

        if non_zero < 200:
            cv2.rectangle(result,(x,y),(x+w,y+h),(0,0,255),3)
            missing += 1

    result_filename = f"result_{session_id}.png"
    result_path = os.path.join(RESULT_FOLDER, result_filename)
    cv2.imwrite(result_path, result)

    return missing, result_filename

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        if 'original' not in request.files or 'filled' not in request.files:
            return "Missing files", 400
            
        original = request.files["original"]
        filled = request.files["filled"]

        if original.filename == '' or filled.filename == '':
            return "No files selected", 400

        session_id = str(uuid.uuid4())
        
        # Check for duplicates
        original_bytes = original.read()
        filled_bytes = filled.read()
        
        # Reset file pointers after reading
        original.seek(0)
        filled.seek(0)
        
        orig_hash = get_file_hash(original_bytes)
        fill_hash = get_file_hash(filled_bytes)
        
        stored_hashes = get_stored_hashes()
        
        # Handle original file
        if orig_hash in stored_hashes and os.path.exists(stored_hashes[orig_hash]):
            orig_path = stored_hashes[orig_hash]
        else:
            orig_filename = secure_filename(f"orig_{session_id}_{original.filename}")
            orig_path = os.path.join(UPLOAD_FOLDER, orig_filename)
            original.save(orig_path)
            save_hash(orig_hash, orig_path)

        # Handle filled file
        if fill_hash in stored_hashes and os.path.exists(stored_hashes[fill_hash]):
            fill_path = stored_hashes[fill_hash]
        else:
            fill_filename = secure_filename(f"fill_{session_id}_{filled.filename}")
            fill_path = os.path.join(UPLOAD_FOLDER, fill_filename)
            filled.save(fill_path)
            save_hash(fill_hash, fill_path)

        missing, result_file = compare_forms(orig_path, fill_path, session_id)

        return render_template("result.html", missing=missing, result_image=result_file)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

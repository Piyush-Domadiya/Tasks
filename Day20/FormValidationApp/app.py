import os
import uuid
from flask import Flask, request, jsonify, render_template
from utils.cv_utils import process_forms

# Get absolute path to the directory containing app.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# Configure upload and result folders
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
RESULT_FOLDER = os.path.join(BASE_DIR, 'static', 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER


def allowed_file(filename):
    """Check if file is a PDF"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


@app.route('/')
def index():
    """Render the main UI"""
    return render_template('index.html')


@app.route('/compare', methods=['POST'])
def compare_forms():
    """
    Upload two PDFs and compare them:
    1. PDF → Image conversion 
    2. Detect highlighted boxes (OpenCV)
    3. OCR / text extraction from filled PDF (PyMuPDF)
    4. Mark empty fields with RED border
    """
    if 'original_form' not in request.files or 'filled_form' not in request.files:
        return jsonify({'error': 'Both files are required'}), 400

    original = request.files['original_form']
    filled = request.files['filled_form']

    if original.filename == '' or filled.filename == '':
        return jsonify({'error': 'No files selected'}), 400

    if not (allowed_file(original.filename) and allowed_file(filled.filename)):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    # Save uploaded files
    session_id = str(uuid.uuid4())
    orig_path = os.path.join(app.config['UPLOAD_FOLDER'], f'orig_{session_id}.pdf')
    filled_path = os.path.join(app.config['UPLOAD_FOLDER'], f'filled_{session_id}.pdf')

    original.save(orig_path)
    filled.save(filled_path)

    try:
        # Result image path
        result_filename = f'result_{session_id}.jpg'
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)

        # Process: PDF paths go in, annotated image + missing fields come out
        missing_fields = process_forms(orig_path, filled_path, result_path)

        return jsonify({
            'success': True,
            'result_image': f'/static/results/{result_filename}',
            'missing_fields': missing_fields,
            'session_id': session_id
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/debug/<session_id>')
def debug_view(session_id):
    """Show debug images — detected boxes and mask"""
    return f'''
    <html><body style="background:#111;color:#fff;font-family:sans-serif;padding:20px;">
    <h2>Debug: Detected Boxes (Green = detected highlighted areas)</h2>
    <img src="/static/results/result_{session_id}_detected_boxes.jpg" style="max-width:90%;border:2px solid #666;margin:10px 0;">
    </body></html>
    '''


if __name__ == '__main__':
    app.run(debug=True, port=5000)

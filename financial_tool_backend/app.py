from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from process_file import process_financial_file, calculate_savings_goal
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
MAX_FILE_SIZE = 200 * 1024 * 1024
UPLOADS_DIR = 'uploads'
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Starting file upload")
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    file_size = int(request.headers.get('Content-Length', 0))
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large! Max size is 200MB.'}), 400
    
    file_path = os.path.join(UPLOADS_DIR, file.filename)
    file.save(file_path)
    
    try:
        logger.info(f"Processing file: {file_path}")
        result = process_financial_file(file_path)
        if result is None:
            return jsonify({'error': 'Invalid file format or data. Ensure it has Date, Expense, and Type of Expense columns.'}), 400
        logger.info("File processed successfully")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Temporary file removed")

@app.route('/predict', methods=['POST'])
def predict_savings():
    try:
        data = request.get_json()
        total_expenses = float(data['total_expenses'])  # This will be the filtered total from frontend
        monthly_income = float(data['monthly_income'])
        goal_type = data['goal_type']
        goal_cost = float(data['goal_cost'])
        type_summary = data.get('type_summary', {})
        filtered_time_series = data.get('filtered_time_series', {})

        prediction = calculate_savings_goal(total_expenses, monthly_income, goal_type, goal_cost, type_summary, filtered_time_series)
        return jsonify(prediction)
    except (KeyError, ValueError) as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400

if __name__ == '__main__':
    from waitress import serve
    logger.info("Starting Waitress server on http://localhost:5000")
    serve(app, host='0.0.0.0', port=5000, threads=4)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from summarizer import summarize_pdf

app = Flask(__name__)
CORS(app)  # Enables CORS so Netlify frontend can access it

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "✅ PDF Summarizer Backend is Live!"

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF uploaded'}), 400

    file = request.files['pdf']
    if file.filename.endswith('.pdf'):
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        summary = summarize_pdf(path)
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

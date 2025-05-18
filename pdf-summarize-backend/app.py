from flask import Flask, render_template, request
import os
from summarizer import summarize_pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        file = request.files['pdf']
        if file and file.filename.endswith('.pdf'):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            summary = summarize_pdf(path)
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)

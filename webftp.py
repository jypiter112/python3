from flask import Flask, request, render_template, redirect, url_for
import os

# Remember to set uinbound and outbound rules!

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('ui.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return 'No file part', 400
    
    files = request.files.getlist('files')
    saved_files = []

    for file in files:
        if file and file.filename:
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(save_path)
            saved_files.append(file.filename)

    if saved_files:
        return f"Uploaded files: {', '.join(saved_files)}"
    else:
        return 'No valid files uploaded.', 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

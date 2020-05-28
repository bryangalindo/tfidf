import os

from flask import Flask, flash, redirect, render_template, request, url_for

import tfidf


UPLOAD_FOLDER = './docs/'
ALLOWED_EXTENSIONS = {'txt',}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload')
def submit_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'text' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['text']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print(file)
            print(request.files)
            return render_template('upload_success.html')


if __name__ == '__main__':
    app.run(debug=True)

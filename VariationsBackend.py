from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import music21, os
from combined import simpleFileRandomizer
from werkzeug import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/home/andy/Desktop/VariationsOnATheme/variations-on-a-theme/uploads/'
app.config['DOWNLOAD_FOLDER'] = '/home/andy/Desktop/VariationsOnATheme/variations-on-a-theme/toDownload/'
app.config['ALLOWED_EXTENSIONS'] = set(['mid'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file'] #Type <class 'werkzeug.datastructures.FileStorage'>
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) #filename is type str
        simpleFileRandomizer(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()
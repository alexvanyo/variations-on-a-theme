from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
import music21, os
from combined import simpleFileRandomizer
from werkzeug import secure_filename
from time import time

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads/')+"/"
app.config['DOWNLOAD_FOLDER'] = os.path.abspath('toDownload/')+"/"
app.config['ALLOWED_EXTENSIONS'] = set(['mid','midi','xml'])

#Directories for API
app.config['API_UPLOADS'] = os.path.abspath('APIuploads/')+"/"
app.config['API_DOWNLOAD'] = os.path.abspath('APItoDownload')+"/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('file[]') #creates list of FileStorage objects
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            curTime = str(time())
            filename = secure_filename(file.filename) #filename is type str
            filename = filename[:len(filename)-4] + curTime + '.mid'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                randomizedSong = simpleFileRandomizer(app.config['UPLOAD_FOLDER'] + filename)
            except TypeError:
                return redirect(url_for('variate_error'))
            fp = randomizedSong.write('midi', fp=app.config['DOWNLOAD_FOLDER'] + filename)
            filenames.append(filename)
    for file in filenames:
        redirect(url_for('uploaded_file', filename=file))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

@app.route('/error/')
def variate_error():
    return "Cannot process file(s), please try different file(s)"


@app.route('/api/variate', methods=['POST'])
def uploadAPI():
    file = request.files['files']  # Type <class 'werkzeug.datastructures.FileStorage'>
    if file and allowed_file(file.filename):
        curTime = str(time())
        filename = secure_filename(file.filename)  # filename is type str
        filename = filename[:len(filename) - 4] + curTime + '.mid'
        file.save(os.path.join(app.config['API_UPLOADS'], filename))
        try:
            randomizedSong = simpleFileRandomizer(app.config['API_UPLOADS'] + filename)
        except TypeError:
            return redirect(url_for('api_error'))
        fp = randomizedSong.write('midi', fp=app.config['API_DOWNLOAD'] + filename)
        return redirect(url_for('api_uploaded_file', filename=filename))

@app.route('/api/uploads/<filename>')
def api_uploaded_file(filename):
    return send_from_directory(app.config['API_DOWNLOAD'], filename)

@app.route('/api/error/')
def api_error():
    return "Cannot process file(s), please try different file(s)"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80)
    #app.run()

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
import music21, os
from combined import simpleFileRandomizer
from werkzeug import secure_filename
from time import time

app = Flask(__name__)

#Sets file path names for ease of use
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads/')+"/"
app.config['DOWNLOAD_FOLDER'] = os.path.abspath('toDownload/')+"/"
app.config['ALLOWED_EXTENSIONS'] = set(['mid','midi','xml'])

#Directories for API
app.config['API_UPLOADS'] = os.path.abspath('APIuploads/')+"/"
app.config['API_DOWNLOAD'] = os.path.abspath('APItoDownload')+"/"

def allowed_file(filename):
    """
    Checks if given file name is allowed, if not redirects to error
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """
    Renders index.html template file
    """
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload():
    """
    Handles client side browser uploading. Sends files to page rendered by upload.html.
    Allows for multiple cuncurent uploads
    """
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
        else:
            return redirect(url_for('filetype_error'))
    return render_template('upload.html', filenames=filenames)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Sends files from server directory to the client through the browser
    """
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

@app.route('/error/variate')
def variate_error():
    """
    Handles error message for combined.py failure. Failure is typically due to algorithim's
    inability to process part of the song
    """
    return "Cannot process file(s), please try different file(s)"

@app.route('/error/filetype')
def filetype_error():
    """
    Handles error returning if the allowed_file function decides file type is not allowed
    """
    return "Improper file type, please choose an MID, MIDI, or XML file type"

@app.route('/api/documentation')
def displayAPIDocs():
    """
    Displays documentaiton for API
    """
    return render_template('api_documentation.html')

@app.route('/api/variate', methods=['POST'])
def uploadAPI():
    """
    Handles file uploading for the API, there is no client wrapper
    """
    file = request.files['files']  # Type <class 'werkzeug.datastructures.FileStorage'>
    if file and allowed_file(file.filename):
        curTime = str(time())
        filename = secure_filename(file.filename)  # filename is type str
        filename = filename[:len(filename) - 4] + curTime + '.mid'
        file.save(os.path.join(app.config['API_UPLOADS'], filename)) #Saves original file to server
        try:
            randomizedSong = simpleFileRandomizer(app.config['API_UPLOADS'] + filename)
        except TypeError or ValueError:
            return redirect(url_for('api_error'))
        fp = randomizedSong.write('midi', fp=app.config['API_DOWNLOAD'] + filename)
        return redirect(url_for('api_uploaded_file', filename=filename))

@app.route('/api/uploads/<filename>')
def api_uploaded_file(filename):
    """
    Allows for users to get file from server
    """
    return send_from_directory(app.config['API_DOWNLOAD'], filename)

@app.route('/api/error/')
def api_error():
    """
    Only current endpoint that handles errors for the API.
    Should show up as the text attribute of the response object
    """
    return "Cannot process file(s), please try different file(s)"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80)
    #app.run()

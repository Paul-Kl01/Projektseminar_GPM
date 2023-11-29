from flask import Flask, jsonify, request, flash, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
import datetime
import os

UPLOAD_FOLDER = 'C:/Users/keckm/Documents/GitHub/Dateiupload_BOS/data' # Ordner für Dateiablage
ALLOWED_EXTENSIONS = {'pdf'} # bisher nur pdf als Dateiformat erlaubt
#MAX_CONTENT_LENGTH = 16 * 1000 * 1000


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config[UPLOAD_FOLDER] = UPLOAD_FOLDER
#app.config[MAX_CONTENT_LENGTH]

def newIndex():
    lastIndex = len(FILES) + 1
    newIndex = lastIndex + 1
    return newIndex

def getUploadDate():
    upload = datetime.datetime.now()
    upload = upload.strftime("%d.%m.%Y - %H:%M:%S")
    return upload

# überprüfen, ob Dateityp erlaubt
def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

FILES = [ # dummy Liste mit Dokumenten
    {
        'index': '3',
        'title': 'Richtlinien zum Katastrophenschutz Ver. 5.7',
        'type': 'Richtlinie',
        'date': '29.11.2023 - 11:20'
    },
    {
        'index': '1',
        'title': 'Richtlinien zum Katastrophenschutz Ver. 8',
        'type': 'Richtlinie',
        'date': '27.11.2023 - 11:20'
    },
    {
        'index': '2',
        'title': 'Richtlinien zum Katastrophenschutz Ver. 5.5',
        'type': 'Richtlinie',
        'date': '28.11.2023 - 11:20'
    }
] 
# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/files', methods=['GET', 'POST'])
def all_files():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        FILES.append({
            'index': newIndex(),
            'title': post_data.get('title'),
            'type': post_data.get('type'),
            'date': getUploadDate()
        })
        response_object['message'] = 'Ein neues Dokument wurde erfolgreich hinzugefügt.'
    else:
        response_object['files'] = FILES
    return jsonify(response_object)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        file = request.files['file']
        file.save(secure_filename(file.filename))
        response_object['message'] = 'Ein neues Dokument wurde erfolgreich hinzugefügt.'
    else:
        response_object['files'] = FILES
    return jsonify(response_object)
        


if __name__ == '__main__':
    app.run()

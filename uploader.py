# coding: utf-8
import os
import re
from unicodedata import normalize
from uuid import uuid4
from flask import Flask, request, render_template


class Config(object):
    UPLOAD_FOLDER = '/tmp/flask_uploader/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'py'])
    DEBUG = True


app = Flask(__name__)
app.config.from_object(Config)
app.debug = app.config['DEBUG']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def secure_filename(filename):
    _filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]')

    if isinstance(filename, str):
        filename = normalize('NFKD', filename).encode('ascii', 'ignore')

    for sep in os.path.sep, os.path.altsep:
        filename = filename.replace(sep, ' ') if sep else filename

    filename = str(_filename_ascii_strip_re.sub('', '_'.join(filename.split()))).strip('._')

    return filename


def resolves_dir(directory):
    try:
        os.mkdir(directory)
    except OSError:
        # When directory already exists, should return it
        pass
    return directory


def unique_file(filename):
    # Rename this file using simple hex with 10 chars
    split_file = filename.split('.')
    split_file[0] = '{filename}_{file_uuid}'.format(filename=split_file[0], file_uuid=uuid4().hex[:10])
    return '.'.join(split_file)


def send_file(file):
    # Validate if file exists and has allowed extension
    if not allowed_file(file.filename) or not file.filename:
        raise ValueError

    # Rename for secure and unique filename
    filename = secure_filename(file.filename)
    filename = unique_file(filename)

    # Make a directory for multiple usage
    unique_name = uuid4().hex
    directory = resolves_dir(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))

    # Join path and save file
    file_path = os.path.join(directory, filename)
    file.save(file_path)

    return file_path


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file_path = send_file(request.files['file'])
            return render_template('success.html', file_path=file_path)
        except ValueError:
            return render_template('error.html')
    return render_template('upload.html')








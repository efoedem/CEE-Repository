from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_courses/<level>/<semester>')
def get_courses(level, semester):
    # This finds the course folders (Maths, Physics, etc.)
    path = os.path.join(UPLOAD_FOLDER, f'Level_{level}', f'Sem_{semester}')
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    # Get only directories (course names)
    courses = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return {"courses": courses}


@app.route('/get_files/<level>/<semester>/<course>')
def get_files(level, semester, course):
    # This finds the files inside a specific course folder
    path = os.path.join(UPLOAD_FOLDER, f'Level_{level}', f'Sem_{semester}', course)
    try:
        files = os.listdir(path)
        return {"files": files}
    except:
        return {"files": []}


@app.route('/download/<level>/<semester>/<course>/<filename>')
def download_file(level, semester, course, filename):
    path = os.path.join(UPLOAD_FOLDER, f'Level_{level}', f'Sem_{semester}', course)
    return send_from_directory(path, filename)


if __name__ == '__main__':
    app.run(debug=True)
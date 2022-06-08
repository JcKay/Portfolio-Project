from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from colorthief import ColorThief
import os

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "DON'TFUCKWITHME,IWILLFUCKYOU"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb_to_hex(r, g, b):
    return ('{:X}{:X}{:X}').format(r, g, b)


print(rgb_to_hex(255, 165, 1))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"static/uploads/{file.filename}"

            # color thief
            color_thief = ColorThief(image_path)
            the_colors = color_thief.get_palette(color_count=11)

            # rgb to color hash
            color_hash = [rgb_to_hex(color[0], color[1], color[2]) for color in the_colors]
            return render_template('index.html', image=image_path, color=the_colors, hashcode=color_hash)

    return render_template('index.html', original_template=True)


if __name__ == '__main__':
    app.run(debug=True)

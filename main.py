from PIL import Image
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
from collections import Counter


UPLOAD_FOLDER = 'static/images/'


app = Flask(__name__)
app.secret_key = "some secret string"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_hex(color):
    return '#%02x%02x%02x' % (color)


def get_codes(img):
    file_name = f'static/images/{img}'
    image = Image.open(file_name)
    img_array = np.array(image)
    rgb_array = []
    for i in range(len(img_array)):
        for j in range(len(img_array)):
            r = img_array[i][j][0]
            g = img_array[i][j][1]
            b = img_array[i][j][2]
            rgb_array.append((r, g, b))

    count = Counter(rgb_array)
    most_common = count.most_common(10)

    hexes = []
    for color in most_common:
        color = color[0]
        hex = get_hex(color)
        hexes.append(hex)
    return hexes


@app.route('/', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        hexes = get_codes(filename)
        return render_template('index.html', filename=filename, hexes=hexes)
    return render_template("index.html")

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='images/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template, send_file
import cv2
import numpy as np
import io

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')
# Route to handle file upload


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        img = np.fromstring(file.read(), np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        moustache = cv2.imread('static/moustache.png', -1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            # Calculate the size of the moustache based on the face dimensions
            moustache_resized = cv2.resize(moustache, (w, int(h / 2)))

            # Calculate offsets for positioning the moustache on the face
            offset_x = int(w * 0.025)
            offset_y = int(h * 0.47)

            # Iterate over the resized moustache and apply it to the face
            for i in range(moustache_resized.shape[0]):
                for j in range(moustache_resized.shape[1]):
                    if moustache_resized[i, j][3] != 0:  # Check alpha channel for transparency
                        img[y + offset_y + i, x + offset_x + j] = moustache_resized[i, j][:3]

        _, img_encoded = cv2.imencode('.png', img)
        return send_file(io.BytesIO(img_encoded), mimetype='image/png')
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'image' not in request.files:
            return 'No file part', 400

        file = request.files['image']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file', 400

        # Save the file to a specific directory
        file.save('uploads/' + file.filename)

        # Optionally, you can process the uploaded file (e.g., using OpenCV)

        # Redirect to a success page or return a success message
        return 'File uploaded successfully!'
    else:
        # Handle other HTTP methods
        return 'Method not allowed', 405
if __name__ == '__main__':
    app.run(debug=True)

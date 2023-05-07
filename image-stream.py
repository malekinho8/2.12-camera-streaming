import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

def get_webcam_image():
    webcam = cv2.VideoCapture(0)
    ret, frame = webcam.read()
    if ret:
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            image_data = jpeg.tobytes()
    else:
        image_data = None

    webcam.release()
    return image_data

@app.route('/')
def index():
    return render_template('index-image.html')

@app.route('/image')
def image():
    image_data = get_webcam_image()
    if image_data:
        return Response(image_data, content_type='image/jpeg')
    else:
        return "Error capturing image", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True, threaded=True)

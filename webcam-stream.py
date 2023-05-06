import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

def get_webcam_feed():
    webcam = cv2.VideoCapture(0)

    while True:
        ret, frame = webcam.read()
        if not ret:
            break

        ret, jpeg = cv2.imencode('.jpg', frame)

        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    webcam.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(get_webcam_feed(),
                    content_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True, threaded=True)

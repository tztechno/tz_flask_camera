from flask import Flask, render_template, Response, request
import cv2
import datetime
import os

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    success, frame = camera.read()
    if success:
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d_%H%M%S") + ".jpg"
        if not os.path.exists('captures'):
            os.makedirs('captures')
        cv2.imwrite(os.path.join('captures', filename), frame)
        return f"Image captured and saved as {filename}"
    else:
        return "Failed to capture image"

if __name__ == '__main__':
    app.run(debug=True)
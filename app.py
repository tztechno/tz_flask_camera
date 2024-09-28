from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import datetime
import os
from ultralytics import YOLO  # YOLOv8の読み込み

app = Flask(__name__)
camera = None
model = YOLO('yolov8n.pt')  # YOLOv8の最軽量モデルをロード

def start_camera():
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)

def stop_camera():
    global camera
    if camera is not None and camera.isOpened():
        camera.release()

def generate_frames():
    start_camera()  # Start camera if not started
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # YOLOv8によるオブジェクト検出
            results = model(frame)  # 推論結果を取得
            # 検出結果をフレームに描画
            annotated_frame = results[0].plot()  # アノテーション付きのフレームを取得
            
            ret, buffer = cv2.imencode('.jpg', annotated_frame)  # 描画済みフレームをエンコード
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
        return redirect(url_for('index'))  # Redirect back to the camera view
    else:
        return "Failed to capture image"

@app.route('/screenshot', methods=['POST'])
def screenshot():
    success, frame = camera.read()
    if success:
        # YOLOv8によるオブジェクト検出
        results = model(frame)
        annotated_frame = results[0].plot()  # アノテーション付きのフレーム

        # スクリーンショットを保存
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d_%H%M%S") + "_detection.jpg"
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        cv2.imwrite(os.path.join('screenshots', filename), annotated_frame)
        return redirect(url_for('index'))  # Redirect back to the camera view
    else:
        return "Failed to capture screenshot"

@app.route('/toggle_camera', methods=['POST'])
def toggle_camera():
    action = request.form.get('action')
    if action == 'on':
        start_camera()
        return "Camera turned on"
    elif action == 'off':
        stop_camera()
        return "Camera turned off"
    else:
        return "Invalid action"

if __name__ == '__main__':
    app.run(debug=True)


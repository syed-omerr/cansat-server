from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app)

sensor_data = {
    "altitude": 0,
    "temperature": 0
}

def generate_video():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data', methods=['POST'])
def data():
    global sensor_data
    sensor_data = request.json
    return jsonify({"status": "received"})

@app.route('/telemetry')
def telemetry():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


from flask import Flask, request, render_template_string, send_file
import os
from datetime import datetime

app = Flask(__name__)


telemetry_data = {}
image_path = "last_frame.jpg"
deploy_triggered = False

@app.route('/')
def dashboard():
    return render_template_string('''
        <html>
        <head><title>CanSat Dashboard</title></head>
        <body>
            <h1>Live CanSat Telemetry</h1>
            {% if telemetry %}
            <ul>
            {% for key, value in telemetry.items() %}
                <li><b>{{ key }}:</b> {{ value }}</li>
            {% endfor %}
            </ul>
            {% else %}
                <p>No telemetry received yet.</p>
            {% endif %}
            <h2>Live Camera Frame</h2>
            <img src="/frame" width="480" height="360">

            <h2>Parachute Control</h2>
            <form action="/deploy" method="post">
                <button type="submit">DEPLOY PARACHUTE</button>
            </form>
        </body>
        </html>
    ''', telemetry=telemetry_data)

@app.route('/telemetry', methods=['POST'])
def receive_telemetry():
    global telemetry_data
    telemetry_data = request.json
    telemetry_data['timestamp'] = datetime.utcnow().isoformat()
    print("Telemetry received:", telemetry_data)
    return 'OK'

@app.route('/frame', methods=['POST'])
def receive_frame():
    file = request.files['image']
    file.save(image_path)
    print("Frame received")
    return 'OK'

@app.route('/frame')
def get_frame():
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return "No frame yet", 404

@app.route('/deploy', methods=['POST'])
def deploy():
    global deploy_triggered
    deploy_triggered = True
    print("Parachute deployment triggered from UI!")
    return 'DEPLOY command sent!'

@app.route('/deploy')
def check_deploy():
    global deploy_triggered
    if deploy_triggered:
        deploy_triggered = False
        return 'DEPLOY'
    return 'NO'

if __name__ == '__main__':
    app.run(debug=True)

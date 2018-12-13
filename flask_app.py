from flask import Flask
from noise_monitor import NoiseMonitor
app = Flask(__name__)


@app.route("/")
def hello():
    return "host:5000/start = start the alert <BR>" \
           "host:5000/flashlight = flash light only"

@app.route("/config")
def config():
    return "config"

@app.route("/flashlight")
def flashlight():
    monitor = NoiseMonitor()
    monitor.flashlight()
    return "chakalaka is on!"


@app.route("/start")
def start():
    monitor = NoiseMonitor()
    monitor.trigger_alert()
    return "alert has started!"

@app.route("/sunset")
def sunset():
    monitor = NoiseMonitor()
    monitor.playsound(sound_type="sunset")
    return "sunset music is playing!"


if __name__ == '__main__':
    app.run(host='0.0.0.0')

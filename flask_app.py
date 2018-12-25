from flask import Flask
from noise_monitor import NoiseMonitor
from soundmeter.meter import Meter 
import pyaudio
import _thread
app = Flask(__name__)
global monitor

@app.route("/")
def hello():
    return "host:5000/monitor = start the monitor <BR>" \
           "host:5000/stop = stop the monitor"

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

@app.route("/go")
def go():
    global monitor
    go = NoiseMonitor()
    go.start()
    return "smonitoring..."


@app.route("/monitor")
def monitor():
    global monitor
    monitor = NoiseMonitor()
    monitor.start()
    return "smonitoring..."


@app.route("/stop")
def stop():
    global meter
    global monitor

    monitor.stop()
    return "stoped"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
#     app.run()

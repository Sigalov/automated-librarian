from flask import Flask
from noise_monitor import NoiseMonitor
from soundmeter.meter import Meter 
import pyaudio
import _thread
from flask.globals import request
app = Flask(__name__)
global monitor

go_back = '''<button onclick="goBack()">Go Back</button>
            <script>
            function goBack() {
              window.history.back();
            }
            </script>'''


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
    rms_th = request.args.get('rms_th', default = 300, type = int)
    monitor_type = request.args.get('monitor_type', default = 'Live', type = int)
    monitor = NoiseMonitor(rms_th, monitor_type)
    _thread.start_new_thread(monitor.start, ())
    return "Monitoring...<br>" + go_back


@app.route("/stop")
def stop():
    global monitor
    monitor.stop()
    return "Proccess Stoped!<br>" + go_back



@app.route("/return_rms_average")
def return_rms_average():
    global monitor
    return monitor.return_rms_average()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
#     app.run()

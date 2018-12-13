from playsound import playsound
#from soundmeter.monitor import Monitor
from yeelight import Bulb
from yeelight import discover_bulbs
from yeelight import BulbException
import thread
import time


class NoiseMonitor(Monitor):
    rms_list = []
    conf_max_sample = 10
    conf_rms_threshold = 1000
    conf_rms_over_threshold = 5
    is_playing_sound = False
    is_flashing_light = False
    bulb = None

    def __init__(self, *args, **kwargs):
        print('Search for light bulb...')

        bulbs_data = discover_bulbs()
        print(bulbs_data)
        ip = bulbs_data[0]["ip"]
        print(ip)
        self.bulb = Bulb(ip, effect="sudden")

        #super(Monitor, self).__init__(*args, **kwargs)

    def monitor(self, rms):

        self.rms_list.append(rms)
        if len(self.rms_list) > self.conf_max_sample:
            self.rms_list.pop(0)

        self.checkalert()
        pass

    def checkalert(self):

        noise_count = 0
        for curr_rms in self.rms_list:
            if curr_rms > self.conf_rms_threshold:
                noise_count = noise_count + 1

        if noise_count >= self.conf_rms_over_threshold:
            self.trigger_alert()
            self.rms_list = []

    def trigger_alert(self):
        """ Alert - play sound + flash light """
        thread.start_new_thread(self.playsound, ())
        thread.start_new_thread(self.flashlight, ())

    def flashlight(self):
        if not self.is_flashing_light:
            self.is_flashing_light = True
            self.bulb.turn_on()
            try:
                for flash_count in range(0, 5):
                    self.bulb.set_rgb(30, 144, 255)
                    time.sleep(0.6)
                    self.bulb.set_rgb(220, 20, 60)
                    time.sleep(0.6)
            except (RuntimeError, BulbException):
                print("error")

            self.bulb.turn_off()
            self.is_flashing_light = False
        else:
            print("light already flashing")

    def playsound(self):
        if not self.is_playing_sound:
            self.is_playing_sound = True
            playsound('./mp3/siren.mp3')
            self.is_playing_sound = False

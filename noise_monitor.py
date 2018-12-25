from playsound import playsound
from soundmeter.monitor import Monitor
from yeelight import Bulb
from yeelight import discover_bulbs
from yeelight import BulbException
import _thread
import time
import sys
import datetime
from collections import deque
from time import sleep
from _datetime import date


class NoiseMonitor(Monitor):
    rms_list = []
    conf_max_sample = 200
    conf_rms_threshold = 500
    conf_rms_over_threshold = 5
    conf_max_flash_count = 3
    average_q_size = 5
    is_playing_sound = False
    is_flashing_light = False
    bulb = None
    
    rms_average = deque([])
    red_light = False
    first_sound = False
    wait_until = datetime.datetime.now() + datetime.timedelta(seconds=5)

    def __init__(self, *args, **kwargs):
        print('Search for light bulb...')

        bulbs_data = discover_bulbs()
        print(bulbs_data)
        ip = bulbs_data[0]["ip"]
        print(ip)
#         self.bulb = Bulb(ip, effect="sudden")
        self.bulb = Bulb(ip, effect="smooth", duration=1000)
        self.bulb.turn_on()
        self.bulb.set_rgb(255, 255, 255)

        super(Monitor, self).__init__(*args, **kwargs)

    def monitor(self, rms):
        rms_avg = int(round(self.get_rms_average(rms)))
        print('CURRENT RMS: ' + str(rms) + '; AVERAGE RMS: ' + str(rms_avg))
        
        # Convert from 1 to rms threshold, to 1-100 
        bright = int(round(rms_avg / self.conf_rms_threshold * 100))
         
        if bright > 100:
            bright = 100
         
#         if bright < 10:
#             bright = 1
         
        # Check alert per 5 seconds 
        if self.wait_until < datetime.datetime.now():    
            if bright > 99 and self.red_light == True and datetime.datetime.now() < self.wait_until_red_light:
                self.bulb.set_rgb(255, 0, 0)
                print("DEBUG: SET RED")
#                 sleep(0.1)
                _thread.start_new_thread(playsound, ('./mp3/Clear_Throat.mp3',))
                
            if bright > 99 and self.red_light == False:
                self.bulb.set_rgb(0, 255, 0)
                print("DEBUG: SET GREEN")    
            
            if bright > 99:
                # Second alert: red light
                self.red_light = True
                self.wait_until_red_light = datetime.datetime.now() + datetime.timedelta(seconds=7)
            elif bright > 50:
                self.red_light = False
                self.bulb.set_rgb(0, 255, 0)
                print("DEBUG: SET GREEN")
#                 sleep(0.1)             
            else:    
                self.red_light = False
                self.bulb.set_rgb(255, 255, 255)
                print("DEBUG: SET WHITE")
                
            self.bulb.set_brightness(bright)
            print("DEBUG: BRIGHTNESS: " + str(bright) + "; TIME: " + str(datetime.datetime.now().time()))
             
            self.wait_until = datetime.datetime.now() + datetime.timedelta(seconds=5)

        
    def go(self, rms):

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
            self.trigger_alert('shush.mp3')
            self.rms_list = []
            

    def trigger_alert(self, sound):
        """ Alert - play sound + flash light """
        _thread.start_new_thread(self.playsound, (sound,))
        _thread.start_new_thread(self.flashlight, ())
        
        
    def flashlight(self):
        if not self.is_flashing_light:
            self.is_flashing_light = True
            self.bulb.turn_on()
            try:
                for flash_count in range(0, self.conf_max_flash_count):
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


    def playsound(self, sound='shush.mp3'):
        if not self.is_playing_sound:
            self.is_playing_sound = True
            playsound('./mp3/' + str(sound))
            self.is_playing_sound = False
            
            
    def get_rms_average(self, rms, queue_size=average_q_size):
        if len(self.rms_average) > queue_size:
            self.rms_average.popleft()
            
        self.rms_average.append(rms)
            
        return sum(self.rms_average) / len(self.rms_average)     

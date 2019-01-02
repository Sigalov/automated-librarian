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
#     rms_list = []
    conf_max_sample = 200
    conf_rms_threshold = 0
    conf_rms_over_threshold = 5
    conf_max_flash_count = 25
    average_q_size = 5
    is_playing_sound = False
    is_flashing_light = False
    bulb = None
    meterr = None
    interval = 5
    monitor_type = 'Live'
    warning_level = deque([])
    rms_average = deque([])
    red_light = False
    first_sound = False
    wait_until = datetime.datetime.now() + datetime.timedelta(seconds=5)
    no_alert_until = datetime.datetime.now()
    

    def __init__(self, rms_th=300, monitor_type='Live', *args, **kwargs):
        print('Search for light bulb...')
        self.conf_rms_threshold = rms_th
        self.monitor_type = monitor_type
        print('conf_rms_threshold set as: "' + str(self.conf_rms_threshold) + '"')
        bulbs_data = discover_bulbs()
        print(bulbs_data)
        ip = bulbs_data[0]["ip"]
        print(ip)
        self.bulb = Bulb(ip, effect="smooth", duration=1000)
        self.bulb.turn_on()
        self.bulb.set_rgb(255, 255, 255)

        super(Monitor, self).__init__(*args, **kwargs)
        
        
    def monitor(self, rms):
        rms_avg = int(round(self.get_rms_average(rms)))
        print('CURRENT RMS: ' + str(rms) + '; AVERAGE RMS: ' + str(rms_avg))
        if self.monitor_type == 'Live':
            # Convert from 1 to rms threshold, to 1-100 
            bright = int(round(rms_avg / self.conf_rms_threshold * 100))
             
            if bright > 100:
                bright = 100
             
            # Check alert per 5 seconds 
            if self.wait_until < datetime.datetime.now():    
                if bright > 99:
                    if self.no_alert_until < datetime.datetime.now():
                        self.warning_level.append(1)
                        
                        # Call alert method
                        print('CURRENT LEVEL SUM: ' + str(sum(self.warning_level)))
                        self.trigger_warning(sum(self.warning_level))
                    
                    
                elif bright < 100:
                    # Clear all warnings level
                    self.warning_level.clear()
                    
                    # Set to default - White light with low brightness
                    self.bulb.set_rgb(255, 255, 255)
                    print("DEBUG: SET WHITE")
                                    
                    self.bulb.set_brightness(bright)
                    print("DEBUG: BRIGHTNESS: " + str(bright) + "; TIME: " + str(datetime.datetime.now().time()))                
                    
                self.wait_until = datetime.datetime.now() + datetime.timedelta(seconds=self.interval)        


    def trigger_warning(self, warning_level=0):
        if self.no_alert_until < datetime.datetime.now():
            if warning_level == 1:
                self.trigger_alert(sound=None, brightness=100, color_R=0, color_G=255, color_B=0)
    #             self.trigger_alert(sound=None, brightness=100, color_R=255, color_G=165, color_B=0)
            elif warning_level == 2:
                self.trigger_alert(sound=None, brightness=100, color_R=0, color_G=0, color_B=255)
            elif warning_level == 3:
                self.trigger_alert(sound='Shush_Short.mp3', brightness=100, color_R=255, color_G=0, color_B=0)
            elif warning_level == 4:
                self.trigger_alert(sound='shush.mp3', brightness=100, color_R=255, color_G=0, color_B=0)            
            elif warning_level == 5:    
                self.trigger_voice_and_blink()
            elif warning_level > 5:
                self.trigger_alert(sound=None, brightness=100, color_R=255, color_G=0, color_B=0)
                #sleep for 1 mintute   
                self.no_alert_until = datetime.datetime.now() + datetime.timedelta(seconds=60)
                # Clear all warnings level
                self.warning_level.clear()     
            else:
                print("DEBUG: Unhandled level: '" + str(warning_level) + "'")


    def trigger_alert(self, sound, brightness, color_R, color_G, color_B):
        """ Alert - play sound + flash light """
        _thread.start_new_thread(self.playsound, (sound,))
        _thread.start_new_thread(self.set_light, (brightness, color_R, color_G, color_B,))
    
        print("DEBUG: trigger_alert: sound=" + str(sound) + "; brightness=" + str(brightness) + "; color_R=" + str(color_R) + "; color_G=" + str(color_G) + "; color_B=" + str(color_B))
        
    
    def set_light(self, brightness=None, color_R=None, color_G=None, color_B=None):
        if color_R != None and color_G != None and color_B != None:
            self.bulb.set_rgb(color_R, color_G, color_B)
            
        if brightness != None:
            self.bulb.set_brightness(brightness)


    def playsound(self, sound=None):
        try: 
            if sound != None:
                if not self.is_playing_sound:
                    self.is_playing_sound = True
                    playsound('./mp3/' + str(sound))
                    self.is_playing_sound = False
        except Exception:
            pass
            
            
    def get_rms_average(self, rms, queue_size=average_q_size):
        if len(self.rms_average) > queue_size:
            self.rms_average.popleft()
            
        self.rms_average.append(rms)
            
        return sum(self.rms_average) / len(self.rms_average)    
    

    def return_rms_average(self):
        return str(sum(self.rms_average))
            
        
    def trigger_voice_and_blink(self):
        _thread.start_new_thread(self.playsound, ('silence_pleae_esp.wav',))
        _thread.start_new_thread(self.flashlight, (2,))         
    
    
#     def trigger_siren(self):
#         """ Alert - play sound + flash light """
#         _thread.start_new_thread(self.playsound, ('siren.mp3',))
#         _thread.start_new_thread(self.flashlight, ()) 

    
    def flashlight(self, flash_count):
        if not self.is_flashing_light:
            self.is_flashing_light = True
#             self.bulb.turn_on()
            self.bulb.set_brightness(100)
            try:
                for flash_count in range(0, flash_count):
                    self.bulb.set_rgb(30, 144, 255)
                    time.sleep(0.6)
                    self.bulb.set_rgb(220, 20, 60)
                    time.sleep(0.6)
                     
                self.bulb.set_brightness(100)    
                self.bulb.set_rgb(255, 0, 0)                
            except (RuntimeError, BulbException):
                print("error")
 
#             self.bulb.turn_off()
            self.is_flashing_light = False
        else:
            print("light already flashing")    
    
    
#     def go(self, rms):
# 
#         self.rms_list.append(rms)
#         if len(self.rms_list) > self.conf_max_sample:
#             self.rms_list.pop(0)
# 
#         self.checkalert()
#         pass    


#     def checkalert(self):
# 
#         noise_count = 0
#         for curr_rms in self.rms_list:
#             if curr_rms > self.conf_rms_threshold:
#                 noise_count = noise_count + 1
# 
#         if noise_count >= self.conf_rms_over_threshold:
#             self.trigger_alert('shush.mp3')
#             self.rms_list = []     

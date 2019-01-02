from noise_monitor import NoiseMonitor
from soundmeter.meter import Meter 
import pyaudio
from playsound import playsound
from yeelight import Bulb
from yeelight import discover_bulbs
from yeelight import BulbException
import _thread
import time
from time import sleep

try:
    print('NoiseMeter is running...')
    def flash():
        bulbs_data = discover_bulbs()
        print(bulbs_data)
        ip = bulbs_data[0]["ip"]
        print(ip)
        bulb = Bulb(ip, effect="smooth", duration=1000)
        bulb.turn_on()
        bulb.set_rgb(255, 255, 255)
        bulb.set_brightness(100)
        try:
            for flash_count in range(0, 17):
                bulb.set_rgb(30, 144, 255)
                time.sleep(0.6)
                bulb.set_rgb(220, 20, 60)
                time.sleep(0.6)
                 
            bulb.set_brightness(30)    
            bulb.set_rgb(255, 255, 255)
        except (RuntimeError, BulbException):
            print("error")   
     
     
    _thread.start_new_thread(flash, ()) 
    playsound('./mp3/' + str('intro.wav'))
     
    sleep(5) 
    
    meter = Meter()
    monitor = NoiseMonitor(3)

    print('------')
    print('settings:')
    print('rms_threshold: {}'.format(NoiseMonitor.conf_rms_threshold))
    print('max_sample: {}'.format(NoiseMonitor.conf_max_sample))
    print('rms_over_threshold: {}'.format(NoiseMonitor.conf_rms_over_threshold))
    print('------')

    monitor.start()

finally:
    print('NoiseMeter stopped. Bye Bye')
    
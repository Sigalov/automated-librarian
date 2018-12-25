from noise_monitor import NoiseMonitor
from soundmeter.meter import Meter 
import pyaudio

try:
    print('NoiseMeter is running...')
#     p = pyaudio.PyAudio()
#     info = p.get_host_api_info_by_index(0)
#     numdevices = info.get('deviceCount')
#     for i in range(0, numdevices):
#             if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#                 print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
#         
    meter = Meter()
    monitor = NoiseMonitor()

    print('------')
    print('settings:')
    print('rms_threshold: {}'.format(NoiseMonitor.conf_rms_threshold))
    print('max_sample: {}'.format(NoiseMonitor.conf_max_sample))
    print('rms_over_threshold: {}'.format(NoiseMonitor.conf_rms_over_threshold))
    print('------')

    monitor.start()

finally:
    print('NoiseMeter stopped. Bye Bye')


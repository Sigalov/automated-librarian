from soundmeter.meter import Meter
from noise_monitor import NoiseMonitor

try:
    print 'NoiseMeter is running...'

    meter = Meter()
    monitor = NoiseMonitor()

    print '------'
    print 'settings:'
    print 'rms_threshold: {}'.format(NoiseMonitor.conf_rms_threshold)
    print 'max_sample: {}'.format(NoiseMonitor.conf_max_sample)
    print 'rms_over_threshold: {}'.format(NoiseMonitor.conf_rms_over_threshold)
    print '------'

    monitor.start()

finally:
    print 'NoiseMeter stopped. Bye Bye'


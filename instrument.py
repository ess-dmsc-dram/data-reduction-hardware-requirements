from astropy import units as u
from math import sqrt

from performance_model import PerformanceModel

class InstrumentParams:
    def __init__(self, num_pixel, event_rate, run_duration, num_bin, max_rate_compensation=1):
        self.num_pixel = num_pixel
        assert run_duration.unit == u.Unit("s")
        assert event_rate.unit == u.Unit("1 / s")
        self.event_rate = event_rate
        self.run_duration = run_duration
        self.num_bin = num_bin
        self.max_rate_compensation = max_rate_compensation

class Instrument:
    def __init__(self, num_pixel, event_rate, run_duration, bin_count):
        self.params = InstrumentParams(num_pixel, event_rate, run_duration, bin_count)

    def required_resources(self, reduction_duration):
        model = PerformanceModel()
        num_event = self.params.run_duration*self.params.event_rate
        for cores in [ round(sqrt(2)**i) for i in range(19) ]:
            actual_duration = model.seconds(cores, self.params.num_pixel, self.params.run_duration*self.params.event_rate, self.params.num_bin)
            if actual_duration < reduction_duration:
                return {'actual_duration':actual_duration, 'cores':cores, 'cpu_time':cores*actual_duration, 'size_on_disk':num_event*12*u.byte}
        return {'actual_duration':actual_duration, 'cores':cores, 'cpu_time':cores*actual_duration, 'size_on_disk':num_event*12*u.byte}

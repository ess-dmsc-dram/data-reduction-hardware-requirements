from astropy import units as u

from performance_model import PerformanceModel

def memory_requirement(num_pixel, num_event):
    #TODO this is just a single workspace, should we put a factor to have multiple?
    num_bin = 1000 # reasonable generic estimate?
    return num_pixel * num_bin * 3 * 8 * u.byte + num_event * 2 * 8 * u.byte

class InstrumentParams:
    def __init__(self, num_pixel, event_rate, run_duration, max_rate_compensation=1):
        self.num_pixel = num_pixel
        assert run_duration.unit == u.Unit("s")
        assert event_rate.unit == u.Unit("1 / s")
        self.event_rate = event_rate
        self.run_duration = run_duration
        self.max_rate_compensation = max_rate_compensation

class Instrument:
    def __init__(self, num_pixel, event_rate, run_duration):
        self.params = InstrumentParams(num_pixel, event_rate, run_duration)

    def required_resources(self, reduction_duration):
        model = PerformanceModel()
        num_event = self.params.run_duration*self.params.event_rate
        for cores in range(1, 999):
            actual_duration = model.seconds(cores, self.params.num_pixel, self.params.run_duration*self.params.event_rate)
            if actual_duration < reduction_duration:
                return {'cores':cores, 'cpu_time':cores*actual_duration, 'size_on_disk':num_event*12*u.byte, 'memory_per_core':memory_requirement(self.params.num_pixel, num_event)/cores}
        return {'cores':'inf', 'cpu_time':'inf', 'size_on_disk':num_event*12*u.byte, 'memory_per_core':0}

    # figures of interest:
    # - number of cores for given reduction duration
    # - number of CPU seconds (minimal and for given run duration?)

    # normalization runs may be read / reduced multiple times, currently this is not taken into account (underestimating ressource requirements)

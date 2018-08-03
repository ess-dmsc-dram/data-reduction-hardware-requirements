from astropy import units as u

class PerformanceModel:
    def __init__(self):
        # TODO so far our tests do not include saving large data, is it relevant?
        self.t_0 = 10.0 * u.second
        # For reductions mostly in event mode:
        self.t_bin = 1.0/5000000 * u.second
        self.t_event = 1.0/1000000 * u.second
        self.bandwidth_max = 1e8 / u.second

    def seconds(self, num_core, num_pixel, num_event, num_bin):
        return self.t_0 + 1.0/num_core * (num_pixel*num_bin*self.t_bin + num_event*self.t_event) + num_event/self.bandwidth_max

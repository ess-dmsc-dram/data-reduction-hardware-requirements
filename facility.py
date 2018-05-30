from astropy import units as u

from instrument import Instrument

class Facility:
    def __init__(self, accelerator_power = 2.0):
        self.accelerator_power = accelerator_power
        self.reductions_per_run = 2
        self.reduction_speedup = 3
        assert self.reductions_per_run < self.reduction_speedup
        self.workspaces_per_reduction = 8
        self.instruments = {}

    def add_instrument(self, name, parameters):
        self.instruments[name] = parameters

    def script_reduction(self):
        cores = 0
        cpu_time_per_real_time = 0 * u.dimensionless_unscaled
        bandwidth = 0 * u.byte / u.second
        for params in self.instruments.values():
            final_accelerator_power = 2.0
            accelerator_power_fraction = self.accelerator_power / final_accelerator_power
            adjusted_event_rate = params.event_rate * min(1, params.max_rate_compensation * accelerator_power_fraction)
            # TODO pixel buildout phases (include coverage and run duration adjustment!)
            instrument = Instrument(params.num_pixel, adjusted_event_rate, params.run_duration)
            resources = instrument.required_resources(params.run_duration/self.reduction_speedup)
            cores += resources['cores'] # is the sum useful? number of cores for running in parallel a single reduction per instrument?
            cpu_time_per_real_time += self.reductions_per_run * resources['cpu_time'] / params.run_duration
            bandwidth += self.reductions_per_run * resources['size_on_disk'] / params.run_duration
        print(cores, cpu_time_per_real_time, bandwidth)





    # compute combined bandwidth and storage requirements
    # combined CPU-time and core count requirements
    # histogram of memory per core?
    # accelerator power?
    # batch, live, and interactive?

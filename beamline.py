from astropy import units as u

from instrument import Instrument

class Beamline:
    def __init__(self, name):
        self.name = name
        self.phases = []
        self.configs = []

    def add_phase(self, num_pixel):
        self.phases.append(num_pixel)

    def add_config(self, name, event_rate, event_count):
        self.configs.append((name, event_rate, event_count))

    def run(self, accelerator_power, speedup):
        for name, rate, count in self.configs:
            for phase_id, phase in enumerate(self.phases):
                assert phase <= self.phases[-1] # phases must be ordered, highest pixel count last
                for power in accelerator_power:
                    reduced_rate = rate*power/5.0*phase/self.phases[-1]
                    run_duration = count/reduced_rate
                    i = Instrument(phase, reduced_rate, run_duration)
                    output = '{:4.1f} MW {:6} pixels {:7} {:20} n/s {:6.0} run[s] {:6.0f}'.format(power, self.name, phase, name, reduced_rate.value, run_duration.value)
                    for factor in speedup:
                        reduction_duration = run_duration/factor
                        resources = i.required_resources(reduction_duration)
                        output += ' | reduction[s] {:6.0f} cores {:3}'.format(reduction_duration.value, resources['cores'])
                    print(output)


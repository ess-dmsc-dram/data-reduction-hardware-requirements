from math import ceil
from astropy import units as u

from instrument import Instrument
from latex_output import LatexTabular

def memory_requirement(num_pixel, num_event, num_core, num_bin):
    # Assumptions:
    # - Each core (MPI rank) requires a baseline of 1 GB.
    # - The Instrument takes 256 Byte/pixel/core, but is assumed to be shared between workspaces.
    # - We require 5 workspaces.
    base_mem = 2**30 * u.byte
    mem_per_pixel = 256 * u.byte
    num_workspace = 5
    # TODO Include memory for meta-data?
    return num_core*(base_mem + mem_per_pixel * num_pixel) + num_workspace*(num_pixel * num_bin * 3 * 8 * u.byte + num_event * 2 * 8 * u.byte)

class Beamline:
    def __init__(self, name):
        self.name = name
        self.phases = []
        self.configs = []

    def add_phase(self, num_pixel):
        self.phases.append(num_pixel)

    def add_config(self, name, use_fraction, event_rate, event_count, num_bin=5000):
        self.configs.append((name, use_fraction, event_rate, event_count, num_bin))

    def run(self, accelerator_power, speedup):
        latex = LatexTabular(len(self.configs), speedup)
        for phase_id, phase in enumerate(self.phases):
            assert phase <= self.phases[-1] # phases must be ordered, highest pixel count last
            latex.set_pixel_count(phase)
            for name, use_fraction, rate, count, num_bin in self.configs:
                latex.set_config(name)
                for power in accelerator_power:
                    reduced_rate = rate*power/5.0*phase/self.phases[-1]
                    run_duration = count/reduced_rate
                    # Typically we have to process a sample run together with a background run.
                    # For now we assume that both have similar size, i.e., the effective number of
                    # events in the reduction is twice that of the run:
                    sample_and_background = 1 + 1
                    i = Instrument(phase, sample_and_background*reduced_rate, run_duration, num_bin)
                    output = '{:4.1f} MW {:7} {:8} pixels {:.3f} {:30} {:6.0} n/s {:8.1f} run[s]'.format(power, self.name, phase, use_fraction, name, reduced_rate.value, run_duration.value)
                    reduction_rate_min = 2e6 / u.second
                    reduction_duration = max(min(run_duration/speedup, reduced_rate*run_duration/reduction_rate_min), 30 * u.second)
                    resources = i.required_resources(reduction_duration)
                    # TODO take into account that not 100% of time is measurement time?
                    cores = resources['cores']
                    actual_duration = resources['actual_duration']
                    try:
                        # Average cores takes into account reducing data several times.
                        reductions_per_run = 2
                        average_cores = ceil(use_fraction*reductions_per_run*(actual_duration/run_duration)*cores)
                        output += ' {:6.0f} reduction[s] {:4} cores {:6.0f} average-cores'.format(actual_duration.value, cores, average_cores)
                        mem_per_core = ceil(memory_requirement(phase, reduced_rate*run_duration, cores, num_bin).value/2**30/cores)
                        output += ' {:4.0f} GByte/core'.format(mem_per_core)
                        latex.add(power, use_fraction, reduced_rate.value, run_duration.value, actual_duration.value, cores, average_cores, mem_per_core)
                    except:
                        output += ' {:6} reduction[s] {:3} cores {:4} average-cores'.format('   inf', ' inf', '   inf')
                    print(output)
        return latex.lines


from astropy import units as u

from performance_model import PerformanceModel
from instrument import Instrument
from instrument import InstrumentParams
from facility import Facility
import accelerator
from plot import PlotPDF
from beamline import Beamline
from latex_output import generate_latex_header, generate_latex_footer

configs = {}
# Probability for small-sample configurations will increase over time (with increasing accelerator power). How can we handle this here?

configs['BEER'] = {
    'phases':[200000,400000],
    'name':['medium-flux', 'medium-flux-multiplexing', 'high-flux-multiplexing'],
    'rate':[3e5, 2e6, 5e7],
    'count':[1e6, 1e6, 1e6], # same run but scanning the sample volume quickly? TODO is this realistic?
    'num_bin':[8500, 8500, 2000],
    'use':[0.7, 0.2, 0.1]}

configs['BIFROST'] = {
    'phases':[5000],
    'name':['high-flux', 'average'],
    'rate':[1e6, 1e5],
    'count':[1e6, 1e6], # TODO
    'num_bin':[110, 850], #TODO
    'use':[0.2, 0.8]}

configs['CSPEC'] = {
    'phases':[400000,750000],
    'name':['normal', 'RRM'],
    'rate':[1e6, 1e7],
    'count':[1e9, 1e9], # 10 min to 1 h for a single rotation, is this a good estimate?
    'num_bin':[1000, 1000], # TODO
    'use':[0.2, 0.8]} # TODO get numbers from Pascale

configs['DREAM'] = {
    'phases':[4000000,12000000],
    'name':['high-resolution', 'medium', 'high-intensity'],
    'rate':[1.3e6, 1e7, 7.5e7],
    'count':[5e8, 5e8, 5e8], # high resolution is 10 minutes per run
    'num_bin':[71000, 10000, 1420],
    'use':[0.33, 0.33, 0.33]}

# Specular-high-intensity rate is up to 2e7 in total reflection (with two detector banks), but would be used usually for higher angles (only 5% in specular mode), use 2e6 as adjusted rate guess.
configs['ESTIA'] = {
    # TODO configs with 10x higher resolution for WFM upgrade?
    'phases':[250000,500000],
    'name':['reference-high-intensity', 'reference-normal', 'specular-high-intensity', 'specular', 'off-specular'],
    'rate':[1e8, 4e6, 2e6, 8e5, 8e5],
    'count':[1e9, 1e9, 1e7, 1e7, 1e9],
    'num_bin':[450, 450, 450, 450, 450],
    'use':[0.001, 0.01, 0.05, 0.5, 0.5]}

configs['LoKI'] = {
    'phases':[750000,1500000],
    'name':['3m-high-flux', '3m-small-sample', '5m-high-flux', '5m-small-sample', '8m-high-flux', '8m-small-sample'],
    'rate':[1e7, 3.33e5, 1.92e6, 1.2e5, 7.5e5, 4.69e4],
    'count':[1e8, 1e8, 1e8, 1e8, 1e8, 1e8],
    'num_bin':[240, 240, 240, 240, 240, 240],
    'use':[0.1, 0.1, 0.1, 0.3, 0.1, 0.3]}

# TODO event rates
# TODO include pixel factor for polariations?
configs['MAGIC'] = {
    'phases':[1440000,2880000],
    'name':['normal', 'high-flux'],
    'rate':[1e6, 1e7], # "typical sample 1e7" (at high flux)
    'count':[5e5, 5e5], # for each rotation, will have >1000, interpreting each rotation as individual run does not play well with current performance model?
    'num_bin':[7100, 7100],
    'use':[0.2, 0.8]}

# Handling imaging with these equations does not make sense, I believe.
#configs['ODIN'] = {
#    'phases':[262144, 1048576], # Berkley detectors
#    'name':[''],
#    'rate':[1e6],
#    'count':[1e6], # TODO
#    'num_bin':[2804], #TODO
#    'use':[0.2, 0.8]}


for instrument_name, config in configs.items():
    beamline = Beamline(instrument_name)
    for phase in config['phases']:
        beamline.add_phase(phase)
    for name, use, rate, num_bin, count in zip(config['name'], config['use'], config['rate'], config['num_bin'], config['count']):
        beamline.add_config(name, use, rate/u.second, count, num_bin)
    with open("{}.tex".format(instrument_name), "w") as output:
        output.write(generate_latex_header())
        latex = beamline.run([0.2, 0.5, 1.0, 2.0, 5.0], 5)
        for line in latex:
            output.write(line)
        output.write(generate_latex_footer())

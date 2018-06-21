from astropy import units as u

from performance_model import PerformanceModel
from instrument import Instrument
from instrument import InstrumentParams
from facility import Facility
import accelerator
from plot import PlotPDF
from beamline import Beamline

ess = Facility()
#ess.add_instrument('LoKI', InstrumentParams(num_pixel=1575000, event_rate=1e7/u.second, run_duration=1000*u.second, max_rate_compensation=6))
# how to model RRM? put more pixels here?
#ess.add_instrument('CSPEC', InstrumentParams(num_pixel=750000, event_rate=1e7/u.second, run_duration=1000*u.second, max_rate_compensation=1))
ess.add_instrument('dummy1', InstrumentParams(num_pixel=500000, event_rate=3e5/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy2', InstrumentParams(num_pixel=500000, event_rate=3e5/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy3', InstrumentParams(num_pixel=500000, event_rate=1e7/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy4', InstrumentParams(num_pixel=500000, event_rate=2e5/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy5', InstrumentParams(num_pixel=500000, event_rate=8e6/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy6', InstrumentParams(num_pixel=500000, event_rate=1e7/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy7', InstrumentParams(num_pixel=500000, event_rate=1e6/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy8', InstrumentParams(num_pixel=500000, event_rate=7e6/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy9', InstrumentParams(num_pixel=500000, event_rate=7e4/u.second, run_duration=1000*u.second, max_rate_compensation=2))
ess.add_instrument('dummy10', InstrumentParams(num_pixel=500000, event_rate=2e6/u.second, run_duration=1000*u.second, max_rate_compensation=2))
#ess.script_reduction_header()
#ess.script_reduction(0.2)
#ess.script_reduction(0.5)
#ess.script_reduction(1.0)

with PlotPDF('overview.pdf') as p:
    p.plot_line(accelerator.power)

configs = {}
# Probability for small-sample configurations will increase over time (with increasing accelerator power). How can we handle this here?

configs['LoKI'] = {
    'name':['3m-high-flux', '3m-small-sample', '5m-high-flux', '5m-small-sample', '8m-high-flux', '8m-small-sample'],
    'rate':[1e7, 3.33e5, 1.92e6, 1.2e5, 7.5e5, 4.69e4],
    'use':[0.1, 0.1, 0.1, 0.3, 0.1, 0.3]}


loki = Beamline('LoKI')
loki.add_phase(750000)
loki.add_phase(1500000)
for name, rate in zip(configs['LoKI']['name'], configs['LoKI']['rate']):
    loki.add_config(name, rate/u.second, 1e8)
loki.run([0.2, 0.5, 1.0, 2.0, 5.0], [2, 5])

#ess.add_instrument('{}-phase1-{}'.format(instrument_name, config.name), InstrumentParams(num_pixel=750000, event_rate=config.rate, run_duration=required_events/config.rate, max_rate_compensation=1))

#instrument = Instrument(750000, config.rate(accelerator_power), config.run_duration(


#instrument = Instrument(1e6, 600*u.second, 1e7/u.second)
#print(instrument.required_ressources(400*u.second))
#print(instrument.required_ressources(300*u.second))
#print(instrument.required_ressources(200*u.second))

#import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits.mplot3d import axes3d

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#model = PerformanceModel()
#cores = [ 1,2,4,8,16,32,64,128,256,512,1024 ]
#events = [ 1e5, 1e6, 1e7, 1e8, 1e9, 1e10 ]
#cores, events = np.meshgrid(cores, events)
#seconds = model.seconds(cores, 1e6, events)
#ax.plot_wireframe(np.log2(cores), np.log10(events), seconds)
#plt.show()

#ax.yaxis.set_scale('log')


# need average file size (number of files for computing totals)



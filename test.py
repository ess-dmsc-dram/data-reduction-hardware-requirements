from astropy import units as u

from performance_model import PerformanceModel
from instrument import InstrumentParams
from facility import Facility

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
ess.script_reduction_header()
ess.script_reduction(0.2)
ess.script_reduction(0.5)
ess.script_reduction(1.0)
ess.script_reduction(2.0)

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



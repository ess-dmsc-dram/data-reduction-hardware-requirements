import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("SNSPowderReduction_bench_data.txt")
#print np.shape(data)

fig = plt.figure()
ratio = 1.5
sizex = 7.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

n = np.shape(data)[1] / 2

for i in range(n):
    
    ax1.plot(data[:,2*i],data[:,2*i+1]/1000.0,label="fact %i"%(i+1))
    #ax1.plot([0,11],[data[-1,2*i+1]/1000.0,data[-1,2*i+1]/1000.0],color='lightgrey',zorder=-5,lw=1)
    
    time0 = data[0,2*i+1]/1000.0
    ax2.plot(data[:,2*i],time0/(data[:,2*i+1]/1000.0),label="fact %i"%(i+1))

ax2.plot([0,11],[0,11],color='k',zorder=-5,lw=1,label="ideal")

ax1.set_xlim([0,11])
ax1.set_xlabel("Number of CPUs")
ax1.set_ylabel("Workflow runtime (s)")
ax1.legend()


ax2.set_xlim([0,11])
ax2.set_ylim([0,8])
ax2.set_xlabel("Number of CPUs")
ax2.set_ylabel("Speedup")
ax2.legend()

ax1.grid(True,color='gray',linestyle='dotted')
ax2.grid(True,color='gray',linestyle='dotted')

fig.savefig("SNSPowderReduction_bench.pdf",bbox_inches="tight")

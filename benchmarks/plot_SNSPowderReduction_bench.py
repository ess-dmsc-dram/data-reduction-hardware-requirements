import matplotlib.pyplot as plt
import numpy as np

## Name of log file
#infile = "bench_log.txt";
#outfile = "SNSPowderReduction_bench.txt"

#fin = open(infile, 'r')
#fout = open(outfile, 'w')


#header = "#  "

#rows = []

#col_count = 0
#row_count = 0
#row_max = 0

#for line in fin:
    
    #if line.count("Running") > 0:
        #col_count += 1
        ##print(line.index("factor"),line[line.index("factor")].rstrip())
        #header += line.split(' ')[-2]+line.split(' ')[-1].rstrip()+"    "
        #row_count = 0
        
    #if line.count("NCPU") > 0:
        #if col_count == 1:
            #rows.append("  ")
        #rows[row_count] += ("%3i"%int(line.split(' ')[-3]))+" "+("%6i"%int(line.split(' ')[-1].rstrip()))+"  "
        #row_count += 1
        #row_max = max(row_max,row_count)
        
        
#fout.write(header+"\n")
#for r in rows:
    #fout.write(r+"\n")

#fin.close()
#fout.close()

# Now load data and plot

data = np.loadtxt("SNSPowderReduction_bench.txt")
#print np.shape(data)

fig = plt.figure()
ratio = 0.7
sizex = 14.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)


# Find max factor
#maxfact = int(np.amax(data[:,2]))


#n = np.shape(data)[1] / 2

#for i in range(maxfact):
    
    #selection = np.where(data[:,2] == float(i+1))
    
    #ax1.plot(data[:,1][selection],data[:,3][selection],label="fact %i"%(i+1))
    
    
    ##ax1.plot(data[:,2*i],data[:,2*i+1]/1000.0,label="fact %i"%(i+1))
    ###ax1.plot([0,11],[data[-1,2*i+1]/1000.0,data[-1,2*i+1]/1000.0],color='lightgrey',zorder=-5,lw=1)
    
    #time0 = data[:,3][selection][0]
    #print time0
    #ax2.plot(data[:,1][selection],time0/data[:,3][selection],label="fact %i"%(i+1))



Nevents = data[:,4]+data[:,5]

s1 = ax1.scatter(data[:,1],data[:,3],c=Nevents,cmap='jet')
#s1 = ax1.scatter(data[:,1],np.log10(data[:,3]),c=Nevents,cmap='jet')
ax1.set_xlim([0,11])
ax1.set_xlabel("Number of CPUs")
ax1.set_ylabel("Workflow runtime (s)")
#ax1.set_ylabel("Log(runtime) (s)")
cb1 = plt.colorbar(s1,ax=ax1)
cb1.ax.set_ylabel("Number of Events")




time0 = np.zeros([len(data[:,3])])
ncpu_max = int(np.amax(data[:,1]))
fact_max = int(np.amax(data[:,2]))
for j in range(fact_max):
    for i in range(ncpu_max):
        time0[j*ncpu_max+i] = data[j*ncpu_max,3]
#maxfact = int(np.amax(data[:,2]))
#print time0

s2 = ax2.scatter(data[:,1],time0/data[:,3],c=Nevents,cmap='jet')
ax2.plot([0,11],[0,11],color='k',zorder=-5,lw=1,label="ideal")
cb2 = plt.colorbar(s2,ax=ax2)
cb2.ax.set_ylabel("Number of Events")

#ax1.legend()


ax2.set_xlim([0,11])
ax2.set_ylim([0,9])
ax2.set_xlabel("Number of CPUs")
ax2.set_ylabel("Speedup")
#ax2.legend()



sc = ax3.scatter(Nevents,np.log10(data[:,3]),c=data[:,1],cmap='jet')
#sc = ax3.scatter(Nevents,data[:,3],c=data[:,1],cmap='jet')
ax3.set_xlabel("Number of events")
ax3.set_ylabel("Log(runtime) (s)")
cb3 = plt.colorbar(sc,ax=ax3)
cb3.ax.set_ylabel("Number of CPUs")

#print data[:,3]/data[:,4]

sa = ax4.scatter(data[:,1],1.0e6*data[:,3]/Nevents,c=Nevents,cmap='jet')
#sb = ax4.scatter(data[:,1],1.0e6*data[:,3]/data[:,5],color='b')
ax4.set_xlabel("Number of CPUs")
ax4.set_ylabel(r"Time per event ($\mu$s)")
cb4 = plt.colorbar(sa,ax=ax4)
cb4.ax.set_ylabel("Number of Events")



ax1.grid(True,color='gray',linestyle='dotted')
ax2.grid(True,color='gray',linestyle='dotted')
ax3.grid(True,color='gray',linestyle='dotted')
ax4.grid(True,color='gray',linestyle='dotted')

lsize=17
xlab1 = 0.05
xlab2 = 0.95
ylab = 0.93

ax1.text(xlab2,ylab,'a',ha='center',va='center',fontsize=lsize,transform = ax1.transAxes)
ax2.text(xlab1,ylab,'b',ha='center',va='center',fontsize=lsize,transform = ax2.transAxes)
ax3.text(xlab1,ylab,'c',ha='center',va='center',fontsize=lsize,transform = ax3.transAxes)
ax4.text(xlab2,ylab,'d',ha='center',va='center',fontsize=lsize,transform = ax4.transAxes)

fig.savefig("SNSPowderReduction_bench.png",bbox_inches="tight")

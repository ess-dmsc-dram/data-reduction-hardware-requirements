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

cmap1 = "jet"

# Now load data and plot

data = np.loadtxt("SNSPowderReduction_bench.txt")
binData = np.loadtxt("SNSPowderReduction_bins_bench.txt")

#print np.shape(data)

fig = plt.figure()
ratio = 1.0
sizex = 14.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)
ax6 = fig.add_subplot(326)




Nevents = data[:,4]+data[:,5]

s1 = ax1.scatter(data[:,1],data[:,3],c=Nevents,cmap=cmap1)
#s1 = ax1.scatter(data[:,1],np.log10(data[:,3]),c=Nevents,cmap=cmap1)
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

s2 = ax2.scatter(data[:,1],time0/data[:,3],c=Nevents,cmap=cmap1)
ax2.plot([0,11],[0,11],color='k',zorder=-5,lw=1,label="ideal")
cb2 = plt.colorbar(s2,ax=ax2)
cb2.ax.set_ylabel("Number of Events")

#ax1.legend()


ax2.set_xlim([0,11])
ax2.set_ylim([0,9])
ax2.set_xlabel("Number of CPUs")
ax2.set_ylabel("Speedup")
#ax2.legend()



sc = ax3.scatter(Nevents,np.log10(data[:,3]),c=data[:,1],cmap=cmap1)
#sc = ax3.scatter(Nevents,data[:,3],c=data[:,1],cmap=cmap1)
ax3.set_xlabel("Number of events")
ax3.set_ylabel("Log(runtime) (s)")
cb3 = plt.colorbar(sc,ax=ax3)
cb3.ax.set_ylabel("Number of CPUs")

#print data[:,3]/data[:,4]

sa = ax4.scatter(data[:,1],1.0e6*data[:,3]/Nevents,c=Nevents,cmap=cmap1)
#sb = ax4.scatter(data[:,1],1.0e6*data[:,3]/data[:,5],color='b')
ax4.set_xlabel("Number of CPUs")
ax4.set_ylabel(r"Time per event ($\mu$s)")
cb4 = plt.colorbar(sa,ax=ax4)
cb4.ax.set_ylabel("Number of Events")

s5 = ax5.scatter(data[:,1],1.0e6*data[:,6]/data[:,4],c=data[:,4],vmin=0.1e9,vmax=1.4e9,cmap=cmap1)
ax5.scatter(data[:,1],1.0e6*data[:,7]/data[:,5],c=data[:,5],vmin=0.1e9,vmax=1.4e9,cmap=cmap1)
#sb = ax4.scatter(data[:,1],1.0e6*data[:,3]/data[:,5],color='b')
ax5.set_xlabel("Number of CPUs")
ax5.set_ylabel(r"Time of filtering operation per event ($\mu$s)")
cb5 = plt.colorbar(s5,ax=ax5)
cb5.ax.set_ylabel("Number of events")




#s6 = ax6.scatter(np.log10(binData[:,3]),np.log10(binData[:,2]),c=binData[:,1],cmap=cmap1)
##s1 = ax1.scatter(data[:,1],np.log10(data[:,3]),c=Nevents,cmap=cmap1)
##ax6.set_xlim([0,11])
##ax6.set_xscale("log", nonposx='clip')
##ax6.set_yscale("log", nonposy='clip')
#ax6.set_xlabel("Log(Number of bins)")
#ax6.set_ylabel("Log(Workflow runtime) (s)")
##ax1.set_ylabel("Log(runtime) (s)")
#cb6 = plt.colorbar(s6,ax=ax6)
#cb6.ax.set_ylabel("Number of CPUs")


#for i in range(np.shape(binData)[0]):
    #print((binData[i,3]/binData[i,2])/binData[i,1],"bins/s/core",binData[i,3],binData[i,2])






ax1.grid(True,color='gray',linestyle='dotted')
ax2.grid(True,color='gray',linestyle='dotted')
ax3.grid(True,color='gray',linestyle='dotted')
ax4.grid(True,color='gray',linestyle='dotted')
ax5.grid(True,color='gray',linestyle='dotted')
#ax6.grid(True,color='gray',linestyle='dotted')

lsize=17
xlab1 = 0.05
xlab2 = 0.95
ylab = 0.93

ax1.text(xlab2,ylab,'a',ha='center',va='center',fontsize=lsize,transform = ax1.transAxes)
ax2.text(xlab1,ylab,'b',ha='center',va='center',fontsize=lsize,transform = ax2.transAxes)
ax3.text(xlab1,ylab,'c',ha='center',va='center',fontsize=lsize,transform = ax3.transAxes)
ax4.text(xlab2,ylab,'d',ha='center',va='center',fontsize=lsize,transform = ax4.transAxes)
ax5.text(xlab2,ylab,'e',ha='center',va='center',fontsize=lsize,transform = ax5.transAxes)
ax6.text(xlab1,ylab,'f',ha='center',va='center',fontsize=lsize,transform = ax6.transAxes)

fig.savefig("SNSPowderReduction_bench.png",bbox_inches="tight")




fig.clear()

ratio = 0.3
sizex = 14.0
fig.set_size_inches(sizex,ratio*sizex)
ax6 = fig.add_subplot(121)
ax7 = fig.add_subplot(122)



s6 = ax6.scatter(np.log10(binData[:,3]),np.log10(binData[:,2]),c=binData[:,1],cmap=cmap1)
#s1 = ax1.scatter(data[:,1],np.log10(data[:,3]),c=Nevents,cmap=cmap1)
#ax6.set_xlim([0,11])
#ax6.set_xscale("log", nonposx='clip')
#ax6.set_yscale("log", nonposy='clip')
ax6.set_xlabel("Log(Number of bins)")
ax6.set_ylabel("Log(Workflow runtime) (s)")
#ax1.set_ylabel("Log(runtime) (s)")
cb6 = plt.colorbar(s6,ax=ax6)
cb6.ax.set_ylabel("Number of CPUs")


s7 = ax7.scatter(np.log10(binData[:,3]),(binData[:,3]/binData[:,2])/binData[:,1],c=binData[:,1],cmap=cmap1)
ax7.set_xlabel("Log(Number of bins)")
ax7.set_ylabel("bins/s/core")
cb7 = plt.colorbar(s7,ax=ax7)
cb7.ax.set_ylabel("Number of CPUs")

ax6.grid(True,color='gray',linestyle='dotted')
ax7.grid(True,color='gray',linestyle='dotted')
ax6.text(xlab1,ylab,'a',ha='center',va='center',fontsize=lsize,transform = ax6.transAxes)
ax7.text(xlab1,ylab,'b',ha='center',va='center',fontsize=lsize,transform = ax7.transAxes)


fig.savefig("SNSPowderReduction_bins.png",bbox_inches="tight")



# Plot of function timings

fig.clear()

ratio = 2.0
sizex = 6.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_axes([0.0,0.0,1.0,1.0])

ax2 = fig.add_axes([1.05,0.0,1.0,1.0])

tfile = "mantid_function_timings.txt"

f = open(tfile, 'r')
header = f.readline().split()
header.pop(0)
f.close()

#print header

itot = header.index("Total")



time_data = np.loadtxt(tfile)

[nx,ny] = np.shape(time_data)

#print nx,ny

list_x = []
list_y = []
list_z = []

xmin1 = -0.01
xmax1 = 0.16
xmin2 = -5.5
xmax2 = -0.6

names = []

# Perform sorting according to maximum time
max_times = []
for j in range(ny):

      max_times.append(np.amax(time_data[:,j]/time_data[:,itot]))
      #print header[j]
      names.append(header[j])
#print max_times,len(max_times),ny
sort = np.argsort(max_times)

#print sort
#print names


cc = 0
for j in sort:
    print j,names[j]
    if (names[j] != "Total") and (names[j] != "NCPU"):
        cc += 1
        ax1.text(-0.015,cc,names[j],ha='right',va='center')
    for i in range(nx):
        if (names[j] != "Total") and (names[j] != "NCPU"):
            list_x.append(time_data[i,j]/time_data[i,itot])
            list_y.append(cc)
            list_z.append(i+1)
            ax1.plot([xmin1,xmax1],[cc,cc],color='lightgray',ls='dotted',zorder=-10)
            ax2.plot([xmin2,xmax2],[cc,cc],color='lightgray',ls='dotted',zorder=-10)



s9 = ax1.scatter(list_x,list_y,c=list_z,cmap=cmap1)
ax1.set_xlabel("Percentage of total time")
ax1.set_yticklabels([])
cbaxes = fig.add_axes([0.0, 1.02, 1.0, 0.018])
cb9 = plt.colorbar(s9,ax=ax1,orientation='horizontal',cax=cbaxes)
cb9.ax.set_xlabel("Number of CPUs")
cb9.ax.xaxis.set_ticks_position('top')
ax1.grid(True,color='gray',linestyle='dotted')
ax1.get_yaxis().set_visible(False)
ax1.set_ylim([0,48])
ax1.set_xlim([xmin1,xmax1])



s8 = ax2.scatter(np.log10(list_x),list_y,c=list_z,cmap=cmap1)
ax2.set_xlabel("log(Percentage of total time)")
ax2.set_yticklabels([])
cbaxes2 = fig.add_axes([1.05, 1.02, 1.0, 0.018])
cb8 = plt.colorbar(s8,ax=ax2,orientation='horizontal',cax=cbaxes2)
cb8.ax.set_xlabel("Number of CPUs")
cb8.ax.xaxis.set_ticks_position('top')
ax2.grid(True,color='gray',linestyle='dotted')
ax2.get_yaxis().set_visible(False)
ax2.set_ylim([0,48])
ax2.set_xlim([xmin2,xmax2])



fig.savefig("timings.pdf",bbox_inches="tight")





# Name of log file
infile = "bench_log.txt";
outfile = "SNSPowderReduction_bench.txt"

fin = open(infile, 'r')
fout = open(outfile, 'w')

# Define data columns
header = ["Run no.","NCPU","factor","Runtime","Nevents1","Nevents2","t_filter_1","t_filter_2","t_filter_3"]
ncols = len(header)

# Write file header
fout.write("# "+(" ".join(header))+"\n")

# Create data array
data = []
nevents = [0,0]
filterTime = [0,0,0]

factor = 0
run_count = 0
proton_count = 0
get_Nevents = False

badpulse_count = 0
grow_count = 0

function_timings = dict()

ncpu_max = 0

# Go through log file content
for line in fin:

    # If 'Running' is found, it means start of a new block for given grow factor    
    if line.count("Running") > 0:
        grow_count += 1
        factor = float(line.split(' ')[-1].rstrip())
        get_Nevents = True # Only get events when NCPU=1

    # If 'proton' is found, then we find number of events in the line
    if (line.count("proton") > 0) and get_Nevents:
        theLine = line.split(" ")
        iloc = theLine.index("events")
        nevents[proton_count] = float(theLine[iloc-1])

        # Deal with number of events for '77777' and '88888' files
        proton_count += 1
        if proton_count > 1:
            proton_count = 0
            get_Nevents = False

    if line.count("FilterBadPulses successful") > 0:
        filterTime[badpulse_count] = float(line.split(' ')[-2])
        badpulse_count += 1
        if badpulse_count > 2:
          badpulse_count = 0
        
    #if line.count("NBINS_NORMAL") > 0:
        #NBins = float(line.split(' ')[-1].rstrip())
    
    # Get timings for largest dataset
    if (line.count("seconds") > 0) and (grow_count == 20):
        func_name = line.split('-')[0]
        if func_name not in function_timings.keys():
            function_timings[func_name] = []
        func_time = float(line.split(' ')[-2])
        function_timings[func_name].append(func_time)

    # If 'NCPU' is found, then we have number of cpus and runtime
    if line.count("NCPU") > 0:
        data.append([0]*ncols)
        data[run_count][0] = run_count+1
        data[run_count][2] = factor
        
        time_cpu = float(line.split(' ')[-1].rstrip())/1000.0
        ncpu = float(line.split(' ')[-3])
        
        ncpu_max = max(ncpu_max,int(ncpu))
        
        data[run_count][1] = ncpu
        data[run_count][3] = time_cpu
        
        data[run_count][4] = nevents[0]
        data[run_count][5] = nevents[1]
        
        data[run_count][6] = filterTime[0]
        data[run_count][7] = filterTime[1]
        data[run_count][8] = filterTime[2]
        
        if "Total" not in function_timings.keys():
            function_timings["Total"] = []
        function_timings["Total"].append(time_cpu)
        
        #data[run_count][6] = NBins
        run_count += 1
        
#print function_timings

# Write data to file
for i in range(run_count):
    for j in range(ncols):
        fout.write("%.3f  " % data[i][j])
    fout.write("\n")


#ncpu_max = int(np.amax(data[:][1]))
nfuncs = len(function_timings.keys())

njust = 7

tfile = "mantid_function_timings.txt"
f2 = open(tfile, 'w')
head = "# NCPU "
lhead = len(head)
for key in function_timings.keys():
    head += key.ljust(njust)+" "
#for i in range(nfuncs):
    #head += " %4i " % (i+1)
f2.write(head+"\n")

for j in range(ncpu_max):
    f2.write(("  %i" % (j+1)).ljust(lhead))
    for key in function_timings.keys():
        nstep = len(function_timings[key])/ncpu_max
        funcSum = 0.0
        for i in range(nstep):
            funcSum += function_timings[key][i + j*nstep]
        #if j == 0:
          #print key,len(key.ljust(7))
        f2.write(("%.2f" % funcSum).ljust(len(key.ljust(njust))+1))
    f2.write("\n")



# Close files
fin.close()
fout.close()
f2.close()




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

# Go through log file content
for line in fin:

    # If 'Running' is found, it means start of a new block for given grow factor    
    if line.count("Running") > 0:
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

    # If 'NCPU' is found, then we have number of cpus and runtime
    if line.count("NCPU") > 0:
        data.append([0]*ncols)
        data[run_count][0] = run_count+1
        data[run_count][2] = factor
        
        data[run_count][1] = float(line.split(' ')[-3])
        data[run_count][3] = float(line.split(' ')[-1].rstrip())/1000.0
        
        data[run_count][4] = nevents[0]
        data[run_count][5] = nevents[1]
        
        data[run_count][6] = filterTime[0]
        data[run_count][7] = filterTime[1]
        data[run_count][8] = filterTime[2]
        
        #data[run_count][6] = NBins
        run_count += 1
        
# Write data to file
for i in range(run_count):
    for j in range(ncols):
        fout.write("%.3f  " % data[i][j])
    fout.write("\n")

# Close files
fin.close()
fout.close()

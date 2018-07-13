# Name of log file
infile = "bench_log2.txt";
outfile = "SNSPowderReduction_bench_data.txt"

fin = open(infile, 'r')
fout = open(outfile, 'w')


header = "#  "

rows = []

col_count = 0
row_count = 0
row_max = 0

for line in fin:
    
    if line.count("Running") > 0:
        col_count += 1
        #print(line.index("factor"),line[line.index("factor")].rstrip())
        header += line.split(' ')[-2]+line.split(' ')[-1].rstrip()+"    "
        row_count = 0
        
    if line.count("NCPU") > 0:
        if col_count == 1:
            rows.append("  ")
        rows[row_count] += ("%3i"%int(line.split(' ')[-3]))+" "+("%6i"%int(line.split(' ')[-1].rstrip()))+"  "
        row_count += 1
        row_max = max(row_max,row_count)
        
        
fout.write(header+"\n")
for r in rows:
    fout.write(r+"\n")

fin.close()
fout.close()
  

from math import log

def preprocess(filename, bins, scales):
    with open(filename) as f:
        lines = f.readlines()
    lines = [ line.strip() for line in lines ]

    with open("{}-gnuplot".format(filename), 'w') as f:
        f.write("#cores bins runtime[seconds]\n")
        for line in lines:
            rank = line.split(' ')[0]
            timings = line.split(' ')[1:]
            for scale, timing in zip(scales, timings):
                f.write("{} {} {}\n".format(rank, scale*bins, timing))

bins = (12.5 - 1.5)/0.125
scales = [ 2**float(x)/2 for x in range(0,7) ]
preprocess('results/SANS2D-event-mode', bins, scales)
preprocess('results/SANS2D-histogram-mode', bins, scales)
bins = log(2.2/0.1)/0.0004
scales = [ 2**float(x)/4 for x in range(0,7) ]
preprocess('results/PG3-event-mode-scale-0.1', bins, scales)

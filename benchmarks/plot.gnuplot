set term pdf size 8,6
set outp "influence-of-bin-count.pdf"

set loadpath "data" "results"

set title "SNSPowderReduction for PG3"
set yra [0:100]
set xla "MPI ranks"
set yla "[s]"
set mytics 4
p \
  'PG3-event-mode-scale-0.1' u 1:2 w lp ti "0.25x" ls 100, \
  '' u 1:3 w lp ti "0.5x" ls 200, \
  '' u 1:4 w lp ti "default binning" ls 300, \
  '' u 1:5 w lp ti "2x" ls 400, \
  '' u 1:6 w lp ti "4x" ls 500, \
  '' u 1:7 w lp ti "8x" ls 700, \
  '' u 1:8 w lp ti "16x" ls 800, \
  '' u 1:9 w lp ti "32x" ls 900

f(x)=a/x+b
fit f(x) 'PG3-event-mode-scale-0.1' u 1:4 via a,b
pixels = 24798
# Bin range given in characterization file, for default binning:
bins = log(2.2/0.1)/0.0004
print(bins*pixels/a)

set xtics (0.25, 0.5, 1,2,4,8,16,32)
set xla "bin count relative to default SNSPowderReduction"
set xra [0:9]
set key t l

p \
  "< cat results/PG3-event-mode-scale-0.1 | grep '\^1 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0/4):1 ti "1 rank", \
  "< cat results/PG3-event-mode-scale-0.1 | grep '\^2 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0/4):1 ti "2 ranks", \
  "< cat results/PG3-event-mode-scale-0.1 | grep '\^4 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0/4):1 ti "4 ranks", \
  "< cat results/PG3-event-mode-scale-0.1 | grep '\^8 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0/4):1 ti "8 ranks"

set title "ISIS SANS reduction for SANS2D"
f1(x)=a/x+b
f16(x)=a16/x+b16
f32(x)=2*a16/x+b32
fit [:5] f1(x) 'SANS2D-event-mode' u 1:2 via a,b
fit [:5] f16(x) 'SANS2D-event-mode' u 1:6 via a16,b16
fit [:5] f32(x) 'SANS2D-event-mode' u 1:7 via b32
print(b32-b16) # constant cost per 16x base binning (is this for final Q?)
pixels = 120000
bins = (12.5-1.5)/0.125 # This is just the WAV binning, what about Q?
qbins = (0.0126-0.001)/0.001 + log(0.2/0.126)/0.08
print(qbins)
print(bins*pixels/a)

set key t r
set au x
set au y
set yra [0:]
set xla "MPI ranks"
set yla "[s]"
p \
  'SANS2D-event-mode' u 1:2 w lp ti "default binning" ls 100, \
  '' u 1:3 w lp ti "default binning" ls 200, \
  '' u 1:4 w lp ti "default binning" ls 300, \
  '' u 1:5 w lp ti "default binning" ls 400, \
  '' u 1:6 w lp ti "default binning" ls 500, \
  '' u 1:7 w lp ti "default binning" ls 600, f32(x), f16(x)

set xtics (1,2,4,8,16,32)
set xla "bin count relative to default SANS2D"
set key t l

p \
  "< cat data/SANS2D-histogram-mode | grep '\^1 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1 ti "1 rank", \
  "< cat data/SANS2D-histogram-mode | grep '\^2 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1 ti "2 ranks", \
  "< cat data/SANS2D-histogram-mode | grep '\^4 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1 ti "4 ranks", \
  "< cat data/SANS2D-histogram-mode | grep '\^8 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1 ti "8 ranks"

p \
  "< cat data/SANS2D-event-mode | grep '\^1 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1 ti "1 rank", \
  "< cat data/SANS2D-event-mode | grep '\^2 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1 ti "2 ranks", \
  "< cat data/SANS2D-event-mode | grep '\^4 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1 ti "4 ranks", \
  "< cat data/SANS2D-event-mode | grep '\^8 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1 ti "8 ranks"

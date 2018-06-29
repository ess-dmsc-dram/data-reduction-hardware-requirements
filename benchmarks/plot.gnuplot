set term pdf size 8,6
set outp "influence-of-bin-count.pdf"

set loadpath "data"

set yra [0:]
set xla "MPI ranks"
set yla "[s]"

set title "SNSPowderReduction for PG3"
p \
  'PG3-event-mode' u 1:2 w lp ti "default binning" ls 100, \
  '' u 1:3 w lp ti "default binning" ls 200, \
  '' u 1:4 w lp ti "default binning" ls 300, \
  '' u 1:5 w lp ti "default binning" ls 400, \
  '' u 1:6 w lp ti "default binning" ls 500, \
  '' u 1:7 w lp ti "default binning" ls 700, \
  '' u 1:8 w lp ti "default binning" ls 800, \
  '' u 1:9 w lp ti "default binning" ls 900

set title "ISIS SANS reduction for SANS2D"
p \
  'SANS2D-histogram-mode' u 1:2 w lp ti "default binning" ls 100, \
  '' u 1:3 w lp ti "default binning" ls 200, \
  '' u 1:4 w lp ti "default binning" ls 300, \
  '' u 1:5 w lp ti "default binning" ls 400, \
  '' u 1:6 w lp ti "default binning" ls 500, \
  '' u 1:7 w lp ti "default binning" ls 600

#set log x
#set log y 2
set xtics (0.25, 0.5, 1,2,4,8,16,32)
set xla "bin count relative to default SNSPowderReduction"
set xra [0:9]
set key t l

p \
  "< cat data/PG3-event-mode | grep '\^1 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0/4):1 ti "1 rank", \
  "< cat data/PG3-event-mode | grep '\^2 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0/4):1 ti "2 ranks", \
  "< cat data/PG3-event-mode | grep '\^4 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0/4):1 ti "4 ranks", \
  "< cat data/PG3-event-mode | grep '\^8 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0/4):1 ti "8 ranks"

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

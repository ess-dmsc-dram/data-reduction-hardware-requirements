set term pdf size 8,6
set outp "influence-of-bin-count.pdf"

set yra [0:]
set xla "MPI ranks"
set yla "[s]"
#set title "SNSPowderReduction for PG3"
#p \
#  'SNSPowderReduction-2018-06-28/binning-0.004'   u 1:6 w lp ti "773 bins" ls 100, \
#  'SNSPowderReduction-2018-06-28/binning-0.0004'  u 1:6 w lp ti "7728 bins" ls 210, \
#  'SNSPowderReduction-2018-06-28/binning-0.00004' u 1:6 w lp ti "77276 bins" ls 320
set title "ISIS SANS reduction for SANS2D"
p \
  'SANS2D-histogram-mode' u 1:2 w lp ti "default binning" ls 100, \
  '' u 1:3 w lp ti "default binning" ls 200, \
  '' u 1:4 w lp ti "default binning" ls 300, \
  '' u 1:5 w lp ti "default binning" ls 400, \
  '' u 1:6 w lp ti "default binning" ls 500, \
  '' u 1:7 w lp ti "default binning" ls 600

set xtics (1,2,4,8,16,32)
set xla "bin count relative to default SANS2D"
set xra [0:33]

p \
  "< cat SANS2D-histogram-mode | grep '\^1 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1, \
  "< cat SANS2D-histogram-mode | grep '\^2 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1, \
  "< cat SANS2D-histogram-mode | grep '\^4 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1, \
  "< cat SANS2D-histogram-mode | grep '\^8 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1

p \
  "< cat SANS2D-event-mode | grep '\^1 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1, \
  "< cat SANS2D-event-mode | grep '\^2 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1, \
  "< cat SANS2D-event-mode | grep '\^4 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1, \
  "< cat SANS2D-event-mode | grep '\^8 ' | cut -d' ' -f2- | tr ' ' '\n'" u (2**$0):1

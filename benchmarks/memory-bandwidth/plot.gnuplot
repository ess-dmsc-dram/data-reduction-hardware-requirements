set term pdf size 8,4
set outp "memory-bandwidth.pdf"

set multiplot layout 1,2
set key b r

set yra [0:]

set xla "threads" offset 0,0.5
set yla "read bandwidth [GByte/s]" offset 1

p \
  "< cat pmbw-1-dimm | grep areasize=2147483648 | tr '=' ' ' | grep ScanRead256PtrUnrollLoop" u 12:($28/(2**30)) ti "1 DIMM" pt 4, \
  "< cat pmbw-2-dimm | grep areasize=2147483648 | tr '=' ' ' | grep ScanRead256PtrUnrollLoop" u 12:($28/(2**30)) ti "2 DIMM" pt 6, \
  "< cat pmbw-4-dimm | grep areasize=2147483648 | tr '=' ' ' | grep ScanRead256PtrUnrollLoop" u 12:($28/(2**30)) ti "4 DIMM" pt 8

set key t r
set xla "MPI ranks" offset 0,0.5
set yla "SNSPowderReduction runtime [s]"
set xra [:12.5]
#p \
#  "PG3-event-mode-scale-0.1-1-dimm" u 1:2 lc 1 dt 1 ti "1 DIMM small data", \
#  "PG3-event-mode-scale-0.1-2-dimm" u 1:2 lc 2 dt 1 ti "2 DIMM small data", \
#  "PG3-event-mode-scale-0.1-4-dimm" u 1:2 lc 3 dt 1 ti "4 DIMM small data"
#p \
#  "PG3-event-mode-scale-1.0-1-dimm" u 1:2 lc 1 dt 2 ti "1 DIMM medium data", \
#  "PG3-event-mode-scale-1.0-2-dimm" u 1:2 lc 2 dt 2 ti "2 DIMM medium data", \
#  "PG3-event-mode-scale-1.0-4-dimm" u 1:2 lc 3 dt 2 ti "4 DIMM medium data"
p \
  "PG3-event-mode-scale-4.0-1-dimm" u 1:2 ti "1 DIMM" pt 4, \
  "PG3-event-mode-scale-4.0-2-dimm" u 1:2 ti "2 DIMM" pt 6, \
  "PG3-event-mode-scale-4.0-4-dimm" u 1:2 ti "4 DIMM" pt 8
unset multiplot

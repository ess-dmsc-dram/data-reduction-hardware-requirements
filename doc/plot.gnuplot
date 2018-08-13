set term pdf size 8,4
set outp "reduction-time-requirement.pdf"

Tmin=30
speedup=5
rate_min=2e6

min(x,y)=x<y?x:y
max(x,y)=x<y?y:x

Treduction(event_rate,Trun)=max(Tmin, min(Trun/speedup, event_rate*Trun/rate_min))

set log x
set log y 2
set xra [10:10000]
set key outside
set xla "run duration [s]"
set yla "required maximum reduction duration [s]" offset 1

set style fill pattern 1

plot \
  Treduction(rate_min/speedup, x) noti w filledcurves above x2 ls 2 lc rgb "grey", \
  30 noti with filledcurves below x1 ls 2 lc rgb "grey", \
  for [i=0:5] Treduction(10000*(2**i), x) ti "".(10*(2**i))."k events/s" ls i+1, \
  Treduction(rate_min/speedup, x) ti sprintf("above %1.0fk events/s", rate_min/speedup/1000) lc 7 lw 2


reset
set term pdf size 6,4
set outp "accelerator-power.pdf"

set xla "year"
set yla "accelerator power [MW]"
set xra [2022.5:2029.5]
set yra [:5.5]
set key t l
p \
  "accelerator_power" u 1:($1<2027?$2:1/0) ti "data from Science Retreat 2018 slides" pt 5, \
  "" u 1:2 ti "extrapolation" pt 4 lc 1

reset
set term pdf size 8,10
set outp "live-reduction-no-mpi.pdf"
Rlive(event_rate,pixels)=(2*(10**12))/(event_rate*pixels)
framerate(event_rate,pixels)=(9*(10**7)*300000)/(event_rate*pixels)

set xra [0:5]
set yra [1:1000]
set samples 1000
set xla "MW" offset 0,1
set log y
set yla "R_{live}" offset 2
set multiplot layout 3,2
set title "LoKI" offset 0,-0.5
p \
  Rlive(1e7*x/5,   1500000) w l ti "3m-high-flux", \
  Rlive(3.33e5*x/5,1500000) w l ti "3m-small-sample", \
  Rlive(1.92e6*x/5,1500000) w l ti "5m-high-flux", \
  Rlive(1.2e5*x/5, 1500000) w l ti "5m-small-sample", \
  Rlive(7.5e5*x/5, 1500000) w l ti "8m-high-flux", \
  Rlive(4.69e4*x/5,1500000) w l ti "8m-small-sample"
set title "ESTIA"
p \
  Rlive(1e8*x/5, 500000) w l ti "reference-high-flux", \
  Rlive(4e6*x/5, 500000) w l ti "reference-normal", \
  Rlive(2e6*x/5, 500000) w l ti "specular-high-flux", \
  Rlive(8e5*x/5, 500000) w l ti "specular", \
  Rlive(8e5*x/5, 500000) w l ti "off-specular"
set title "CSPEC"
p \
  Rlive(1e7*x/5, 750000) w l ti "RRM", \
  Rlive(1e6*x/5, 750000) w l ti "normal"
set title "MAGIC"
p \
  Rlive(1e7*x/5, 2880000) w l ti "high-flux", \
  Rlive(1e6*x/5, 2880000) w l ti "normal"
set title "DREAM"
p \
  Rlive(7.5e7*x/5, 12000000) w l ti "high-flux", \
  Rlive(1e7*x/5,   12000000) w l ti "medium-resolution", \
  Rlive(1.3e6*x/5, 12000000) w l ti "high-resolution"
set title "BEER"
p \
  Rlive(5e7*x/5, 400000) w l ti "high-flux-multiplexing", \
  Rlive(2e6*x/5, 400000) w l ti "medium-resolution-multiplexing", \
  Rlive(3e5*x/5, 400000) w l ti "medium-resolution"
#set title "BIFROST"
#p \
#  Rlive(1e6*x/5, 5000) w l ti "high-flux", \
#  Rlive(1e5*x/5, 5000) w l ti "average"
unset multiplot


reset
set term pdf size 8,4
set outp "interactive-ram.pdf"

set xra[1e7:1e10]
set log x
set yra [16:]
set log y 2
set key outside
set xla "N_{event}" offset 0,1
set yla "GByte" offset 2

interactive_ram(Nspec, Nbin, Nevent)=2 + (Nspec*256 + 10*(24*Nspec*Nbin + 16*Nevent))/(2**30)
# Using a 10x scale in Nspec for BIFROST for scanning.
p \
  interactive_ram(400000, 8500, x)  w l lc 1 dt 1 ti 'BEER-medium-flux', \
  interactive_ram(400000, 2000, x)  w l lc 1 dt 2 ti 'BEER-high-flux', \
  interactive_ram(50000, 850, x)    w l lc 2 dt 1 ti 'BIFROST-average', \
  interactive_ram(50000, 110, x)    w l lc 2 dt 2 ti 'BIFROST-high-flux', \
  interactive_ram(750000, 1000, x)  w l lc 3 dt 1 ti 'CSPEC', \
  interactive_ram(12000000, 71000, x) w l lc 4 dt 1 ti 'DREAM-high-resolution', \
  interactive_ram(12000000, 10000, x) w l lc 4 dt 2 ti 'DREAM-medium', \
  interactive_ram(12000000, 1420, x)  w l lc 4 dt 3 ti 'DREAM-high-flux', \
  interactive_ram(500000, 450, x)     w l lc 5 dt 1 ti 'ESTIA', \
  interactive_ram(1500000, 240, x)    w l lc 6 dt 1 ti 'LoKI', \
  interactive_ram(2880000, 7100, x)   w l lc 7 dt 1 ti 'MAGIC'

#set xra[1e5:2e7]
#set log x
#set yra [10:20000]
#set log y
#set xtics nomirror
#set log x2
#set x2ra[1e5:2e7]
#set x2tics ("BEER" 400000, "CSPEC"  750000, "DREAM" 12000000, "ESTIA" 500000, "LoKI" 1500000, "MAGIC" 2880000) rotate by 90 scale 2
#set key outside
#set xla "N_{spec}"
#set yla "GByte" offset 2
#
#interactive_ram(Nspec, Nbin, Nevent)=2 + (Nspec*256 + 10*(24*Nspec*Nbin + 16*Nevent))/(2**30)
#p \
#  interactive_ram(x, 200, 1e8)   w l lc 1 dt 1, \
#  interactive_ram(x, 2000, 1e8)  w l lc 1 dt 2, \
#  interactive_ram(x, 20000, 1e8) w l lc 1 dt 3, \
#  interactive_ram(x, 200, 1e9)   w l lc 2 dt 1, \
#  interactive_ram(x, 2000, 1e9)  w l lc 2 dt 2, \
#  interactive_ram(x, 20000, 1e9) w l lc 2 dt 3, \
#  interactive_ram(x, 200, 1e10)   w l lc 3 dt 1, \
#  interactive_ram(x, 2000, 1e10)  w l lc 3 dt 2, \
#  interactive_ram(x, 20000, 1e10) w l lc 3 dt 3


#set pm3d map
#set xra [1e5:1e8]
#set yra [1e5:1e7]
#set log x
#set log y
##set yla "events/s"
##set yra [1e4:1e8]
##set cblabel "time to reduce data [s]"
#set log cb
#set cbrange [1:1000]
#set zra [1:1000]
#set samples 100; set isosamples 100
##set lmargin at screen 0.15
##set rmargin at screen 0.80
##set title "10 cores, B-max 5e7"
#set contour base
#set cntrparam levels discrete 14
#splot framerate(x,y)


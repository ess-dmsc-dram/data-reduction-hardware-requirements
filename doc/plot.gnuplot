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

#set pm3d map
#set yla "events/s"
#set yra [1e4:1e8]
#set cblabel "time to reduce data [s]"
#set log cb
#set samples 100; set isosamples 100
#set lmargin at screen 0.15
#set rmargin at screen 0.80
#set title "10 cores, B-max 5e7"
##set contour base
#splot Treduction(y,x)


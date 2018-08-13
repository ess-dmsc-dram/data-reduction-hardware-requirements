f(Npixel, Nevent) = a / (Npixel * Nevent)
a=3*10**13

fit f(x,y) 'live-timings' u 1:2:3 via a

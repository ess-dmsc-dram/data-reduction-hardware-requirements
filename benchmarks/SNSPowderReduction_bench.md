## SNSPowderReduction benchmark

The `SNSPowderReduction` workflow was run using 1-10 cpus, and `grow.py` factors from 1-20.

The `grow.py` script is used to artificially increase the number of events in a data file.
Growing the data is actually quite time-consuming, so the `loop_make_SNSPowderReduction_files.sh` 
file was created to run only the data generation. This is done once and for all and does not need 
to be carried out every time the benchmark is run, the data in simply stored on disk (~85Gb). Note 
that the disk is a classical HDD (Seagate Desktop HDD ST2000DM001 - 2 TB - SATA 6Gb/s - 7200 rpm).

The `SNSPowderReduction-binning.sh` script contains a loop over `grow` factor and number of cpus.
Figure 1 shows the scaling performance of the workflow. Machine used: HP Z820 workstation (12 
cores: 2x Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz)

![Figure 1](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/SNSPowderReduction_bench.png)

**Figure 1:** Panel (b) shows that a larger number of events leads to a better speedup, which is expected as the 
size of the parallel portion of the computational work increases. The times per event in panel (d) 
go below 0.1 &mu;s for NCPU > ~4 as long as the number of events is high enough.

The timings from panel (e) are taken from Mantid directly (i.e. what is prints out in the log) for
the `FilterBadPulses` algorithm. This was then simply divided by the number of events.

The number of bins here was 7728.

The table containing the data is `SNSPowderReduction_bench.txt`:

```
# Run no. NCPU factor Runtime Nevents1 Nevents2 t_filter_1 t_filter_2 t_filter_3
  1.000  1.000  1.000  46.714  17926980.000  65836865.000  0.950  2.510  0.450  
  2.000  2.000  1.000  24.924  17926980.000  65836865.000  0.410  1.360  0.240  
  3.000  3.000  1.000  18.154  17926980.000  65836865.000  0.260  0.890  0.170  
  4.000  4.000  1.000  14.325  17926980.000  65836865.000  0.200  0.660  0.140  
  5.000  5.000  1.000  12.670  17926980.000  65836865.000  0.170  0.570  0.120  
  6.000  6.000  1.000  11.376  17926980.000  65836865.000  0.140  0.470  0.110  
  7.000  7.000  1.000  10.520  17926980.000  65836865.000  0.120  0.420  0.100  
  8.000  8.000  1.000  9.850  17926980.000  65836865.000  0.110  0.370  0.100  
  9.000  9.000  1.000  9.557  17926980.000  65836865.000  0.100  0.350  0.090  
  .      .      .      .          .            .           .      .      .
  .      .      .      .          .            .           .      .      .
  .      .      .      .          .            .           .      .      .
199.000  9.000  20.000  48.400  358539600.000  1316737300.000  0.630  3.110  0.120  
200.000  10.000  20.000  45.403  358539600.000  1316737300.000  0.570  2.770  0.100 
```

The columns represent (in order):
0: Run number
1: Number of CPUs
2: `grow` factor
3: Workflow runtime
4: Number of events in 77777 file
5: Number of events in 88888 (Vanadium) file
6: Time for filtering bad pulses from 77777 file
7: Time for filtering bad pulses from 88888 file
8: Time for filtering bad pulses from 99999 file


### Profiling the workflow

We use the timings given my Mantid to get a rough profiling of the workflow. The percentage of time
spent in each part of the workflow is shown in figure 2

![Figure 2](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/timings.png)

**Figure 2:** The left panel shows a linear percentage scale, while it is logarithmic in the right
panel. You can also download a [pdf](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/timings.pdf) version of the figure.




**TODO:** change the number of bins, get the workflow to use `FilterEvents`.


**Notes on using more than 10 CPUs**:

For a reason I have not been able to determine, the workflow won't run on 11 or 12 (or even 16) 
CPUs. It just halts at `AlignAndFocusPowder-[Warning] null output` after starting 
`DiffractionFocussing`. All the CPUs are still working, at 100% but the workflow never progresses.
This behaviour is independent of the size of the data to process (i.e. the number of events).

I also don't fully understand why some of the time during the workflow execution individual CPU 
usages go to ~200% when I set `MultiThreaded.MaxCores=1` in `Mantid.user.properties`.
```
top - 11:00:16 up 6 days, 19:17,  1 user,  load average: 1.03, 0.69, 1.56
Tasks: 421 total,   1 running, 276 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.8 us,  0.7 sy,  0.0 ni, 93.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 65894044 total, 27160064 free,  7158324 used, 31575656 buff/cache
KiB Swap:  2097148 total,  1720176 free,   376972 used. 61295564 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND                                                                                  
25593 nvaytet   20   0 4180404 2.952g 109100 S 147.0  4.7   0:35.13 python                                                                                   
 1216 root      20   0 1119040 234272 202652 S   1.7  0.4 181:16.52 Xorg                                                                                     
  311 nvaytet   20   0 1314136  87524  15820 S   1.3  0.1  35:24.84 mate-terminal                                                                            
```

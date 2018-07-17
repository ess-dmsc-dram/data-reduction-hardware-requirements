## SNSPowderReduction benchmark:

The `SNSPowderReduction` workflow was run using 1-10 cpus, and `grow.py` factors from 1-20.

The `grow.py` script is used to artificially increase the number of events in a data file.
Growing the data is actually quite time-consuming, so the `loop_make_SNSPowderReduction_files.sh` 
file was created to run only the data generation. This is done once and for all and does not need 
to be carried out every time the benchmark is run, the data in simply stored on disk (~85Gb). Note 
that the disk is a classical 

The `SNSPowderReduction-binning.sh` script contains a loop over `grow` factor and number of cpus.
Figure 1 shows the scaling performance of the workflow. Machine used: HP Z820 workstation (12 
cores: 2x Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz)

![Figure 1](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/SNSPowderReduction_bench.png)

Panel (b) shows that a larger number of events leads to a better speedup, which is expected as the 
size of the parallel portion of the computational work increases. The times per event in panel (d) 
go below 0.1 &mu;s for NCPU > ~4 as long as the number of events is high enough.

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





**TODO:** change the number of bins, get the workflow to use `FilterEvents`.


**Notes on using more than 10 CPUs**:

For a reason I have not been able to determine, the workflow won't run on 11 or 12 (or even 16) 
CPUs. It just halts at `AlignAndFocusPowder-[Warning] null output` after starting 
`DiffractionFocussing`. All the CPUs are still working, at 100% but the workflow never progresses.


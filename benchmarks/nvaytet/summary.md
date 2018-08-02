# Summary of filtering benchmarks

## SNSPowderReduction

The `SNSPowderReduction` workflow was run using 1-10 cpus, and `grow.py` factors from 1-20.

The `grow.py` script is used to artificially increase the number of events in a data file.
Growing the data is actually quite time-consuming, so the `loop_make_SNSPowderReduction_files.sh` 
file was created to run only the data generation. This is done once and for all and does not need 
to be carried out every time the benchmark is run, the data in simply stored on disk (~85Gb). Note 
that the disk is a classical HDD (Seagate Desktop HDD ST2000DM001 - 2 TB - SATA 6Gb/s - 7200 rpm).

The file sizes are listed in the table below

| Grow factor | Main file (77777) | Vanadium run (88888) | Vanadium background (99999) | Total |
| ----------- |------------------ | ---------------------| --------------------------- | ----- |
|  1          | 113M              |  392M                |  58M                        | 563M  |
|  2          | 195M              |  696M                |  66M                        | 960M  |
|  3          | 280M              | 1004M                |  74M                        | 1.4G  |
|  4          | 362M              |  1.3G                |  82M                        | 1.8G  |
|  5          | 446M              |  1.6G                |  90M                        | 2.2G  |
|  6          | 529M              |  1.9G                |  98M                        | 2.5G  |
|  7          | 613M              |  2.2G                | 106M                        | 2.9G  |
|  8          | 695M              |  2.5G                | 114M                        | 3.3G  |
|  9          | 780M              |  2.8G                | 122M                        | 3.7G  |
| 10          | 863M              |  3.1G                | 130M                        | 4.1G  |
| 11          | 947M              |  3.4G                | 138M                        | 4.5G  |
| 12          | 1.1G              |  3.7G                | 146M                        | 4.9G  |
| 13          | 1.1G              |  4.0G                | 154M                        | 5.3G  |
| 14          | 1.2G              |  4.3G                | 162M                        | 5.6G  |
| 15          | 1.3G              |  4.6G                | 170M                        | 6.0G  |
| 16          | 1.4G              |  4.9G                | 177M                        | 6.4G  |
| 17          | 1.5G              |  5.2G                | 186M                        | 6.8G  |
| 18          | 1.5G              |  5.5G                | 194M                        | 7.2G  |
| 19          | 1.6G              |  5.8G                | 202M                        | 7.6G  |
| 20          | 1.7G              |  6.1G                | 210M                        | 8.0G  |

The `SNSPowderReduction-binning.sh` script contains a loop over `grow` factor and number of cpus.
Figure 1 shows the scaling performance of the workflow. Machine used: HP Z820 workstation (12 
cores: 2x Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz)

![Figure 1](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/nvaytet/SNSPowderReduction/SNSPowderReduction_bench.png)

**Figure 1:** Panel (b) shows that a larger number of events leads to a better speedup, which is expected as the 
size of the parallel portion of the computational work increases. The times per event in panel (d) 
go below 0.1 &mu;s for NCPU > ~4 as long as the number of events is high enough.

The timings from panel (e) are taken from Mantid directly (i.e. what is prints out in the log) for
the `FilterBadPulses` algorithm. This was then simply divided by the number of events.

The number of bins for panels (a)-(e) was 7728.

The table containing the data (for just 7728 bins) is `SNSPowderReduction_bench.txt`:

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


### Varying the number of bins

![Figure 2](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/nvaytet/SNSPowderReduction/SNSPowderReduction_bins.png)

Panel (a) shows the dependence of the workflow runtime on the number of bins, from 7728 to 247284.
Panel (b) shows the number of bins processes per second per core (using the total workflow
runtime). **This probably should be improved by using the time spent working with histograms  rather than total workflow time.**

What is the reason for the poor scaling with number of bins? Panel (b) shows significantly worse 
results for 10 CPUs compared to 1.

The table containing the variable number of bins data is `SNSPowderReduction_bins_bench.txt`.



### Profiling the workflow

We use the timings given my Mantid to get a rough profiling of the workflow. The percentage of time
spent in each part of the workflow is shown in figure 2

![Figure 3](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/nvaytet/SNSPowderReduction/timings.png)

**Figure 2:** The left panel shows a linear percentage scale, while it is logarithmic in the right
panel. You can also download a [pdf](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/timings.pdf) version of the figure.

This was done for the largest file, with a `grow` factor of 20.


**TODO:** ~~change the number of bins~~, get the workflow to use `FilterEvents`.  


### Notes on using more than 10 CPUs [SOLVED]

For a reason I have not been able to determine, the workflow won't run on 11 or 12 (or even 16) 
CPUs. It just halts at `AlignAndFocusPowder-[Warning] null output` after starting 
`DiffractionFocussing`. All the CPUs are still working, at 100% but the workflow never progresses.
This behaviour is independent of the size of the data to process (i.e. the number of events).

**Update:** setting in the Mantid.user.properties file
```
logging.channels.fileFilterChannel.level=
```
solves this problem (thanks Simon!).

### Notes on using only one thread

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

## FilterEvents

The examples from the `FilterEvents` [documentation page](http://docs.mantidproject.org/nightly/algorithms/FilterEvents-v1.html) were benchmarked. The input file used was grown to contain 1122660000 events (1.7GB on disk).

The following timings for 1 CPU were obtained.

**1. File loading:** 68.98s

**2. Example 1 - Filtering event without correction on TOF:** `151.39s`

Output:
```
workspace tempsplitws_0 has 1240000 events
workspace tempsplitws_1 has 169151818 events
workspace tempsplitws_2 has 100088182 events
workspace tempsplitws_3 has 69620000 events
workspace tempsplitws_4 has 225199163 events
workspace tempsplitws_5 has 51330837 events
workspace tempsplitws_unfiltered has 506030000 events
```

**3. Example 2 - Filtering event by a user-generated TableWorkspace:** `20.24s`

Output:
```
workspace tempsplitws3_a has 775800000 events
event splitter log: entry 0 and entry 1 are 2010-03-25T16:08:37Z and 2010-03-25T16:10:17Z.
workspace tempsplitws3_b has 0 events
event splitter log: entry 0 and entry 1 are 2010-03-25T16:08:37Z and 2010-03-25T16:11:57Z.
workspace tempsplitws3_c has 0 events
event splitter log: entry 0 and entry 1 are 2010-03-25T16:08:37Z and 2010-03-25T16:15:17Z.
workspace tempsplitws3_unfiltered has 346860000 events
event splitter log: entry 0 and entry 1 are 2010-03-25T16:08:37Z and 2010-03-25T16:10:17Z.
```

**4. Example 3 - Filtering event by pulse time:** `33.50s`

Output:
```
workspace tempsplitws_1 has 1230000 events
workspace tempsplitws_2 has 169510000 events
workspace tempsplitws_3 has 99720000 events
workspace tempsplitws_4 has 70190000 events
workspace tempsplitws_5 has 225290000 events
workspace tempsplitws_6 has 50670000 events
```

**5. Example 4 - Filtering event with correction on TOF:** `16.59s`

Output:
```
workspace tempsplitws_0 has 1230000 events
workspace tempsplitws_1 has 169510000 events
workspace tempsplitws_2 has 99720000 events
workspace tempsplitws_3 has 70190000 events
workspace tempsplitws_4 has 225140924 events
workspace tempsplitws_5 has 50819076 events
workspace tempsplitws_unfiltered has 506050000 events
```

**6. Example 2 - Modified:** `154.63s`

Looking at the results of Example 2, two output workspaces contained no data. The filtering limits were modified to
```
split_table_ws.addRow([0., 33., 'a'])
split_table_ws.addRow([34., 66., 'b'])
split_table_ws.addRow([67., 99., 'c'])
split_table_ws.addRow([100., 650., 'b'])
```
and the scripts now outputs
```
workspace tempsplitws3_a has 420970733 events
event splitter log: entry 0 and entry 1 are 2010-03-25T16:08:37Z and 2010-03-25T16:09:10Z.
workspace tempsplitws3_b has 453660950 events
event splitter log: entry 0 and entry 1 are 2010-03-25T16:08:37Z and 2010-03-25T16:09:11Z.
workspace tempsplitws3_c has 230740000 events
event splitter log: entry 0 and entry 1 are 2010-03-25T16:08:37Z and 2010-03-25T16:09:44Z.
workspace tempsplitws3_unfiltered has 17288317 events
event splitter log: entry 0 and entry 1 are 2010-03-25T16:08:37Z and 2010-03-25T16:09:10Z.
```

**Note:** the run time has significantly increased from 20s to 155s.


## Other tests

I also tried running two more workflows and ran into issues.

### SANS2D-binning.sh

A script, that calls `run_SANS2DMinimalBatchReductionSlicedTest_V2.py` runs fine with 1 CPU but for 2 CPUs and above, it just hangs at
```
LoadInstrument-[Notice] LoadInstrument successful, Duration 0.03 seconds
```
after also printing out the error
```
Traceback (most recent call last):
  File "./run_SANS2DMinimalBatchReductionSlicedTest_V2.py", line 26, in <module>
    BatchReduce(BATCHFILE, '.nxs', saveAlgs={}, combineDet='rear')
  File "/home/nvaytet/work/mantid/MPI/mpi-build/scripts/SANS/sans/command_interface/ISISCommandInterface.py", line 911, in BatchReduce
    use_reduction_mode_as_suffix=use_reduction_mode_as_suffix)
  File "/home/nvaytet/work/mantid/MPI/mpi-build/scripts/SANS/sans/command_interface/ISISCommandInterface.py", line 783, in WavRangeReduction
    state = director.process_commands()
  File "/home/nvaytet/work/mantid/MPI/mpi-build/scripts/SANS/sans/command_interface/command_interface_state_director.py", line 127, in process_commands
    data_state = self._get_data_state()
  File "/home/nvaytet/work/mantid/MPI/mpi-build/scripts/SANS/sans/command_interface/command_interface_state_director.py", line 148, in _get_data_state
    file_information = file_information_factory.create_sans_file_information(file_name)
  File "/home/nvaytet/work/mantid/MPI/mpi-build/scripts/SANS/sans/common/file_information.py", line 1043, in create_sans_file_information
    raise NotImplementedError("The file type you have provided is not implemented yet.")
```

### HYSPECReductionTest.sh

Taken from the system tests, I tried to use this workflow as it makes use of `FilterEvents`, but this failed on more than one CPU, saying that the algorithm does not support distributed workspaces

```
FilterByLogValue-[Notice] FilterByLogValue started
GenerateEventsFilter-[Warning] Algorithm does not support execution with input workspaces of the following storage types: 
GenerateEventsFilter-[Warning] InputWorkspace Parallel::StorageMode::Distributed
```

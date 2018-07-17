**SNSPowderReduction benchmark:**

The `SNSPowderReduction` workflow was run using 1-10 cpus, and `grow.py` factors from 1-20.
For a reason I have not been able to determine, the workflow won't run on 11 or 12 CPUs. It just 
halts at `AlignAndFocusPowder-[Warning] null output` after starting `DiffractionFocussing`.

The `grow.py` script is used to artificially increase the number of events in a data file.
Growing the data is actually quite time-consuming, so the `loop_make_SNSPowderReduction_files.sh` 
file was created to run only the data generation. This is done once and for all and does not need 
to be carried out every time the benchmark is run, the data in simply stored on disk (~85Gb).

The `SNSPowderReduction-binning.sh` script contains a loop over `grow` factor and number of cpus.
Figure 1 shows the scaling performance of the workflow. Machine used: HP Z820 workstation (12 
cores: 2x Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz)

![Figure 1](https://raw.githubusercontent.com/nvaytet/data-reduction-hardware-requirements/master/benchmarks/SNSPowderReduction_bench.png)

Panel (b) shows that a larger number of events leads to a better speedup, which is expected as the 
size of the parallel portion of the computational work increases. The times per event in panel (d) 
go below 0.1 &mu;s for NCPU > ~4 as long as the number of events is high enough.

The number of bins here was 7728.

**TODO:** change the number of bins, get the workflow to use `FilterEvents`.

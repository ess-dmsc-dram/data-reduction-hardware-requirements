import os
cwd = os.getcwd()

import sys
factor = float(sys.argv[1])
run_file = str(sys.argv[2])

from mantid.simpleapi import SNSPowderReduction
from mantid import config

# Adopted from SNSPowderRedux.PG3Analysis
ref_file  = "PG3_4844_reference.gsa"
cal_file  = "PG3_FERNS_d4832_2011_08_24.cal"
try:
    char_file = str(sys.argv[3])
except IndexError:
    char_file = "PG3_characterization_2011_08_31-HR.txt"

SNSPowderReduction(Filename=run_file,
                   PreserveEvents=False,
                   CalibrationFile=cal_file,
                   CharacterizationRunsFile=char_file,
                   LowResRef=15000, RemovePromptPulseWidth=50,
                   Binning=-0.0004/factor, BinInDspace=True, FilterBadPulses=95,
                   SaveAs="gsas and fullprof and pdfgetn", OutputDirectory=cwd + '/data',
                   FinalDataUnits="dSpacing")

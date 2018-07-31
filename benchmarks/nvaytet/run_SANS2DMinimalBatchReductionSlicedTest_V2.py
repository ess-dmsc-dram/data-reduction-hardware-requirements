import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--user-file", type=str, default='', help='ISIS SANS2D user file to configure the reduction.')
parser.add_argument('-e', '--event-mode', action='store_true', help='Use event mode reduction instead of legacy reduction which converts to histograms early.')
args = parser.parse_args()

# Adapted from SANS2DSlicingTest_V2.SANS2DMinimalBatchReductionSlicedTest_V2

from mantid.api import (AnalysisDataService, FileFinder)
from sans.command_interface.ISISCommandInterface import (SANS2D, MaskFile, BatchReduce, SetEventSlices,
                                                         UseCompatibilityMode, AssignSample, AssignCan,
                                                         TransmissionSample, TransmissionCan, WavRangeReduction)

MASKFILE = args.user_file
BATCHFILE = FileFinder.getFullPath('sans2d_reduction_gui_batch.csv')

# Compatibility mode converts to histograms earlier.
# If enabled use something like the following line in MASKFILE to define binning:
# L/EVENTSTIME 7000.0,500.0,60000.0
if not args.event_mode:
    UseCompatibilityMode()
SANS2D()
MaskFile(MASKFILE)
SetEventSlices("0.0-451, 5-10")
BatchReduce(BATCHFILE, '.nxs', saveAlgs={}, combineDet='rear')

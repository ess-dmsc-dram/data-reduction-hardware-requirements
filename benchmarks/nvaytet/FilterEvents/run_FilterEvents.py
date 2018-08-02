from mantid.simpleapi import *
from mantid import config
import numpy as np
import time

divider = "==============================================="

#====================================================
# Load the Nexus file
#====================================================

print(divider)

print("File loading started")
time0  = time.time()
ws = Load(Filename='CNCS_7777_event.nxs')
time1  = time.time()
print("File loading complete")
print(divider)

print("Total Events, Load time: %i %.2f" % (ws.getNumberEvents(),(time1-time0)))

print(divider)

#====================================================
# Example 1 - Filtering event without correction on TOF
#====================================================

splitws, infows = GenerateEventsFilter(InputWorkspace=ws, UnitOfTime='Nanoseconds', LogName='SampleTemp',
        MinimumLogValue=279.9,  MaximumLogValue=279.98, LogValueInterval=0.01)

print("Calling FilterEvents")
time2  = time.time()
FilterEvents(InputWorkspace=ws, SplitterWorkspace=splitws, InformationWorkspace=infows,
        OutputWorkspaceBaseName='tempsplitws',  GroupWorkspaces=True,
        FilterByPulseTime = False, OutputWorkspaceIndexedFrom1 = False,
        CorrectionToSample = "None", SpectrumWithoutDetector = "Skip", SplitSampleLogs = False,
        OutputTOFCorrectionWorkspace='mock')
time3  = time.time()
print("FilterEvents complete")

# Print result
wsgroup = mtd["tempsplitws"]
wsnames = wsgroup.getNames()
for name in sorted(wsnames):
    tmpws = mtd[name]
    print("workspace %s has %d events" % (name, tmpws.getNumberEvents()))
    DeleteWorkspace(tmpws)

print("Example 1 Filter time: %.2f" % ((time3-time2)))

DeleteWorkspace(splitws)

print(divider)

#====================================================
# Example 2 - Filtering event by a user-generated TableWorkspace
#====================================================

# create TableWorkspace
split_table_ws = CreateEmptyTableWorkspace()
split_table_ws.addColumn('float', 'start')
split_table_ws.addColumn('float', 'stop')
split_table_ws.addColumn('str', 'target')

split_table_ws.addRow([0., 100., 'a'])
split_table_ws.addRow([200., 300., 'b'])
split_table_ws.addRow([400., 600., 'c'])
split_table_ws.addRow([600., 650., 'b'])

# filter events
time2  = time.time()
FilterEvents(InputWorkspace=ws, SplitterWorkspace=split_table_ws,
        OutputWorkspaceBaseName='tempsplitws3',  GroupWorkspaces=True,
        FilterByPulseTime = False, OutputWorkspaceIndexedFrom1 = False,
        CorrectionToSample = "None", SpectrumWithoutDetector = "Skip", SplitSampleLogs = False,
        OutputTOFCorrectionWorkspace='mock',
        RelativeTime=True)
time3  = time.time()

# Print result
wsgroup = mtd["tempsplitws3"]
wsnames = wsgroup.getNames()
for name in sorted(wsnames):
    tmpws = mtd[name]
    print("workspace %s has %d events" % (name, tmpws.getNumberEvents()))
    split_log = tmpws.run().getProperty('splitter')
    entry_0 = np.datetime_as_string(split_log.times[0].astype(np.dtype('M8[s]')), timezone='UTC')
    entry_1 = np.datetime_as_string(split_log.times[1].astype(np.dtype('M8[s]')), timezone='UTC')
    print('event splitter log: entry 0 and entry 1 are {0} and {1}.'.format(entry_0, entry_1))
    DeleteWorkspace(tmpws)

print("Example 2 Filter time: %.2f" % ((time3-time2)))

DeleteWorkspace(split_table_ws)

print(divider)

#====================================================
# Example 3 - Filtering event by pulse time
#====================================================

splitws, infows = GenerateEventsFilter(InputWorkspace=ws, UnitOfTime='Nanoseconds', LogName='SampleTemp',
        MinimumLogValue=279.9,  MaximumLogValue=279.98, LogValueInterval=0.01)

time2  = time.time()
FilterEvents(InputWorkspace=ws,
    SplitterWorkspace=splitws,
    InformationWorkspace=infows,
    OutputWorkspaceBaseName='tempsplitws',
    GroupWorkspaces=True,
    FilterByPulseTime = True,
    OutputWorkspaceIndexedFrom1 = True,
    CorrectionToSample = "None",
    SpectrumWithoutDetector = "Skip",
    SplitSampleLogs = False,
    OutputTOFCorrectionWorkspace='mock')
time3  = time.time()

# Print result
wsgroup = mtd["tempsplitws"]
wsnames = wsgroup.getNames()
for name in sorted(wsnames):
    tmpws = mtd[name]
    print("workspace %s has %d events" % (name, tmpws.getNumberEvents()))
    DeleteWorkspace(tmpws)

print("Example 3 Filter time: %.2f" % ((time3-time2)))

DeleteWorkspaces([splitws,infows])

print(divider)

#====================================================
# Example 4 - Filtering event with correction on TOF
#====================================================

splitws, infows = GenerateEventsFilter(InputWorkspace=ws, UnitOfTime='Nanoseconds', LogName='SampleTemp',
        MinimumLogValue=279.9,  MaximumLogValue=279.98, LogValueInterval=0.01)

time2  = time.time()
FilterEvents(InputWorkspace=ws, SplitterWorkspace=splitws, InformationWorkspace=infows,
    OutputWorkspaceBaseName='tempsplitws',
    GroupWorkspaces=True,
    FilterByPulseTime = False,
    OutputWorkspaceIndexedFrom1 = False,
    CorrectionToSample = "Direct",
    IncidentEnergy=3,
    SpectrumWithoutDetector = "Skip",
    SplitSampleLogs = False,
    OutputTOFCorrectionWorkspace='mock')
time3  = time.time()

# Print result
wsgroup = mtd["tempsplitws"]
wsnames = wsgroup.getNames()
for name in sorted(wsnames):
    tmpws = mtd[name]
    print("workspace %s has %d events" % (name, tmpws.getNumberEvents()))
    DeleteWorkspace(tmpws)

print("Example 4 Filter time: %.2f" % ((time3-time2)))

DeleteWorkspaces([splitws,infows])

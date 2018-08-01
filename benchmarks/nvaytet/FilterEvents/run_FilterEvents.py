
import mantid.simpleapi as api
from mantid import config

## Adopted from SNSPowderRedux.PG3Analysis
#ref_file  = "PG3_4844_reference.gsa"
#cal_file  = "PG3_FERNS_d4832_2011_08_24.cal"
#try:
    #char_file = str(sys.argv[3])
#except IndexError:
    #char_file = "PG3_characterization_2011_08_31-HR.txt"

#SNSPowderReduction(Filename=run_file,
                   #PreserveEvents=False,
                   #CalibrationFile=cal_file,
                   #CharacterizationRunsFile=char_file,
                   #LowResRef=15000, RemovePromptPulseWidth=50,
                   #Binning=-0.0000004/factor, BinInDspace=True, FilterBadPulses=95,
                   #SaveAs="gsas and fullprof and pdfgetn", OutputDirectory=cwd + '/data',
                   #FinalDataUnits="dSpacing")






ws = api.Load(Filename='CNCS_7777_event.nxs')
splitws, infows = api.GenerateEventsFilter(InputWorkspace=ws, UnitOfTime='Nanoseconds', LogName='SampleTemp',
        MinimumLogValue=279.9,  MaximumLogValue=279.98, LogValueInterval=0.01)

api.FilterEvents(InputWorkspace=ws, SplitterWorkspace=splitws, InformationWorkspace=infows,
        OutputWorkspaceBaseName='tempsplitws',  GroupWorkspaces=True,
        FilterByPulseTime = False, OutputWorkspaceIndexedFrom1 = False,
        CorrectionToSample = "None", SpectrumWithoutDetector = "Skip", SplitSampleLogs = False,
        OutputTOFCorrectionWorkspace='mock')


# Print result
wsgroup = api.mtd["tempsplitws"]
wsnames = wsgroup.getNames()
for name in sorted(wsnames):
    tmpws = api.mtd[name]
    print("workspace %s has %d events" % (name, tmpws.getNumberEvents()))

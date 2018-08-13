#!/bin/bash

# Important: Need to enable pipefail to capture return value of Mantid in command with pipe below.
set -o pipefail

MANTID=~/software/mantid-mpi/bin/mantidpython
SCRIPT="./run_SNSPowderReduction.py"
RESULTS="memory-bandwidth"
EVENT_SCALE=$1
SUFFIX=$2
HIST_FILE=$RESULTS/PG3-histogram-mode
EVENT_FILE=$RESULTS/PG3-event-mode-scale-"$EVENT_SCALE"-$SUFFIX
PWD=$(pwd)

# Create data files with the requested number of events.
DATA="data"
./make_SNSPowderReduction_files.sh ~/build/mantid-mpi/ExternalData/Testing/Data/SystemTest/ $DATA $EVENT_SCALE
RUN_FILE=$DATA/PG3_77777_event.nxs

# Create characterization files that links the run file to its vanadium run and empty run.
CHAR_FILE=$PWD/$DATA/PG3_characterization_2011_08_31-HR.txt
echo "#S 1 characterization runs\n
#L frequency(Hz) center_wavelength(angstrom) bank_num vanadium_run empty_run vanadium_back d_min(angstrom) d_max(angstrom)\n
60 0.533  1 88888 0 99999 0.10  2.20 00000.00 16666.67" > $CHAR_FILE

# Append our data path to the Mantid search path.
CONFIG=~/.mantid/Mantid.user.properties
cp $CONFIG $CONFIG.backup
trap "mv $CONFIG.backup $CONFIG" INT
DATA_SEARCH_DIRS=$(cat $CONFIG | grep ^datasearch.directories)";$PWD/$DATA"
cat $CONFIG | grep -v ^datasearch.directories > $CONFIG.new
mv $CONFIG.new $CONFIG
echo $DATA_SEARCH_DIRS >> $CONFIG

mkdir -p $RESULTS
rm -f $HIST_FILE
rm -f $EVENT_FILE

for i in $(seq 1 12)
do
  line_event="$i"
  line_histogram="$i"
  for bin_scale in 1.0
  do
    seconds=$(\time -f %e mpirun -n $i $MANTID --classic $SCRIPT $bin_scale $RUN_FILE $CHAR_FILE 2>&1 | tail -n 1)
    if [ $? -ne 0 ]
    then
      echo "Mantid exited with a non-zero status, aborting."
      mv $CONFIG.backup $CONFIG
      exit 1
    fi
    line_event=$line_event" "$seconds
  done
  echo $line_event | tee -a $EVENT_FILE
done
mv $CONFIG.backup $CONFIG

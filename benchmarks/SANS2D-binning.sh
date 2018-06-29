#!/bin/sh

# Important: Need to enable pipefail to capture return value of Mantid in command with pipe below.
set -o pipefail

MANTID=~/software/mantid-mpi/bin/mantidpython
SCRIPT="./run_SANS2DMinimalBatchReductionSlicedTest_V2.py"
CONFIG=$(mktemp)
RESULTS="results"
HIST_FILE=$RESULTS/SANS2D-histogram-mode
EVENT_FILE=$RESULTS/SANS2D-event-mode

mkdir -p $RESULTS
rm -f $HIST_FILE
rm -f $EVENT_FILE

for i in $(seq 1 12)
do
  line_event="$i"
  line_histogram="$i"
  for bin_scale in 0.5 1 2 4 8 16 32
  do
    python create_user_file.py $bin_scale > $CONFIG
    seconds=$(\time -f %e mpirun -n $i $MANTID --classic $SCRIPT --user-file $CONFIG --event-mode 2>&1 | tail -n 1)
    if [ $? -ne 0 ]
    then
      echo "Mantid exited with a non-zero status, aborting."
      mv $CONFIG.backup $CONFIG
      exit 1
    fi
    line_event=$line_event" "$seconds
    seconds=$(\time -f %e mpirun -n $i $MANTID --classic $SCRIPT --user-file $CONFIG 2>&1 | tail -n 1)
    if [ $? -ne 0 ]
    then
      echo "Mantid exited with a non-zero status, aborting."
      mv $CONFIG.backup $CONFIG
      exit 1
    fi
    line_histogram=$line_histogram" "$seconds
  done
  echo $line_histogram | tee -a $HIST_FILE
  echo $line_event | tee -a $EVENT_FILE
done

rm $CONFIG

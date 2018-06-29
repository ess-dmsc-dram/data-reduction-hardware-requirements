#!/bin/sh

MANTID="/home/simon/software/mantid-mpi/bin/mantidpython"
SCRIPT="./run_SANS2DMinimalBatchReductionSlicedTest_V2.py"
CONFIG=$(mktemp)
DIR="data"
HIST_FILE=$DIR/SANS2D-histogram-mode
EVENT_FILE=$DIR/SANS2D-event-mode

mkdir -p $DIR
rm -f $HIST_FILE
rm -f $EVENT_FILE

for i in $(seq 1 12)
do
  line_event="$i"
  line_histogram="$i"
  for bin_scale in 1 2 4 8 16 32
  do
    python create_user_file.py $bin_scale > $CONFIG
    seconds=$(\time -f %e mpirun -n $i $MANTID --classic $SCRIPT --user-file $CONFIG --event-mode 2>&1 | tail -n 1)
    line_event=$line_event" "$seconds
    seconds=$(\time -f %e mpirun -n $i $MANTID --classic $SCRIPT --user-file $CONFIG 2>&1 | tail -n 1)
    line_histogram=$line_histogram" "$seconds
  done
  echo $line_histogram | tee -a $HIST_FILE
  echo $line_event | tee -a $EVENT_FILE
done

rm $CONFIG

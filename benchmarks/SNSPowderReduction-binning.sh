#!/bin/bash

# Important: Need to enable pipefail to capture return value of Mantid in command with pipe below.
set -o pipefail

MANTID=~/software/mantid-mpi/bin/mantidpython
SCRIPT="./run_SNSPowderReduction.py"
DATA="data"
DIR="data-test"
HIST_FILE=$DIR/PG3-histogram-mode
EVENT_FILE=$DIR/PG3-event-mode
EVENT_SCALE=$1
RUN_FILE=$DATA/PG3_4844_event.nxs
PWD=$(pwd)
CHAR_FILE=$PWD/$DATA/PG3_characterization_2011_08_31-HR.txt

mkdir -p $DATA

CONFIG=~/.mantid/Mantid.user.properties
cp $CONFIG $CONFIG.backup
trap "mv $CONFIG.backup $CONFIG" INT
DATA_SEARCH_DIRS=$(cat $CONFIG | grep ^datasearch.directories)";$PWD/$DATA"
cat $CONFIG | grep -v ^datasearch.directories > $CONFIG.new
mv $CONFIG.new $CONFIG
echo $DATA_SEARCH_DIRS >> $CONFIG

# cp PG3_4866_event.nxs PG3_99999_event.nxs
# python ~/code/nexus-sandbox/scripts/grow.py -s 0.1 -f PG3_99999_event.nxs
# h5repack -i PG3_99999_event.nxs -o PG3_99999_event-rechunked.nxs -l CHUNK=8192
# mv PG3_99999_event-rechunked.nxs PG3_99999_event.nxs

echo "#S 1 characterization runs\n
#L frequency(Hz) center_wavelength(angstrom) bank_num vanadium_run empty_run vanadium_back d_min(angstrom) d_max(angstrom)\n
60 0.533  1 99999 0 88888 0.10  2.20 00000.00 16666.67" > $CHAR_FILE
#60 0.533  1 4866 0 5226 0.10  2.20 00000.00 16666.67" > $CHAR_FILE

mkdir -p $DIR
rm -f $HIST_FILE
rm -f $EVENT_FILE

for i in $(seq 11 12)
do
  line_event="$i"
  line_histogram="$i"
  for bin_scale in 1 #0.25 #0.5 1 2 4 8 16 32
  do
    mpirun -n $i $MANTID --classic $SCRIPT $bin_scale $RUN_FILE $CHAR_FILE
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

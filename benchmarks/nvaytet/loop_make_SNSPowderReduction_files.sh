#!/bin/bash


# Create data files with the requested number of events.

for j in $(seq 10 20); do

  DATA="data_fact$(printf "%03d" $j)"

  EVENT_SCALE=$j

  # ./make_SNSPowderReduction_files.sh ~/build/mantid-mpi/ExternalData/Testing/Data/SystemTest/ $DATA $EVENT_SCALE
  ./make_SNSPowderReduction_files.sh /home/nvaytet/work/mantid/branches/2018/build/ExternalData/Testing/Data/SystemTest $DATA $EVENT_SCALE &

done

exit
  

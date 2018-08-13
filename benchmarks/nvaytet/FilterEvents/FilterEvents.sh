#!/bin/bash

#=========================================================
# Use in the following way:
# ./FilterEvents.sh | tee bench_log.txt
#=========================================================


MANTID=/home/nvaytet/work/mantid/MPI/mpi-build/bin/mantidpython
# MANTID=/home/nvaytet/work/mantid/branches/current-build/bin/mantidpython
SCRIPT="./run_FilterEvents.py"

mpirun -n 1 $MANTID --classic $SCRIPT;

# for i in $(seq 1 12)
# do

#   STARTTIME=$(python -c 'import time; print int(time.time()*1000)');
#   mpirun -n 1 $MANTID --classic $SCRIPT;
#   ENDTIME=$(python -c 'import time; print int(time.time()*1000)');
#   milliseconds=$(($ENDTIME - $STARTTIME));
#   echo "NCPUs and runtime : $i  $milliseconds";

#   if [ $? -ne 0 ]
#   then
#     echo "Mantid exited with a non-zero status, aborting."
#   #         mv $CONFIG.backup $CONFIG
#     exit 1
#   fi

# done

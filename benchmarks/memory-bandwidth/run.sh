#!/bin/bash

DIMMS=$1
SUFFIX="$DIMMS"-dimm

~/software/pmbw/pmbw  -f 256PtrUnroll -M 4294967296 -s 1073741824 -S 4294967296 -o pmbw-$SUFFIX
cd ..
./SNSPowderReduction.sh 0.1 $SUFFIX
./SNSPowderReduction.sh 1.0 $SUFFIX
./SNSPowderReduction.sh 4.0 $SUFFIX

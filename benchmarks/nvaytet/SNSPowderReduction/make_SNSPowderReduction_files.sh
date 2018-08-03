#!/bin/bash

SOURCE=$1
DATA=$2
SCALE=$3

mkdir -p $DATA
cd $DATA

cp $SOURCE/PG3_4844_event.nxs PG3_77777_event.nxs
cp $SOURCE/PG3_4866_event.nxs PG3_88888_event.nxs
cp $SOURCE/PG3_5226_event.nxs PG3_99999_event.nxs

for i in 77777 88888 99999
do
  echo $i;
#   python ~/code/nexus-sandbox/scripts/grow.py -s $SCALE -f PG3_"$i"_event.nxs
  python ~/work/mantid/nexus-sandbox/scripts/grow.py -s $SCALE -f PG3_"$i"_event.nxs
  h5repack -i PG3_"$i"_event.nxs -o PG3_"$i"_event-rechunked.nxs -l CHUNK=8192
  mv PG3_"$i"_event-rechunked.nxs PG3_"$i"_event.nxs
done

FILE=$1;
SCALE=$2;

python ~/work/mantid/nexus-sandbox/scripts/grow.py -s ${SCALE} -f ${FILE};
h5repack -i ${FILE} -o ${FILE}_rechunked -l CHUNK=8192;
mv ${FILE}_rechunked ${FILE};

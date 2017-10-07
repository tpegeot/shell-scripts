#!/bin/ksh
# Author : Thomas Pegeot
# Description : scans a batch of pages with ADF and converts it to multiple pdf files

TMP_DIR=/tmp/scan
PDF_DIR=/media/documents/commun/scan

[ -d $TMP_DIR ] || mkdir $TMP_DIR
cd $TMP_DIR
scanimage -y 297 -x 210 -b --batch-scan=yes --source ADF --format tiff --mode color --resolution 300dpi
for file in $(find $TMP_DIR -name '*.tif')
do
  input=$(basename $file .tif)
  output=$(print "${input}$(date +%s).pdf")
  #tiff2pdf -o ${PDF_DIR}/${output} -p A4 $file
  #tiff2pdf -o ${PDF_DIR}/${output} -p A4 -j -q 90 $file
  #probleme avec tiff2pdf lors de compression jpg : image rose
  convert -page A4 -compress jpeg -quality 90% $file ${PDF_DIR}/${output}
  rm $file
done

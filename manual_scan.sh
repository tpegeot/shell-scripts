#!/bin/ksh

TMP_DIR=/tmp/scan
PDF_DIR=/media/documents/commun/scan

[ -d $TMP_DIR ] || mkdir $TMP_DIR
cd $TMP_DIR
scanimage -y 297 -x 210 --batch-scan=no --source Flatbed --format tiff --mode color --resolution 300dpi > scan.tif
#scanimage -y 297 -x 210 --batch-scan=no --source Flatbed --format tiff --mode gray --resolution 300dpi > scan.tif
for file in $(find $TMP_DIR -name '*.tif')
do
  input=$(basename $file .tif)
  output=$(print "${input}$(date +%s).pdf")
  #tiff2pdf -o ${PDF_DIR}/${output} -p A4 $file
  #tiff2pdf -o ${PDF_DIR}/${output} -p A4 -j -q 90 $file
  #probleme avec tiff2pdf lors de compression jpg : image rose
  #convert -page A4 -compress jpeg -quality 90% $file ${PDF_DIR}/${output}
  convert -compress jpeg -quality 90% $file ${PDF_DIR}/${output}
  rm $file
done

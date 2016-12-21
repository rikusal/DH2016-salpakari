#!/bin/bash
 
tif=".tif"
emp="_"
for tiffile in $(\ls originaltif $filenames)
do
   scenes=$(\identify originaltif/$tiffile | wc -l) #scenes = the number of scenes in the tif
   echo $scenes
   processedScenes=0
   while [ $processedScenes -lt $scenes ] #processedScenes < scenes
   do
      ind="[$processedScenes]"
      scenetif=${tiffile//$tif/$emp}$processedScenes$tif
      echo $tiffile$ind
      echo $scenetif
      convert originaltif/$tiffile$ind separatedtif/$scenetif  
      processedScenes=$(( $processedScenes + 1 ))
   done
done

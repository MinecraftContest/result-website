#!/bin/sh

for filepath in output/*.zip; do
    rm -rf convert_tmp/
    unzip $filepath -d convert_tmp/
    ./j2b -i convert_tmp/world/ -o convert_tmp/converted/
    filename=$(basename -- $filepath)
    filename="${filename%.*}"
    echo $filename
    rm -rf convert_tmp/world/
    cd convert_tmp/converted/
    zip -r "../../output/$filename.mcworld" *
    cd ../../
done

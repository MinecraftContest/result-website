#!/bin/sh

for filepath in output/*.zip; do
    rm -rf convert_tmp/
    unzip $filepath -d convert_tmp/
    ./j2b -i convert_tmp/world/ -o convert_tmp/converted/
    filename = $(basename -- $filepath)
    echo $filename
    # zip -r ../../output/test.mcworld *
    break
done

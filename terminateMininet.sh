#!/bin/bash

for i in 2 3 4
do

    sleep 200m

    pkill -f random60nodes.py
    pkill -f main.py
    pkill -f SimpleHTTPServer

    mn -c

    mkdir selectionLayer/wired/random/r$i
    mkdir selectionLayer/wired/random/r$i/gwChange
    mv selection_* selectionLayer/wired/random/r$i/gwChange


    mkdir selectionLayer/wired/random/r$i/download
    mv download_* selectionLayer/wired/random/r$i/download
done
#!/bin/bash

for i in 3 4 5 6 7 8 9
do          
    sleep 205m
    
    pkill -f random60nodes.py
    pkill -f main.py
    pkill -f SimpleHTTPServer

    mn -c

    mkdir selectionLayer/combine/wired/gateselect/r$i
    mkdir selectionLayer/combine/wired/gateselect/r$i/gwChange
    mv selection_* selectionLayer/combine/wired/gateselect/r$i/gwChange


    mkdir selectionLayer/combine/wired/gateselect/r$i/download
    mv download_* selectionLayer/combine/wired/gateselect/r$i/download
    
    python random60nodes.py &
done
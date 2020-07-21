#!/bin/bash

for i in 8 9
do          
    sleep 205m
    
    pkill -f test_mobility_multiAP.py
    pkill -f main.py
    pkill -f SimpleHTTPServer

    mn -c

    mkdir selectionLayer/combine/mobility/gateselect/r$i
    mkdir selectionLayer/combine/mobility/gateselect/r$i/gwChange
    mv selection_* selectionLayer/combine/mobility/gateselect/r$i/gwChange


    mkdir selectionLayer/combine/mobility/gateselect/r$i/download
    mv download_* selectionLayer/combine/mobility/gateselect/r$i/download
    
    python test_mobility_multiAP.py
done
#!/bin/bash

for i in 10 11
do          
    sleep 205m
    
    pkill -f test_multiAP.py
    pkill -f main.py
    pkill -f SimpleHTTPServer

    mn -c

    mkdir selectionLayer/combine/wireless/greedy/r$i
    mkdir selectionLayer/combine/wireless/greedy/r$i/gwChange
    mv selection_* selectionLayer/combine/wireless/greedy/r$i/gwChange


    mkdir selectionLayer/combine/wireless/greedy/r$i/download
    mv download_* selectionLayer/combine/wireless/greedy/r$i/download
    
    python test_multiAP.py
done
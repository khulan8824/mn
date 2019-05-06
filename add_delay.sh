#!/bin/bash

sleep 20m
tc qdisc add dev h93-eth0 root netem delay 200ms


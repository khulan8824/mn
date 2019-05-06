#!/bin/bash
sleep 40m
tc qdisc del dev h93-eth0 root netem

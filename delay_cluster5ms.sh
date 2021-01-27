#
#!/bin/bash

tc qdisc add dev ens18 root handle 1: prio

tc filter add dev ens18 protocol ip parent 1: prio 2 u32 match ip dst 10.139.40.115 flowid 1:2

tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.131 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.132 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.133 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.134 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.135 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.136 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.137 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.138 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.139 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.140 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.141 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.142 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.143 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.144 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.145 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.146 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.147 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.148 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.149 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.150 flowid 1:3

tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.145.32.66 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.138.57.2 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.138.85.130 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.37.194 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.138.25.67 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.228.192.210 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.228.193.210 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.228.204.9 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.138.129.98 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.140.150.227 flowid 1:3

tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.101 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.102 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.103 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.104 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.105 flowid 1:1

tc qdisc add dev ens18 parent 1:3 handle 30: netem delay 2ms
tc qdisc add dev ens18 parent 1:2 handle 20: netem delay 0ms
tc qdisc add dev ens18 parent 1:1 handle 10: netem delay 5ms

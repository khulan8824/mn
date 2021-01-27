#
#!/bin/bash

tc qdisc add dev ens18 root handle 1: prio
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.206 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.207 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.208 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.209 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.210 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.211 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.212 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.213 flowid 1:1
tc filter add dev ens18 protocol ip parent 1: prio 1 u32 match ip dst 10.139.40.214 flowid 1:1


tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.215 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.216 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.217 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.218 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.219 flowid 1:3
tc filter add dev ens18 protocol ip parent 1: prio 3 u32 match ip dst 10.139.40.220 flowid 1:3

tc filter add dev ens18 protocol ip parent 1: prio 2 u32 match ip dst 10.139.40.201 flowid 1:2
tc filter add dev ens18 protocol ip parent 1: prio 2 u32 match ip dst 10.139.40.202 flowid 1:2
tc filter add dev ens18 protocol ip parent 1: prio 2 u32 match ip dst 10.139.40.203 flowid 1:2
tc filter add dev ens18 protocol ip parent 1: prio 2 u32 match ip dst 10.139.40.204 flowid 1:2
tc filter add dev ens18 protocol ip parent 1: prio 2 u32 match ip dst 10.139.40.205 flowid 1:2

tc qdisc add dev ens18 parent 1:1 handle 10: netem delay 3ms
tc qdisc add dev ens18 parent 1:3 handle 30: netem delay 5ms
tc qdisc add dev ens18 parent 1:2 handle 20: netem delay 0ms

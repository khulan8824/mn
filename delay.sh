#
#!/bin/bash

interface=ens18
ip=(10.139.40.206 10.139.40.207 10.139.40.208 10.139.40.209 10.139.40.210 10.139.40.211 10.139.40.212 10.139.40.13 10.139.40.214 )
delay=3ms
tc qdisc add dev $interface root handle 2: prio
for i in "${ip[@]}"
do
    tc filter add dev $interface parent 1:0 protocol ip prio 1 u32 match ip dst $i flowid 2:1
    tc qdisc add dev $interface parent 1:1 handle 2: netem delay $delay
done

ip=(10.139.40.215 10.139.40.216 10.139.40.217 10.139.40.218 10.139.40.219 10.139.40.220)
delay=5ms
for i in "${ip[@]}"
do
    #tc qdisc add dev $interface root handle 1: prio
    tc filter add dev $interface parent 2:0 protocol ip prio 1 u32 match ip dst $i flowid 2:1
    tc qdisc add dev $interface parent 2:1 handle 2: netem delay $delay
done
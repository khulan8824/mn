#
#!/bin/bash

interface=ens18
ip=(10.139.40.206 10.139.40.207 10.139.40.208 10.139.40.209 10.139.40.210 10.139.40.211 10.139.40.212 10.139.40.13 10.139.40.214 )
delay=3ms
tc qdisc add dev $interface root handle 1: prio
tc class add dev $interace parent 1: classid 1:1 prio
tc class add dev $interface parent 1:1 classid 1:11 prio netem delay 3ms
tc class add dev $interface parent 1:1 classid 1:12 prio netem delay 5ms


tc filter add dev $interface parent 1:11 protocol ip prio 1 u32 match ip dst 10.139.40.206 flowid 1:11
tc filter add dev $interface parent 1:12 protocol ip prio 1 u32 match ip dst 10.139.40.215 flowid 1:12

tc qdisc add dev $interface parent 1:11 handle 10: netem delay 3ms
tc qdisc add dev $interface parent 1:12 handle 20: netem delay 5ms


#tc filter add dev $interface parent 1:0 protocol ip prio 1 u32 match ip dst 10.139.40.206 flowid 2:1
#tc qdisc add dev $interface parent 1:1 handle 2: netem delay $delay
#done

#ip=(10.139.40.215 10.139.40.216 10.139.40.217 10.139.40.218 10.139.40.219 10.139.40.220)


#tc qdisc add dev eth1 handle 1: root htb r2q 1700

#tc class add dev eth1 parent 1: classid 1:1 htb rate 100Mbps ceil 100Mbps
#tc class add dev eth1 parent 1:1 classid 1:11 htb rate 100Mbps
#tc class add dev eth1 parent 1:1 classid 1:12 htb rate 100Mbps

#tc filter add dev eth1 parent 1: protocol ip prio 1 u32 match ip src 10.0.1.0/24 flowid 1:11
#tc filter add dev eth1 parent 1: protocol ip prio 1 u32 match ip src 20 10.0.2.0/24 flowid 1:12
#tc qdisc add dev eth1 parent 1:11 handle 10: netem trace testpattern1.bin 0 1
#tc qdisc add dev eth1 parent 1:12 handle 20: netem trace testpattern2.bin 100 0
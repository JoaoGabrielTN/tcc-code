#!/bin/bash
PROTO=("TCP" "UDP")
PACKET_SIZE=(100 300 500)

for r in {1..10}; do
    for ip in 192.168.0.{2..10}; do
        for prot in "${PROTO[@]}"; do
            for ps in "${PACKET_SIZE[@]}"; do
                time=$(shuf -i 10-60 -n 1)
                echo "[$(date)] Round $r: Testing $ip with $prot, packet size: $ps, duration: ${time}s"
                
                if [ "$prot" == "TCP" ]; then
                    iperf3 -c "$ip" -t "$time" -l "$ps"
                else 
                    iperf3 -c "$ip" -u -t "$time" -l "$ps"
                fi
                sleep 2
            done
        done
    done
done

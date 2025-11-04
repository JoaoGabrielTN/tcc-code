#!/bin/bash
PROTO=("TCP" "UDP")
PACKET_SIZE=(100 300 500)
LOG_FILE="iperf_test_$(date +%Y%m%d_%H%M%S).log"

for r in {1..100}; do
    for ip in 192.168.0.{1..10}; do
        for prot in "${PROTO[@]}"; do
            for ps in "${PACKET_SIZE[@]}"; do
                time=$(shuf -i 10-60 -n 1)
                echo "[$(date)] Round $r: Testing $ip with $prot, packet size: $ps, duration: ${time}s" | tee -a "$LOG_FILE"
                
                if [ "$prot" == "TCP" ]; then
                    iperf3 -c "$ip" -t "$time" -l "$ps" 2>&1 | tee -a "$LOG_FILE"
                else 
                    iperf3 -c "$ip" -u -t "$time" -l "$ps" 2>&1 | tee -a "$LOG_FILE"
                fi
                echo "----------------------------------------" | tee -a "$LOG_FILE"
                sleep 2  # Add small delay between tests
            done
        done
    done
done

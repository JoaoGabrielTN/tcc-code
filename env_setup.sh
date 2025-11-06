tmux new-session -s mn -d
tmux new-session -s tshark -d

tmux send-keys -t mn:0 'sudo python3 tcc_topo.py' Enter
sleep 40

while true; do
    if ip link show hwsim0 2>/dev/null | grep -q "state UNKNOWN"; then
        echo "Interface hwsim0 está UP"
        break
    else
        echo "Interface hwsim0 não está UP, tentando levantar..."
        tmux send-keys -t mn:0 'sh ifconfig hwsim0 up' Enter
        sleep 5  # Aguarda 5 segundos antes de verificar novamente
    fi
done

for i in {2..10}; do
	tmux send-keys -t mn:0 'car${i} iperf3 -s &' Enter
done

tmux send-keys -t tshark:0 'tshark -i hwsim0 -w benign.pcap' Enter

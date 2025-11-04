tmux new-session -s mn -d
tmux new-session -s tshark -d

tmux send-keys -t mn:0 'sudo python3 tcc_topo.py' Enter
sleep 40
tmux send-keys -t mn:0 'sh ifconfig hwsim0 up' Enter
tmux send-keys -t tshark:0 'tshark -i hwsim0 -w benign.pcap' Enter

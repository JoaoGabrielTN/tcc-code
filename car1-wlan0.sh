echo "Automating car1 wlan interface"
while true; do
	STATE=$(ip a | grep 'car[0-9]-wlan0' | grep 'state DOWN')
	if [[ $STATE != "" ]]; then
		iw dev car1-wlan0 connect vanet-ssid
		sleep 2
	fi
done

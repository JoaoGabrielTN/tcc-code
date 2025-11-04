#!/bin/bash
echo "Automating car wlan interfaces (car[0-9]*-wlan0)"

while true; do
    # Get all car interfaces that are in DOWN state - fixed regex to handle car10, car11, etc.
    DOWN_INTERFACES=$(ip link show | grep -E 'car[0-9]+-wlan0:' | grep 'state DOWN' | awk -F: '{print $2}' | tr -d ' ')
    
    if [[ -n "$DOWN_INTERFACES" ]]; then
        echo "Found down interfaces: $DOWN_INTERFACES"
        
        # Process each down interface
        while IFS= read -r interface; do
            if [[ -n "$interface" ]]; then
                echo "Bringing up interface: $interface"
                
                # Bring interface up first
                ip link set "$interface" up
                sleep 2
                
                # Then try to connect
                iw dev "$interface" connect vanet-ssid
                
                # Wait and check if it worked
                sleep 3
                CURRENT_STATE=$(ip link show "$interface" 2>/dev/null | grep -o 'state [A-Z]*' | awk '{print $2}')
                if [[ "$CURRENT_STATE" == "UP" ]]; then
                    echo "Successfully brought up $interface"
                else
                    echo "Failed to bring up $interface, current state: $CURRENT_STATE"
                    # Additional debugging
                    echo "Interface details:"
                    ip link show "$interface" 2>/dev/null || echo "Interface not found"
                fi
            fi
        done <<< "$DOWN_INTERFACES"
    else
        echo "All car interfaces are up - $(date)"
    fi
    
    sleep 5
done

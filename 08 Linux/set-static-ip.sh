#! /bin/sh
sudo ip addr add 192.168.99.1/24 dev enp3s0
ip addr show enp3s0

sudo iptables -A FORWARD -s 192.168.99.0/24 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -t nat -F POSTROUTING
sudo iptables -t nat -A POSTROUTING -o wlp5s0 -j MASQUERADE

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

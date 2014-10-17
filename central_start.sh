#!/usr/bin/sudo /bin/bash
SERVICE=`service network-manager status | grep "stop/waiting" | cut -d ' ' -f 2`
if [ -z $SERVICE ];
then
	echo "Network Manager Stop"
	sudo service network-manager stop
fi	
sudo ifconfig eth0 10.8.0.27

IP_ADDRESS="10.8.0.27"
PORT_NUM="5566"
NUM_OF_REFERENCE_NODE=4

./central.py $IP_ADDRESS $PORT_NUM $NUM_OF_REFERENCE_NODE 

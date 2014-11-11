#!/usr/bin/sudo /bin/bash
SERVICE=`service network-manager status | grep "stop/waiting" | cut -d ' ' -f 2`
if [ -z $SERVICE ];
then
	echo "Network Manager Stop"
	sudo service network-manager stop
fi	
sudo ifconfig eth0 10.8.0.27


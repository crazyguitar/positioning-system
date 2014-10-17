#!/usr/bin/sudo /bin/bash 

SERVICE=`service network-manager status | grep "stop/waiting" | cut -d ' ' -f 2`
if [ -z $SERVICE ];
then
	sudo service network-manager stop
fi

IWLMODULE=`lsmod | grep ^iwlwifi | awk '{print $1}'`
if [ -z $IWLMODULE ];
then
	sudo modprobe iwlwifi
	sleep 3
fi
../injection/setup_monitor_csi.sh 64 HT20


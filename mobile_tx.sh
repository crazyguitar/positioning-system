#!/usr/bin/sudo /bin/bash

SERVICE=`service network-manager status | grep "stop/waiting" | cut -d ' ' -f 2`
if [ -z $SERVICE ];
then
	sudo service network-manager stop
fi

./setup_inject.sh 64 HT20
echo 0x4101 | sudo tee `find /sys -name monitor_tx_rate`

while [ 1 ];
do
	sudo ../injection/random_packets 256 100 1 100
done


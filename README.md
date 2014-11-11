## Training Phase

### Experiment Setup

Connect central server, reference node(access point) and mobile to same switch.  

1. For Central Server:

```bash
$ ./central_start.sh
```

2. For Reference Node:
```bash
$ sudo ./reference_start.sh
$ sudo ./reference.py 10.8.0.27 5566
```

3. For Mobile Node: 
```bash
$ sudo ./mobile_start.sh
$ sudo ./mobile.py 10.8.0.27 5566
```
4. Protocol flow chart
```

					      Send Packet
__________________________________________________________________________________ Mobile node(TX)
\					        /     \                                               /
 \					       /       \											 /
GETREADY	            READY    SENDOVER                                   ALLSTOP
   \				     /           \                                         /
____\___________________/_____________\_______________________________________/__ Central Server
     \			    ////			   \          /     \         \          /
      \		  	   ////				    \        /       \         \        /
   STARTRECV  ACKFORSTART           STOPRECV  ACKFORSTOP FETCH log RM_LOG ACK
        \        ////					  \    /           \         \    /
_________\______////_______________________\__/_____________\_________\__/_______ Reference node(AP)
		  Prepare

```

## Testing Phase

### Experiment setup 

Connect central server, reference node(access point) and mobile to same switch.  
Reference Node need execute in order. 

1. For Central Server:

```bash
# ./central_sync_server.py <ip address> <port> <num_ap>
$ ./central_sync_server.py 10.8.0.27 5566 4
```	
2. For Reference Node:

```bash	
$ sudo ./reference_start.sh

# sudo ./reference_sync.py <ip address> <port> <ap index>
$ sudo ./reference_sync.py 10.8.0.27 5566 1 
```
3. For Mobile Node: 
```bash
$ ./mobile_tx.sh
```

4. protocol flow chart
```
							  SCP get log file
______________________________________________
\                  ////           /      /
 \                ////           /      /
 SYNC    ACK_FOR_END_COLLECT    / .... /
   \            ////           /      /
____\__________////___________/______/________
  Refer collect CSI

```

## Matlab Processing data

1. trainingScript.m

	This file provide example of how to use training function.

2. training.m

	This is a trainig function of matlab.
```matlab
	function tritraining(           ... 
		access_point_location_file, ... 
		training_location_file,     ... 
		log_file_info_dir,          ... 
		output_dir,                 ... 
		num_training,               ... 
		num_antenna                 ... 
	) 
```

3. tripositioningScript.m

	This file is positioning system part.

4. tripositioning.m

	This is a testing function of matlab 

All above files need to put into /path/to/linux-80211n-csitool-supplement/matlab



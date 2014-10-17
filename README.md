## Training Phase

### Experiment Setup

Connect central server, reference node(access point) and mobile to same switch.  

1. For Central Server:

	./central_start.sh

2. For Reference Node:

	sudo ./reference_start.sh <br /> 
	sudo ./reference.py 10.8.0.27 5566

3. For Mobile Node: 

	sudo ./mobile_start.sh	<br />
	sudo ./mobile.py 10.8.0.27 5566


<!--

					      Send Packet
______________________________________________________________ Mobile node(TX)
\					        /     \                    /
 \					       /       \                  /
GETREADY	            READY    SENDOVER         ALLSTOP
   \				     /           \              /
____\___________________/_____________\____________/__________ Central Server
     \			    ////			   \          /
      \		  	   ////				    \        /
   STARTRECV  ACKFORSTART            STOPRECV  ACKFORSTOP 
        \        ////					  \    /
_________\______////_______________________\__/_______________ Reference node(AP)
		  Prepare

-->

## Testing Phase

### Experiment setup 

Connect central server, reference node(access point) and mobile to same switch.  
Reference Node need execute in order. 

1. For Central Server:

	// ./central_sync_server.py &lt;ip_address&gt; &lt;port&gt; &lt;num_ap&gt; <br />
	./central_sync_server.py 10.8.0.27 5566 4
	
2. For Reference Node:
	
	// sudo ./reference_sync.py &lt;server_ip&gt; &lt;server_port&gt; &lt;ap_id&gt; <br />
	sudo ./reference_sync.py 10.8.0.27 5566 1 

3. For Mobile Node: 

	./mobile_tx.sh

<!-- 
							  SCP get log file
______________________________________________
\                  ////           /      /
 \                ////           /      /
 SYNC    ACK_FOR_END_COLLECT    / .... /
   \            ////           /      /
____\__________////___________/______/________
  Refer collect CSI
-->




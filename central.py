#!/usr/bin/python

import socket
import sys
import subprocess
import shlex


class CentralServer:

	def __init__(self, addr, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		self.sock.bind((addr, port))
		self.sock.listen(16)
		print "Server Start!"

class conn_client:

	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr

	def send_start_recv(self):
		self.conn.send("STARTRECV")
	
	def send_stop_recv(self):
		self.conn.send("STOPRECV")
	
	def send_remove_log(self):
		self.conn.send("REMOVELOG")

class mobi_client:

	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr

	def recv_command(self):
		recv_msg = self.conn.recv(256)
		return recv_msg

	def send_command(self, command):
		self.conn.send(command)
		
def download_log_file(ap, count, index):

	command = "scp mvnl@%s:~/linux-80211n-csitool-supplementary/lab_pos/tmp/log%d.dat ../log_file/AP%d" % (ap.addr[0], count , index)
	print command
	args = shlex.split(command)
	subprocess.call(args)
	

def main():

	server = CentralServer(sys.argv[1], int(sys.argv[2]))
	clientList = []
	connect_number = 0 

	while(connect_number != int(sys.argv[3])): 
		connect, address = server.sock.accept()
		clientList.append(conn_client(connect, address))
		connect_number += 1
		print 'Node: '+str(connect_number)+' connected'
	
	count = 96 
	while True: 
			
		connect, address = server.sock.accept()
		mobileNode = mobi_client(connect, address)
		print "Mobile Node Connected!"
		count += 1

		# Get ready 
		recv_msg = mobileNode.recv_command()
		print recv_msg
		for ap in clientList:
			ap.send_start_recv()	
			recv_ack = ap.conn.recv(256)
			# Recv ACK
			print recv_ack

		# Send over
		mobileNode.send_command("READY")
		recv_msg = mobileNode.recv_command()
		print recv_msg
		for ap in clientList:
			ap.send_stop_recv()
			recv_ack = ap.conn.recv(256)
			# Recv ACK
			print recv_ack

		# grab log file from all access point
		for i in range(len(clientList)):
			download_log_file(clientList[i], count, i+1)

		# send remove log file
		for ap in clientList:
			ap.send_remove_log()
			recv_ack = ap.conn.recv(256)
			# Recv ACK
			print recv_ack
		
		ACK_msg = "ALLSTOP Times: %d" % (count)
		mobileNode.send_command(ACK_msg)
		mobileNode.conn.close()
	
	server.sock.close()

if __name__ == "__main__":
	main()


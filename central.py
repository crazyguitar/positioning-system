#!/usr/bin/python

import socket
import sys


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

class mobi_client:

	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr

	def recv_command(self):
		recv_msg = self.conn.recv(256)
		return recv_msg

	def send_command(self, command):
		self.conn.send(command)

def main():

	server = CentralServer(sys.argv[1], int(sys.argv[2]))
	clientList = []
	connect_number = 0 

	while(connect_number != int(sys.argv[3])): 
		connect, address = server.sock.accept()
		clientList.append(conn_client(connect, address))
		connect_number += 1
		print 'Node: '+str(connect_number)+' connected'
	
	
	while True: 
			
		connect, address = server.sock.accept()
		mobileNode = mobi_client(connect, address)
		print "Mobile Node Connected!"

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
		mobileNode.send_command("ALLSTOP")
		mobileNode.conn.close()
	
	server.sock.close()

if __name__ == "__main__":
	main()


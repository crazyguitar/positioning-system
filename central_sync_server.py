#!/usr/bin/python

import socket
import sys
from thread import *
import time
import subprocess
import shlex

ACK = [0]*int(sys.argv[3])

class syncServer:

	def __init__(self, addr, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((addr, port))
		self.sock.listen(16)
		print "Sync Server Start!"


class referenceNode:

	def __init__(self, conn, addr):
		self.conn = conn 
		self.addr = addr 

	def send_sync_msg(self):
		self.conn.send("SYNC")

	def recv_finish_msg(self):
		recv_msg = self.conn.recv(256)
		print recv_msg


def sync(ap, index):
	
	global ACK
	ap.send_sync_msg()
	ap.recv_finish_msg()
	command = "scp mvnl@10.8.0.2%d:~/linux-80211n-csitool-supplementary/lab_pos/online/log%d.dat ../tmp/" % (index+2, index+1)
	print command
	args = shlex.split(command)
	subprocess.call(args)

	ACK[index] = True

def main():

	server = syncServer(sys.argv[1], int(sys.argv[2]))
	clientList = []
	connect_number = 0
	global ACK

	# Before start, we need to connect to all access points
	while(connect_number != int(sys.argv[3])):
		connect, address = server.sock.accept()
		clientList.append(referenceNode(connect, address))
		connect_number += 1
		print "Node: " + str(connect_number) + " Connected!"
	
	while True:
		
		for i in range(len(clientList)):
			ap = clientList[i]
			start_new_thread(sync, (ap,i, ))

		while(sum(ACK) != int(sys.argv[3])):
			pass

		ACK = [0]*int(sys.argv[3])



if __name__ == "__main__":
	main()

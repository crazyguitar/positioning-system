#!/usr/bin/python

import socket
import sys
import time
import subprocess
import shlex
import os


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
	
	def send_est_finish_msg(self):
		self.conn.send('ESTIMATE_END')
	
	def recv_est_finish_ack(self):
		recv_msg = self.conn.recv(256)
		print recv_msg


def sync(ap):
	
	ap.send_sync_msg()

def sync_ack(ap):
	ap.recv_finish_msg()

def download_log_file(ap, index):
	command = "scp mvnl@%s:~/linux-80211n-csitool-supplementary/lab_pos/online/log%d.dat ../tmp/" % (ap.addr[0], index+1)
	print command
	args = shlex.split(command)
	subprocess.call(args)


def main():

	server = syncServer(sys.argv[1], int(sys.argv[2]))
	clientList = []
	connect_number = 0

	# Before start, we need to connect to all access points
	while(connect_number != int(sys.argv[3])):
		connect, address = server.sock.accept()
		clientList.append(referenceNode(connect, address))
		connect_number += 1
		print "Node: " + str(connect_number) + " Connected!"
	
	while True:
		
		# send sync msg
		for i in range(len(clientList)):
			ap = clientList[i]
			sync(ap)

		for i in range(len(clientList)):
			ap = clientList[i]
			sync_ack(ap)

		for i in range(len(clientList)):
			ap = clientList[i];
			download_log_file(ap, i)

		
		log_file_list = os.listdir('../tmp/')
		while(len(log_file_list)!=0):
			log_file_list = os.listdir('../tmp/')

		for i in range(len(clientList)):
			ap = clientList[i]
			ap.send_est_finish_msg()
			ap.recv_est_finish_ack()


if __name__ == "__main__":
	main()

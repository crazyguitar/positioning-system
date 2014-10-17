#!/usr/bin/python

import socket
import sys
import subprocess
import shlex
import time

class syncClient:

	def __init__(self):

		self.sock = socket.socket( \
				socket.AF_INET, \
				socket.SOCK_STREAM)
		self.p = None

	def connect_to_sync_server(self, addr, port):
		self.sock.connect((addr, port))

	def recv_sync_msg(self):

		recv_msg = self.sock.recv(256)
		print recv_msg
		
	def start_collect(self, ap_id):
		command = "sudo ../netlink/log_to_file online/log%d.dat" % (ap_id)
		args = shlex.split(command) 
		self.p = subprocess.Popen(args, stdout=subprocess.PIPE)
		time.sleep(3)
	
	def send_ACK_to_sync_server(self):
		
		try:
			self.sock.send("ACK_FOR_END_COLLECT")
		except socket.error, e:
			print "error = %s" % e
			sys.exit(1)
	
	def end_collect(self):
		self.p.terminate()
		print self.p.communicate()[0]
	

def main():

	ap_id = int(sys.argv[3])
	refer = syncClient()
	# connect to sync server
	refer.connect_to_sync_server(sys.argv[1], int(sys.argv[2]))
	
	while True:

		# wait for sync msg
		refer.recv_sync_msg()
		
		# start to collect CSI
		refer.start_collect(ap_id)

		# end collect 
		refer.end_collect()

		# send ACK to sync server 
		refer.send_ACK_to_sync_server()

	refer.sock.close()

if __name__ == '__main__':
	main()

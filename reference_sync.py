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
		time.sleep(1.5)
	
	def send_ACK_to_sync_server(self):
		
		try:
			self.sock.send("ACK_FOR_END_COLLECT")
		except socket.error, e:
			print "error = %s" % e
			sys.exit(1)
	
	def end_collect(self):
		self.p.terminate()
		print self.p.communicate()[0]

	def recv_est_end(self):
		recv_msg = self.sock.recv(256)
		print recv_msg

	def remove_log_file(self, ap_id):
		# remove log file
		command = "sudo rm -rf online/log%d.dat" % (ap_id)
		print command
		args = shlex.split(command)
		subprocess.call(args)
	
	def send_est_end_ack(self):

		try:
			self.sock.send("ACK_FOR_ESTIMATE_END")
		except socket.error, e:
			print "error = %s" % e
			sys.exit(1)
	

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
		
		# recv download end msg
		refer.recv_est_end()
		
		# remove log file
		refer.remove_log_file(ap_id)

		# send download end ack to syn server
		refer.send_est_end_ack()

	refer.sock.close()

if __name__ == '__main__':
	main()

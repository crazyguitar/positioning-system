#!/usr/bin/python

import socket
import subprocess
import shlex
import os 
import sys


class ReferenceNode:

	def __init__(self):
		self.sock = socket.socket( \
				socket.AF_INET, \
				socket.SOCK_STREAM)
		self.p = None

	def connect_to_central(self, addr, port):
		self.sock.connect((addr, port))

	def recv_start_command(self, current_count):

		recv_msg = self.sock.recv(256)
		print recv_msg
		try:
			self.sock.send("ACKFORSTART")
		except socket.error, e:
			print "error = %s" % e
			sys.exit(1)

		command = 'sudo ../netlink/log_to_file tmp/log%d.dat' % \
				(current_count)
		args = shlex.split(command)
		self.p = subprocess.Popen(args, stdout=subprocess.PIPE)

	def recv_stop_command(self):

		recv_msg = self.sock.recv(256)
		print recv_msg
		self.p.terminate()
		print self.p.communicate()[0]
		try:
			self.sock.send("ACKFORSTOP")
		except socket.error, e:
			print "error = %s" %e
			sys.exit(1)
		
def main():

	refer = ReferenceNode()
	refer.connect_to_central(sys.argv[1], int(sys.argv[2]))
	current_count = 0;
	while True:
		current_count += 1
		print current_count
		refer.recv_start_command(current_count)
		refer.recv_stop_command()

	refer.sock.close()


if __name__ == "__main__":
	main()


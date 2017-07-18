# Botnet
Botnet project for UIUC security course CS460

The master script currently has 2 zombies hardcoded in  IP,PORT = 127.0.0.1,6001 and IP,PORT = 127.0.0.1,6002. So when you run zombie.py, make sure it is either "python zombie.py 6001" and/or "python zombie.py 6002".

-zombie script is run on infected machine using command "python zombie.py 'PORT'" where 'PORT' is the port number you want the zombie to listen on.

-master script is run on the host machine using command "python master.py". It then waits for commands. Commands are in format "'INDEX' 'CMD'" where 'INDEX' is the index of the zombie machine you wish to send (in our case 0 or 1) to or "all" if you wish to send to all zombies. 'CMD' depends on which command you wish to execute:

Reverse shell - 'CMD' = "RVSH". (This cannot be sent to all bots)

DDOS attack - 'CMD' = "DDOS,'DEST_IP','DEST_PORT'" where 'DEST_IP' and 'DEST_PORT' are the destination ip address and port for the attack. (To test you can run a zombie at port 6003 for example and send a ddos to 127.0.0.1,6003 and observe what gets printed)

Keylogger - 'CMD' = "KEYL,'TIME'" where 'TIME' is how long you wish to keylog in seconds. You can also press '`' (grave key) to stop.




FOR LEARNING PURPOSES ONLY. NOT FOR MALICIOUS USE.

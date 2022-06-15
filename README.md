# SSH_Honeypot

## This is an SSH research honeypot written in Python.
\
The primary purpose of this honeypot is to gather information regarding potential bad actors and block their IPs so they cannot reconnect. 
This information includes:
- Client IP and port used
- SSH version used by the client
- Type of encryption and strength
- Client's public key
- Client's Username and password
- Any commands received
- Failed connections

All this information is in a log file named "Honeypot_ssh.log"

### Setup

It uses the [Paramiko](https://github.com/paramiko/paramiko) Python SSH protocol library.
To install the Pramiko library on a Ubuntu device, use the command:

`sudo apt-get install -y python3-paramiko`\
\
\
Then one must setup the server's key using the following commands:

`ssh-keygen -t rsa -f server_honey.key`

Then rename the public key:

`mv server_honey.key.pub server_honey.pub`\
\
\
To run the honeypot, use the command:

`python3 __main__.py`

This allows for two arguments:
- `-b` To bind it to the IP of choice (The default is the local loopback address)
- `-p` To bind it to the port of choice (The default is port 4444)

### Further Configuration


This iptables command will redirect all traffic from the port 1 to 5000 to port 4444

`sudo iptables -t nat -A PREROUTING -p tcp --dport 1:5000 -j REDIRECT --to-ports 4444`\
\
\
For any questions or comments please email me @ `cyberpings@gmail.com`


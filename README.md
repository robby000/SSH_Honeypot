# SSH_Honeypot

## This is an SSH research honeypot written in Python.
\
The primary purpose of this honeypot is to gather information regarding potential bad actors and block their IPs so they can't reconnect. 
This information includes:
- Client IP and port used
- SSH version used by the client
- Type of encryption and strength
- Client's public key
- Client's Username and password
- Any commands received
- Failed connections

All this information is in a log file named "Honeypot_ssh.log"\
\
\
It uses the [Paramiko](https://github.com/paramiko/paramiko) Python SSH protocol library.
To install the Pramiko library on a Ubuntu device, please use the command:

`sudo apt-get install -y python3-paramiko`\
\
\
Then one must setup the servers key using the following commands:

`ssh-keygen -t rsa -f server_honey.key`

Then rename the public key:

`mv server_honey.key.pub server_honey.pub`\
\
\
To run the honeypot, use the command:

`python3 __main__.py`

This allows for two arguments
1. `-b` To bind it to the IP of choice (The default is the local loopback address)
2. `-p` To bind it to the port of choice (The default is port 4444)


# Imports:
import ctypes
import logging
import os
import socket
import platform
import argparse

# Local imports
from __init__ import HoneyPot

########################################################################################################################
# Configure logger
logging.basicConfig(filename='Honeypot_ssh.log',
                    encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%s',
                    level=logging.INFO)

# Declare constants
IP = socket.gethostbyname(socket.gethostname())  # Loopback IP is the default IP that the honeypot runs on

platform = platform.system()  # Get the current platform (Linux, Windows)

########################################################################################################################
# Check that this is not run as root or admin as this can lead to privilege escalation

if platform == "Linux":  # If using Linux
    if os.geteuid() == 0:
        print("Do not run this honeypot as root as it can lead to privilege escalation")
        exit(2)
elif platform == "Windows":  # If using Windows
    if ctypes.windll.shell32.IsUserAnAdmin():
        print("Do not run this honeypot as administrator as it can lead to privilege escalation")
        exit(3)
else:
    print(f"{platform} is not supported for this honeypot")
    exit(4)

########################################################################################################################

# Run the honeypot and allow for added arguments

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create and run an honeypot SSH server")
    parser.add_argument("--port", "-p", help="The port to bind the ssh server to (default 22)", default=4444, type=int,
                        action="store")
    parser.add_argument("--bind", "-b", help="The address to bind the server to (defaults to loopback). In a cloud "
                                             "instance it should bind to 0.0.0.0", default=IP, type=str, action="store")
    args = parser.parse_args()
    honeypot = HoneyPot(args.port, args.bind)
    honeypot.run()

########################################################################################################################

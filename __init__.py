import csv
from socket import socket
import paramiko  # Need to install using the command "sudo apt-get install -y python3-paramiko"
import socket
import threading
import logging
import traceback
import sys
from os import getcwd
import platform

# Imports from local files
from commands import handle_cmd
from server_config import SshServer

########################################################################################################################
# Declare Constants and lists

Ip_list = "ip_list"

Ip_list_read = []

location = getcwd()  # Create relative path for files

# Import SSH host key
HOST_KEY = paramiko.RSAKey(filename='server_honey.key')
# Banner for SSH entry
ENTRY_BANNER = "SSH-2.0-OpenSSH_7.7"

# Get the current platform (Linux, Windows)
platform = platform.system()

# Create list of IPs that have already connected in the past
with open("ip_list.csv", newline="") as i:
    for row in csv.reader(i):
        Ip_list_read.append(row[0])

########################################################################################################################


# Create a csv file with a list of previously connected IPs
def write_ips(ip):
    if platform == "Windows":
        csv_file = location + "\\" + Ip_list + ".csv"  # get file path
    else:
        csv_file = location + "/" + Ip_list + ".csv"  # get file path
    with open(csv_file, 'a', encoding='UTF8') as j:
        csv_out = csv.writer(j)
        csv_out.writerow([ip])

########################################################################################################################


class HoneyPot(object):

    def __init__(self, port, ip):
        if port < 1:
            #  Force this specified exception if no port was provided
            raise Exception("No ports were provided.")

        self.port = port
        self.ip = ip

    @staticmethod
    def handle_client(client, addr):
        clients_ip = addr[0]
        write_ips(clients_ip)

        # Send information to logger
        logging.info(f"New connection from {addr}")

        try:
            tran = paramiko.Transport(client)
            # must contain private key info
            tran.add_server_key(HOST_KEY)
            # Create entry banner for client
            tran.local_version = ENTRY_BANNER
            server = SshServer(clients_ip)

            try:
                # Start the server using the SSHServer class
                tran.start_server(server=server)
            # if the SSH2 negotiation fails, the host key supplied by the server is incorrect, or authentication fails.
            except paramiko.SSHException:
                logging.error(f"Server failed to start SSH connection with client - {addr}")
                print(f"Server failed to start SSH connection with client - {addr}")

            # Wait for auth with a timeout of X seconds
            channel = tran.accept(100)
            if channel is None:
                logging.error(f"No channel was received from {addr}")
                print(f"No channel was received from {addr}")
                raise Exception("No channel received")

            # A timeout of the connection after X seconds
            channel.settimeout(100)

            # If there is information from the client then log it
            if tran.remote_version != '':
                logging.info(f"{addr} SSH version is {tran.remote_version}")

            if tran.remote_cipher != '':
                logging.info(f"{addr} Cipher is {tran.remote_cipher}")

            # Wait for a shell request
            server.event.wait(100)
            # If client never asked for a shell
            if not server.event.is_set():
                logging.info(f"Client - {addr} never asked for a shell")
                raise Exception("No shell requested")
            try:
                # Send the fake root shell header
                channel.send("Ubuntu 20.04 LTS Internal Server N.056 \n\r\n".encode())
                channel.send("This server is for internal use only!!!\n\r\n".encode())
                logging.info(f"Sent fake shell to client @ {addr}, Channel id is - {channel.get_id()}")
                while True:
                    # Send shell command line
                    channel.send("root@internal_server_056# ".encode())
                    command = ""
                    while not command.endswith("\r"):  # If the letter is not enter
                        # Create variable for the received command and fix the amount of bytes to receive
                        received = channel.recv(1024)
                        # Send back received command to simulate terminal
                        channel.send(received)
                        # Add all the letters of the command together
                        command += received.decode("utf-8")
                    channel.send("\r\n".encode())  # Remove blank created in terminal
                    logging.info(f"Received command {command.rstrip()} from {addr}")  # rstrip is for the logger

                    # If the command is exit then exit terminal
                    if command.startswith("exit"):
                        logging.info(f"Connection closed by client - {clients_ip} using command Exit")
                        break

                    # Send command to get response
                    else:
                        handle_cmd(command, channel)

            except Exception as err:
                logging.error(f"Exception: Class: {err.__class__} Error: {err} (Sending Shell)")
                print(f"Exception: Class: {err.__class__} Error: {err}")
                tran.close()

            channel.close()

        except Exception as err:
            logging.error(f"Failed to create SSH Session with client {addr}")
            print(f"Failed to create SSH Session with client {addr} Error = {err}")
            tran.close()

    # Start listening for connections
    def start_listening(self):
        if 1 <= self.port <= 65535:
            try:
                # Type of connections to allow(IPv4), Streaming data from the socket(TCP)
                listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Allows for multiple sockets on the same port
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # Binding the socket to an IP and port number
                listener.bind((self.ip, self.port))
            except Exception as err:
                print(f"The bind has failed, Error = {err}")
                # Print the error
                traceback.print_exc()
                sys.exit(1)

            threads = []
            while True:
                try:
                    # amount of connections allowed
                    listener.listen(100)
                    print(f"Listening for a connection on {self.ip} and port - {self.port}")
                    logging.info(f"Listening for a connection on {self.ip} and port - {self.port}")
                    # Accept a connection
                    client, addr = listener.accept()
                    # If IP has already connected then refuse the connection
                    if addr[0] in Ip_list_read:
                        # Close the socket to disconnect known IP
                        listener.close()
                        logging.info(f"Refused connection from known IP = {addr[0]}")
                        print(f"Refused connection from known IP = {addr[0]}")
                        # Restart the socket
                        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        listener.bind((self.ip, self.port))
                        continue
                    else:
                        print(f"Connection from {addr} has been established.")
                        # Add the new IP to the known list
                        Ip_list_read.append(addr[0])

                        # Create threads to handle_connection
                        new_thread = threading.Thread(target=self.handle_client, args=(client, addr))
                        # Start the threads
                        new_thread.start()
                        threads.append(new_thread)
                        for thread in threads:
                            thread.join()

                except Exception as err:
                    print(f"The listen/accept has failed, Error = {err}")
                    traceback.print_exc()

        else:
            print("[!] Please specify a valid port range (1-65535) in the configuration.")
            sys.exit(2)

    def run(self):
        self.start_listening()

########################################################################################################################

import threading
from binascii import hexlify
import paramiko
import logging


########################################################################################################################
# Documentation:https://docs.paramiko.org/en/stable/api/server.html
# This class defines an interface for controlling the behavior of Paramiko in server mode for SSH.
# Methods on this class are called from paramiko's primary thread
class SshServer(paramiko.ServerInterface):

    client_ip = None

    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    # Always check channel request if it is a session log it and then open
    # self, kind = the kind of channel the client wants to open (usually session), chanid = small number
    def check_channel_request(self, kind, chanid):
        logging.info(f"Client = {self.client_ip} channel request has been checked and is: {kind}")
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    # Return a list of authentication methods supported by the server, and log username of client.
    def get_allowed_auths(self, username):
        logging.info(
            f"Client = {self.client_ip} Returned list of supported authentication to username: {username}")
        auths = 'gssapi-keyex,gssapi-with-mic,password,publickey'
        return auths

    # Accept all passwords as valid by default and log the credentials
    def check_auth_password(self, username, password):
        logging.info(f"Client = {self.client_ip} has logged in using username - {username} and password - {password}")
        return paramiko.AUTH_SUCCESSFUL

    # Authorise when client uses a publickey to log in and log the public key
    def check_auth_publickey(self, username, key):
        # Convert fingerprint hash to hexadecimal digits
        fingerprint = (hexlify(key.get_fingerprint()))
        logging.info(f" {self.client_ip} with the username - {username} has logged in using a public key: "
                     f"Name: {key.get_name()} fingerprint - {fingerprint} base64 - {key.get_base64()} "
                     f"bits (to see the length of the key) - {key.get_bits()}")
        return paramiko.AUTH_SUCCESSFUL

    # Log GSS API login attempts and only partially authorise so to require public key or password
    def check_auth_gssapi_keyex(self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None):
        logging.info(f"Client = {self.client_ip} has partially logged in using gssapi_keyex with username - {username}")
        return paramiko.AUTH_PARTIALLY_SUCCESSFUL

    def check_auth_gssapi_with_mic(self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None):
        logging.info(f"Client = {self.client_ip} has partially logged in using gssapi_keyex with username - {username}")
        return paramiko.AUTH_PARTIALLY_SUCCESSFUL

    # Log port forwarding requests then refuse them
    def check_port_forward_request(self, address, port):
        logging.info(f" {self.client_ip} has requested port forwarding with address - {address} and port {port}")
        return False

    # Approve client's request for a shell
    def check_channel_shell_request(self, channel):
        self.event.set()  # Invoke the thread
        return True

    # Approve client's request for a pseudo-terminal
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    # Log channel exec requests
    def check_channel_exec_request(self, channel, command):
        logging.info(f"{self.client_ip} sent a command = {command} with a channel exec request")
        return True

########################################################################################################################

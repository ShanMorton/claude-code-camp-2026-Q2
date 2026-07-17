#!/usr/bin/env python3
"""
tbaMUD Telnet Client
Connects to tbaMUD on localhost:4000 and manages MUD interactions.
"""

import socket
import sys
import re
import time
import os
from pathlib import Path

# Configuration
MUD_HOST = 'localhost'
MUD_PORT = 4000
MUD_USER = 'dummy'
MUD_PASSWORD = 'helloworld'
SESSION_FILE = Path(os.path.expanduser('~/.mud_session'))


class MUDClient:
    """Manages socket connection to tbaMUD"""

    def __init__(self, host=MUD_HOST, port=MUD_PORT, username=MUD_USER, password=MUD_PASSWORD):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sock = None
        self.connected = False

    def connect(self):
        """Establish socket connection to MUD"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.host, self.port))
            self.connected = True
            time.sleep(1.0)
            return True
        except Exception as e:
            print(f"Error connecting to {self.host}:{self.port}: {e}")
            return False

    def recv_until(self, pattern=None, timeout=3):
        """Receive data until pattern found or timeout"""
        self.sock.settimeout(timeout)
        data = b''
        try:
            while True:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                data += chunk
                if pattern and pattern in data:
                    break
        except socket.timeout:
            pass
        except:
            pass
        return data

    def login(self, silent=False):
        """Authenticate with the MUD"""
        if not self.connected:
            if not self.connect():
                return False

        try:
            # Clear initial data
            self.recv_until(timeout=2)

            # Send username
            self.sock.send(f"{self.username}\r\n".encode())
            time.sleep(0.3)
            response = self.recv_until(timeout=1)

            # If asked for confirmation, send yes
            if b'Y/N' in response or b'(Y/N)' in response:
                self.sock.send(b"Y\r\n")
                time.sleep(0.3)
                response = self.recv_until(timeout=1)

            # Send password
            self.sock.send(f"{self.password}\r\n".encode())
            time.sleep(2.0)
            response = self.recv_until(timeout=1)

            # Handle disclaimer
            if b'Yes or No' in response or b'Disclaimer' in response or b'?' in response:
                self.sock.send(b"Yes\r\n")
                time.sleep(0.5)
                self.recv_until(timeout=1)

            self.connected = True
            if not silent:
                print("Logged in successfully")
            return True
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def send_command(self, command):
        """Send a command to the MUD and return the response"""
        if not self.connected:
            print("Not connected to MUD. Run 'login' first.")
            return None

        try:
            self.sock.send(f"{command}\r\n".encode())
            response = self.recv_until(timeout=2)

            response_str = response.decode('utf-8', errors='ignore')
            cleaned = self._clean_ansi(response_str)
            return cleaned.strip()
        except Exception as e:
            print(f"Error executing command: {e}")
            self.connected = False
            return None

    def logout(self):
        """Disconnect from the MUD"""
        if self.connected:
            try:
                self.send_command("quit")
                self.sock.close()
            except:
                pass
            self.connected = False
            print("Logged out")

    @staticmethod
    def _clean_ansi(text):
        """Remove ANSI escape codes from text"""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)


def main():
    if len(sys.argv) < 2:
        print("Usage: mud_client.py <command> [args]")
        print("Commands:")
        print("  login              - Connect and authenticate")
        print("  command <cmd>      - Execute a MUD command")
        print("  logout             - Disconnect")
        print("  status             - Show character status")
        sys.exit(1)

    action = sys.argv[1]
    client = MUDClient()

    try:
        if action == 'login':
            client.connect()
            client.login()

        elif action == 'command':
            if len(sys.argv) < 3:
                print("Usage: mud_client.py command <command>")
                sys.exit(1)
            cmd = ' '.join(sys.argv[2:])
            client.connect()
            client.login(silent=True)
            output = client.send_command(cmd)
            if output:
                print(output)

        elif action == 'logout':
            client.connect()
            client.logout()

        elif action == 'status':
            client.connect()
            client.login(silent=True)
            output = client.send_command('score')
            if output:
                print(output)

        else:
            print(f"Unknown command: {action}")
            sys.exit(1)

    finally:
        if client.connected:
            try:
                client.sock.close()
            except:
                pass


if __name__ == '__main__':
    main()

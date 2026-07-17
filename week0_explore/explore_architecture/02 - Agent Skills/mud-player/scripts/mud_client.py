#!/usr/bin/env python3
"""
tbaMUD Telnet Client
Connects to tbaMUD on localhost:4000 and manages MUD interactions.
"""

import telnetlib
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
    """Manages telnet connection to tbaMUD"""

    def __init__(self, host=MUD_HOST, port=MUD_PORT, username=MUD_USER, password=MUD_PASSWORD):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.tn = None
        self.connected = False

    def connect(self):
        """Establish telnet connection to MUD"""
        try:
            self.tn = telnetlib.Telnet(self.host, self.port, timeout=10)
            self.connected = True
            # Read initial connection message
            time.sleep(0.5)
            self.tn.read_very_eager()
            return True
        except Exception as e:
            print(f"Error connecting to {self.host}:{self.port}: {e}")
            return False

    def login(self):
        """Authenticate with the MUD"""
        if not self.connected:
            if not self.connect():
                return False

        try:
            # Wait for login prompt
            time.sleep(0.5)
            output = self.tn.read_very_eager().decode('utf-8', errors='ignore')

            # Send username
            self.tn.write(f"{self.username}\r\n".encode())
            time.sleep(0.5)
            output = self.tn.read_very_eager().decode('utf-8', errors='ignore')

            # Send password
            self.tn.write(f"{self.password}\r\n".encode())
            time.sleep(1.0)  # Wait longer for login to complete
            output = self.tn.read_very_eager().decode('utf-8', errors='ignore')

            self.connected = True
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
            # Send command
            self.tn.write(f"{command}\r\n".encode())
            time.sleep(0.3)

            # Read response
            response = self.tn.read_very_eager().decode('utf-8', errors='ignore')

            # Clean ANSI codes and extra whitespace
            cleaned = self._clean_ansi(response)
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
                self.tn.close()
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

    # Create client
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
            # Check if we're already logged in
            client.tn.read_very_eager()  # Clear buffer
            output = client.send_command(cmd)
            if output:
                print(output)

        elif action == 'logout':
            client.connect()
            client.logout()

        elif action == 'status':
            client.connect()
            client.tn.read_very_eager()  # Clear buffer
            output = client.send_command('score')
            if output:
                print(output)

        else:
            print(f"Unknown command: {action}")
            sys.exit(1)

    finally:
        if client.connected:
            try:
                client.tn.close()
            except:
                pass


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
tbaMUD Telnet Client
Connects to tbaMUD on localhost:4000 and manages MUD interactions.
"""

import socket
import sys
import re
import time

# Configuration
MUD_HOST = 'localhost'
MUD_PORT = 4000
MUD_USER = 'dummy'
MUD_PASSWORD = 'helloworld'

# Marks that we've reached the normal in-game prompt, e.g. "22H 100M 84V (news) (motd) >"
IN_GAME_RE = re.compile(rb'\d+H\s+\d+M\s+\d+V')


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
            return True
        except Exception as e:
            print(f"Error connecting to {self.host}:{self.port}: {e}")
            return False

    def _read_available(self, settle=0.3, max_wait=6):
        """Read whatever the server sends, waiting for output to go quiet
        (settle) rather than assuming a fixed prompt arrives instantly.
        The MUD does several seconds of telnet option negotiation before
        showing its first real prompt, so a fixed short timeout races it."""
        self.sock.settimeout(settle)
        data = b''
        start = time.time()
        last_recv = start
        while time.time() - start < max_wait:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                data += chunk
                last_recv = time.time()
            except socket.timeout:
                if data and (time.time() - last_recv) >= settle:
                    break
                continue
            except OSError:
                break
        return data

    def login(self, silent=False):
        """Authenticate with the MUD, reacting to whatever prompt the
        server actually sends rather than sending credentials on a timer.
        Also transparently handles the case where a prior session is still
        linkdead and the server drops us straight back into the game."""
        if not self.connected:
            if not self.connect():
                return False

        name_sent = False
        password_sent = False
        deadline = time.time() + 20

        while time.time() < deadline:
            chunk = self._read_available(settle=0.4, max_wait=4)

            if IN_GAME_RE.search(chunk):
                self.connected = True
                if not silent:
                    print("Logged in successfully")
                return True

            if not chunk:
                continue

            if b'By what name' in chunk:
                self.sock.send(f"{self.username}\r\n".encode())
                name_sent = True
            elif b'Did I get that right' in chunk or b'(Y/N)' in chunk:
                # Only confirm if it's confirming the name we actually sent.
                if self.username.encode().lower() in chunk.lower():
                    self.sock.send(b"Y\r\n")
                else:
                    self.sock.send(b"N\r\n")
            elif b'Password:' in chunk and not password_sent:
                self.sock.send(f"{self.password}\r\n".encode())
                password_sent = True
            elif b'PRESS RETURN' in chunk:
                self.sock.send(b"\r\n")
            elif b'Make your choice' in chunk:
                self.sock.send(b"1\r\n")
            elif b'Wrong password' in chunk or b'password incorrect' in chunk.lower():
                print("Error: incorrect password")
                self.connected = False
                return False

        print("Error: timed out waiting for login to complete")
        self.connected = False
        return False

    def send_command(self, command):
        """Send a command to the MUD and return the response"""
        if not self.connected:
            print("Not connected to MUD. Run 'login' first.")
            return None

        try:
            self.sock.send(f"{command}\r\n".encode())
            response = self._read_available(settle=0.3, max_wait=6)
            cleaned = self._clean_ansi(response.decode('utf-8', errors='ignore'))
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
            except Exception:
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
        print("Usage: mud_client.py <action> [args]")
        print("Actions:")
        print("  login                 - Connect, authenticate, and quit")
        print("  command <cmd>         - Log in, execute one command, quit")
        print("  commands <cmd> <cmd>  - Log in, execute multiple commands in order, quit")
        print("  status                - Log in, show character status (score), quit")
        print("  logout                - Connect and quit (clears a linkdead session)")
        sys.exit(1)

    action = sys.argv[1]
    client = MUDClient()

    try:
        if action == 'login':
            if client.login():
                client.logout()

        elif action == 'command':
            if len(sys.argv) < 3:
                print("Usage: mud_client.py command <command>")
                sys.exit(1)
            cmd = ' '.join(sys.argv[2:])
            if client.login(silent=True):
                output = client.send_command(cmd)
                if output:
                    print(output)
                client.logout()

        elif action == 'commands':
            if len(sys.argv) < 3:
                print("Usage: mud_client.py commands <cmd1> <cmd2> ...")
                sys.exit(1)
            if client.login(silent=True):
                for cmd in sys.argv[2:]:
                    output = client.send_command(cmd)
                    print(f"> {cmd}")
                    if output:
                        print(output)
                    print()
                client.logout()

        elif action == 'status':
            if client.login(silent=True):
                output = client.send_command('score')
                if output:
                    print(output)
                client.logout()

        elif action == 'logout':
            if client.login(silent=True):
                client.logout()

        else:
            print(f"Unknown action: {action}")
            sys.exit(1)

    finally:
        if client.connected and client.sock:
            try:
                client.sock.close()
            except Exception:
                pass


if __name__ == '__main__':
    main()

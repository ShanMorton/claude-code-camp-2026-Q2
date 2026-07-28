---
name: mud-player
description: Connect to and play tbaMUD on localhost:4000. Use this skill when the user wants to interact with the MUD, execute commands, check character status, explore, or engage in any MUD gameplay. Authenticates with the provided credentials and manages telnet connection.
compatibility: Python 3.6+, telnetlib (stdlib)
---

# tbaMUD Player Skill

This skill connects to tbaMUD running on localhost:4000 and allows you to execute commands and interact with the game.

## Setup

The MUD client script is located at `scripts/mud_client.py`. It manages the telnet connection and command execution.

**Default credentials:**
- Username: `dummy`
- Password: `helloworld`
- Server: `localhost:4000`

## How to Use

### 1. Connect to the MUD
```bash
python scripts/mud_client.py login
```
This connects and authenticates with the MUD.

### 2. Execute a Command
```bash
python scripts/mud_client.py command "look"
```
Replace `"look"` with any MUD command. Common commands:
- `look` - Observe current surroundings
- `inventory` or `i` - Check your inventory
- `go north/south/east/west` - Move around
- `kill <target>` - Attack an NPC
- `cast <spell>` - Cast a spell
- `tell <player> <message>` - Send a message
- `say <message>` - Speak to current room
- `get <item>` - Pick up an item

### 2b. Execute Multiple Commands in One Session
```bash
python scripts/mud_client.py commands "look" "inventory" "score"
```
Logs in once and runs each command in order, printing each command's
output. Prefer this over repeated single `command` calls when running a
sequence of actions — it avoids repeating the login handshake each time.

### 3. Get Status
```bash
python scripts/mud_client.py status
```
Returns character information and current status.

### 4. Logout
```bash
python scripts/mud_client.py logout
```
Disconnects from the MUD.

## Command Output

The script returns clean, parsed responses from the MUD. Output includes:
- Game messages and descriptions
- Command results
- Character status updates

## Example Workflow

```bash
# Connect to the MUD
python scripts/mud_client.py login

# Look around
python scripts/mud_client.py command "look"

# Check inventory
python scripts/mud_client.py command "i"

# Move north
python scripts/mud_client.py command "go north"

# Attack a mob
python scripts/mud_client.py command "kill goblin"

# Cast a spell
python scripts/mud_client.py command "cast magic missile"

# Logout when done
python scripts/mud_client.py logout
```

## Notes

- Each CLI invocation is a fresh process, so `command`/`status`/`logout` each open a new
  connection, log in, do their work, and quit. Use `commands` (plural) to run several MUD
  commands in a single login session instead of repeating `command` many times.
- The MUD does several seconds of telnet negotiation before showing its login prompt, and if
  a prior session is still linkdead it skips straight back into the game instead of prompting
  for a name/password — the client detects and handles both cases automatically.
- Output is automatically cleaned of ANSI color codes for readability
- Command execution is synchronous - the script waits for the MUD's response

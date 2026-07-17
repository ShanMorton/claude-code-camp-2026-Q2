# tbaMUD Player Skill

A Claude Code skill for playing tbaMUD on localhost:4000.

## Installation

This skill is located in the `mud-player` folder with skill metadata in `SKILL.md`.

1. Reload skills in Claude Code:
   ```
   /reload-skills
   ```

2. The skill should now be available and will trigger when you mention MUD gameplay.

## Quick Start

### Connect to the MUD
```bash
python .claude/skills/mud-player/scripts/mud_client.py login
```

### Execute a Command
```bash
python .claude/skills/mud-player/scripts/mud_client.py command "look"
```

### Common Commands
- `look` - Observe surroundings
- `inventory` / `i` - Check inventory
- `go north/south/east/west` - Move
- `kill <target>` - Attack NPC
- `cast <spell>` - Cast a spell
- `tell <player> <message>` - Send message
- `say <message>` - Speak in room
- `get <item>` - Pick up item

### Logout
```bash
python .claude/skills/mud-player/scripts/mud_client.py logout
```

## Default Credentials

- **Username:** dummy
- **Password:** helloworld
- **Server:** localhost:4000

## How It Works

The skill includes a Python telnet client that:
- Connects to tbaMUD via telnet
- Handles authentication
- Executes commands and returns clean responses
- Removes ANSI color codes for readability
- Maintains connection between commands

## Notes

- The client persists connections, so you don't re-login for each command
- Output is automatically cleaned and formatted
- If connection drops, use `login` to reconnect
- The skill works with Claude Code and will assist you in playing the MUD

# Player: dummy

Reference notes for the `mud-player` skill (`02 - Agent Skills/.claude/skills/mud-player/`)
so future sessions don't have to re-derive connection/login details from scratch.

## Credentials

- Server: `localhost:4000`
- Username: `dummy`
- Password: `helloworld`

## Connecting

Use the skill's client directly, or invoke the `mud-player` skill:

```bash
python .claude/skills/mud-player/scripts/mud_client.py login
python .claude/skills/mud-player/scripts/mud_client.py command "<cmd>"
python .claude/skills/mud-player/scripts/mud_client.py commands "<cmd1>" "<cmd2>" ...
python .claude/skills/mud-player/scripts/mud_client.py status
python .claude/skills/mud-player/scripts/mud_client.py logout
```

Prefer `commands` (plural) when running a sequence of actions — it logs in once and
runs everything in that session instead of repeating the login handshake per command.

## Login handshake — things that used to break this

- The MUD (tbaMUD) takes several seconds to run telnet client-detection negotiation
  before it shows the "By what name" prompt. Sending the username/password on a fixed
  timer races this negotiation and corrupts the login (in one case it created a stray
  character named "Helloworld" instead of logging in as `dummy`). The client now reads
  until output settles and reacts to whichever prompt actually appears (`By what name`,
  `Password:`, `PRESS RETURN`, `Make your choice`) rather than guessing timing.
- If a previous session is still linkdead, reconnecting drops straight back into the
  game and skips the name/password/menu prompts entirely — the client detects this by
  watching for the in-game status-bar pattern (`\d+H \d+M \d+V`) at any point.
- If login ever times out again, don't assume the environment/WSL/Ruby setup is broken —
  trace the raw protocol first (open a socket by hand and watch what the server actually
  sends) before changing anything else.

## Character snapshot (as of 2026-07-27)

- Class/title: Dummy the Swordpupil (level 1)
- Age: 18
- HP/Mana/Move: 22(22) / 100(100) / 84(84)
- Armor class: 100/10, alignment 0
- Gold: 0, exp: 1, quest points: 0
- First-ever login room: **The Temple of Midgaard** (southern end of the temple hall)

## Save / load room behavior

The MUD does **not** always load the character at a fixed spawn point — logging in
resumes wherever the character last `quit` from. Confirmed by quitting inside the
Bakery, then logging in again and landing back in the Bakery rather than the Temple.
If you want to guarantee a known starting room for the next session, walk back to
**The Temple of Midgaard** and `quit` from there before ending the session (see
`world.md` for the route back from the Bakery).

See `world.md` for the map, room exits, and shop info gathered so far.

# Week1 Technical Documentation

## Technical Goals
I want to try to get through as many videos as I can and to follow along.
I feel this may be a little trying, but will work through as many as I can.




## Technical Uncertainly
Earlier this week, I tried to run Cladue to play the game but it still was stuck
on trying to get the environment to start up and to get the correct player to 
log in with the login timing out.  I got frustrated with it and quit.

- installed ruby in WSL on my laptop.


## Technicial Hypotheses



## Technical Conclusions
Unknown as yet.


## Key Takeaways 
To keep trying with my efforts and following the videos.
I'm trying to be careful and do things correctly, but I feel I'm still
behind b/c I can't get into the game and find the bakery. 

## Update - 2026-07-27: Fixed the login timeout and found the bakery

Went back to the `mud-player` skill (`.claude/skills/mud-player/`) that was already
sitting in the `02 - Agent Skills` folder to figure out why login kept timing out.

- Root cause: the client was sending the username and password on fixed timers, but
  tbaMUD takes a few seconds to finish its telnet client-detection negotiation before
  it actually shows the "By what name" prompt. The old code raced that negotiation, so
  the credentials landed at the wrong prompt — at one point it even blindly created a
  stray character named "Helloworld" instead of logging in as `dummy`.
- Fix: rewrote the login logic in `scripts/mud_client.py` as a small state machine that
  reads server output until it settles, then reacts to whatever prompt actually shows up
  (`By what name`, `Password:`, `PRESS RETURN`, `Make your choice`), instead of assuming
  fixed timing. It also now handles reconnecting to a still-linkdead session, which skips
  the login menu entirely and drops straight back into the game.
- Added a `commands` (plural) action so a whole sequence of MUD commands can run in one
  login session instead of re-doing the handshake for every single command.
- Cleaned up a leftover, incomplete duplicate `mud-player/` draft folder at the top level
  (old `telnetlib`-based script, no `SKILL.md`) that was superseded by the real skill.

With login actually working, explored from the starting room to find the bakery:

`Temple of Midgaard` → down → `Temple Square` → south → `Market Square` → west →
`Main Street` → north → `The Bakery`

Bakery items and prices (`list` command in the shop):

| Item | Price (gold) |
|---|---|
| A danish pastry | 7 |
| A bread | 15 |
| A waybread | 76 |

Takeaway: the "login timing out" problem wasn't the environment or Ruby/WSL setup at
all — it was a race condition in the telnet handshake logic in the skill's own script.
Worth remembering for next time something "just hangs": trace the raw protocol by hand
before assuming the infrastructure is broken.
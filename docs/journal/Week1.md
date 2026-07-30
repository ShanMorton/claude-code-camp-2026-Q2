# Week1 Technical Documentation

## Technical Goals
I want to try to get through as many videos as I can and to follow along.
I feel this may be a little trying, but will work through as many as I can.

27July2026
Went back throug the "Explore Agent Architechure 2" video from the start and 
not sure how I skipped it but asked Claude to fix the issue of getting logged
in and finding the bakery. I guess I didn't put the proper prompt in the first time;
Claude kept trying to log in and create a new user instead of logging in with
the user I had created.
This time around I got the prompt more correct, and proceeded with updating/creating the skill and installing the skill into Claude to be used.



## Technical Uncertainly
Earlier this week, I tried to run Cladue to play the game but it still was stuck
on trying to get the environment to start up and to get the correct player to 
log in with the login timing out.  I got frustrated with it and quit.

- installed ruby in WSL on my laptop.
- got Ruby to run properly with assistance.


## Technicial Hypotheses



## Technical Conclusions
27July2026
It really makes a difference how good your prompts are.  The better they are the more
they can do. Now, I'm not thinking Claude is as dumb as I thought; I'm the less intelligent
one for not telling it exactly what I want it to do.


## Key Takeaways 
To keep trying with my efforts and following the videos.
I'm trying to be careful and do things correctly, but I feel I'm still
behind b/c I can't get into the game and find the bakery. 
27July2026
Even if you take a rest, going back over the videos and data and trying is a worthy
endeavor to get to the next step.
Now to move on to week1 and see if I can get finished with that week.
I think week2 will be beyond me.


## Update - 2026-07-27: Fixed the login timeout and found the bakery (Summary by Claude)

Went back to the `mud-player` skill (`.claude/skills/mud-player/`) that was already
sitting in the `02 - Agent Skills` folder to figure out why login kept timing out.

- Root cause: the client was sending the username and password on fixed timers, but
  tbaMUD takes a few seconds to finish its telnet client-detection negotiation before
  it actually shows the "By what name" prompt. The old code raced that negotiation, so
  the credentials landed at the wrong prompt; at one point it even blindly created a
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
(End Summary by Claude)

28July2026 - SM
Wow! Talk about being confused!!!

I am working through the video "Config Ruby" and asking for help from Claude to get 
Ruby running and to fix any file/paths that need to be updated.

Claude is FIXING MY ERRORS!!!  

I wish I had this type of tool when I was in college to learn to program.
I might have been a decent programmer!! 
I guess I still could be!

Ruby is running and I'm progressing througt the video.
Still confused but at least things are matching the video.

Below is where I'll ask Claude to update this readme file with the work 
that it has done for me.

## Update - 2026-07-28: Got example.rb running (Summary by Claude)

Worked through the `00_config` step in `week1_baseline/ruby/` and fixed a few things
so `example.rb` would actually run:

- `ruby examples/example.rb` was failing with `cannot load such file -- dotenv`
  because the `dotenv` gem was only installed into Bundler's local `vendor/bundle`
  path, not Ruby's global gem path. Running it as `bundle exec ruby examples/example.rb`
  worked right away.
- `bin/00_config` had a broken `cd` path (an extra `ruby/` had snuck into it), so the
  script's `cd` was silently failing. Fixed the path so the script runs from the right
  directory again.
- Added `require "bundler/setup"` to the top of `examples/example.rb` so plain
  `ruby example.rb` also works now, without needing `bundle exec` every time.
- Updated the root `.gitignore` to ignore `vendor/` and `.bundle/` so the installed
  gems and local Bundler config don't get committed.

End result: `example.rb` runs cleanly and prints the Boukensha config output.

## Project Summary So Far - 2026-07-28 (Summary by Claude)

Overall progress across this week, pulled together from the updates above:

**27 July 2026 — MUD login and finding the bakery**
- Challenge: login to the MUD kept timing out, and the client sometimes created a
  stray new character instead of logging in as the existing user.
- Root cause: the `mud-player` skill's script sent username/password on fixed timers,
  racing tbaMUD's telnet negotiation, so credentials landed at the wrong prompt.
- Fix: rewrote the login logic in `scripts/mud_client.py` as a state machine that
  waits for and reacts to the actual prompt shown, added support for reconnecting to
  a linkdead session, added a `commands` (plural) action to run a sequence of MUD
  commands in one login, and removed a stray duplicate draft `mud-player/` folder.
- Result: logged in successfully and found the Bakery (Temple of Midgaard → down →
  Temple Square → south → Market Square → west → Main Street → north → The Bakery),
  with prices recorded for danish pastry, bread, and waybread.

**28 July 2026 — Getting Ruby's `example.rb` running (`week1_baseline/ruby/00_config`)**
- Challenge: `ruby examples/example.rb` failed with `cannot load such file -- dotenv`.
- Root cause: `dotenv` was installed only into Bundler's local `vendor/bundle` path,
  not Ruby's global gem path, so a plain `ruby` invocation couldn't see it.
- Fix: confirmed `bundle exec ruby examples/example.rb` worked, then added
  `require "bundler/setup"` to the top of `example.rb` so plain `ruby example.rb`
  works too.
- Challenge: `bin/00_config` was failing to `cd` into the right directory.
- Root cause: an extra `ruby/` segment had been added to the `cd` path by mistake.
- Fix: corrected the path back to `../00_config`.
- Housekeeping: updated the root `.gitignore` to ignore `vendor/` and `.bundle/`
  (installed gems and local Bundler config shouldn't be committed), and confirmed the
  existing `.env` rule in `.gitignore` already covers `.boukensha/.env` with no
  changes needed.
- Result: `example.rb` now runs cleanly with either `bundle exec ruby` or plain
  `ruby`, printing the Boukensha config output.

**Overall takeaway:** most of the "stuck" moments this week turned out to be small,
findable root causes (a race condition in a script, a typo'd path, a missing
`bundle exec`) rather than the environment or WSL/Ruby setup being broken. Working
through them one at a time with Claude, and giving more specific prompts, made steady
progress possible.
####(End Summary by Claude)

I decided NOT to port to Python, so I did watch the video, Config Python Port,
I wanted to move fwd to see how far I would get in the Week1 videos.

Proceeding on to video "Struct Skeleton Ruby".


29July2026
Running into the same issues the the video.
I asked Claude to ensure that any time I want to run ruby, that I can do 
it from anywhere in my repo/files.

So far, so good.

I am passing on porting the Ruby code to Python; watched the "Struct Skeleton Python Port" 
video but didn't ask for the conversion to be done.


On to the "Prompt Builder Ruby" video, watching but choosing not to port the code to Python.


30July2026
I attended the office hrs to see if I would learn something new.  I don't think I'll get through
week1 but my goal is to finish the videos and follow along as best I can.

Seeing how Andrew uses Claude has been the most helpful for me.


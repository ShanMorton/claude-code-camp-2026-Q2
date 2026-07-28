# World Map — Midgaard (tbaMUD, localhost:4000)

Rooms discovered so far while playing as `dummy` (see `player.md` for login info).
Exits are as reported by `look` in-game (`n`/`e`/`s`/`w`/`u`/`d`).

## Route from spawn to the Bakery

```
Temple of Midgaard --d--> Temple Square --s--> Market Square --w--> Main Street (west) --n--> The Bakery
```

Command sequence: `d`, `s`, `w`, `n`

## Route from the Bakery back to the Temple (main entry)

```
The Bakery --s--> Main Street (west) --e--> Market Square --n--> Temple Square --n--> Temple of Midgaard
```

Command sequence: `s`, `e`, `n`, `n`

Note: the return trip from Temple Square to the Temple uses `n` (not `u`), even
though the outbound trip used `d` — the up/down steps are keyed as `n`/`d` here,
not `u`/`d`. Confirmed working 2026-07-27 (see `player.md` for why the character's
login room isn't fixed — it resumes wherever you last quit).

## Rooms

### The Temple of Midgaard (spawn point)
- Exits: n e s w d
- Southern end of the temple hall. Reading Room to the west, donation room to the east.
- Steps lead down (`d`) to the Temple Square.
- Has an ATM ("automatic teller machine... installed in the wall").

### Temple Square (`d` from Temple)
- Exits: n e s w
- Clerics' Guild to the west. The old Grunting Boar Inn to the east.
- Market square is just south.
- Fountain, and a cityguard NPC present.

### Market Square (`s` from Temple Square)
- Exits: n e s w
- "The famous Square of Midgaard" — a large statue in the middle.
- North → Temple Square. South → Common Square. East/West → Main Street.
- Center hub of the city.

### Main Street — east branch, 1st room (`e` from Market Square)
- Exits: n e s w
- General store to the north. Pet Shop to the south (small door).
- Main street continues east.

### Main Street — east branch, 2nd room (`e` again)
- Exits: n e s w
- Weapon shop to the north. Guild of Swordsmen to the south.
- East leaves town. A "beastly fido" mob wanders here.

### Common Square (`s` from Market Square)
- Exits: n e s w
- Poor alley to the west, dark alley to the east.
- "Nasty smell" from the south (unexplored).
- A "beastly fido" mob wanders here.

### Main Street — west branch (`w` from Market Square)
- Exits: n e s w
- Armory to the south. **Bakery to the north.**

### The Bakery (`n` from Main Street west branch)
- Exits: s only (dead end / shop room)
- NPCs: a Peacekeeper (guard), the baker.
- Shop command: `list` shows wares.

## Shops

### Bakery (Main Street, west of Market Square)

| Item | Price (gold) | Stock |
|---|---|---|
| A danish pastry | 7 | Unlimited |
| A bread | 15 | Unlimited |
| A waybread | 76 | Unlimited |

### Other known shop locations (contents not yet checked)
- General store — north off Main Street (east branch, 1st room)
- Pet Shop — south off Main Street (east branch, 1st room)
- Weapon shop — north off Main Street (east branch, 2nd room)
- Guild of Swordsmen — south off Main Street (east branch, 2nd room)
- Armory — south off Main Street (west branch)
- Clerics' Guild — west off Temple Square
- Grunting Boar Inn — east off Temple Square

## Unexplored leads
- South of Common Square ("nasty smell")
- Poor alley (west of Common Square) and dark alley (east of Common Square)
- East of Market Square's 2nd Main Street room (leaves town — surrounding wilderness)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

"Ghost Survival" — a top-down wave-survival game built with **pygame**, written by students in the ConnectSTEM CS program. Playable build: https://polnareffturtle07.itch.io/ghost-survival

The codebase is educational: many collaborators, inconsistent conventions, and lots of `TODO` / "placeholder" / commented-out experiments. It carries known bugs and half-finished features (see **Known bugs** below) — treat rough spots as things to fix, not conventions to preserve.

### Known bugs / unfinished work
- **Tilemap spawns are ignored.** `GameplayScene.__init__` reads spawn points from `tilemap.spawns` to build `EnemyList`, then immediately overwrites `EnemyList` with `Enemy.create_wave(...)`, discarding the tilemap-driven spawns (the player-spawn override is also thrown away). The wave system should consume tilemap spawns instead (see the `TODO` in that file).
- Enemy attack animations are incomplete (see recent commit history — "one of the attacks still needs fixing").

## Commands

```bash
# Setup (use python3 on mac)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the game
python main.py
```

Assets are loaded via **relative paths** (`assets/images/...`, `assets/tiled/...`, `assets/fonts/pixel.ttf`), so the game **must be run from the repo root**. `scripts/tilemap.py` reads `assets/tiled/spritesheet.json` at *import time*, so a missing/renamed asset breaks imports, not just runtime.

There is no test suite, linter, or type checker configured. Requirements pin only `pygame>=2.6.1`.

## Web build (pygbag)

The game is structured for **pygbag** (WASM/browser) deployment — that is why `main.py` uses `asyncio` and every frame `await asyncio.sleep(0)`. `build/web/` is committed pygbag output; `build/version.txt` holds the current version string. Preserve the async structure when editing the main loop.

## Architecture

### Game loop and scene stack (`main.py`)
`Game` owns the window (1280×720 `screen`), a low-res `320×180` `display` surface that everything renders to and is then scaled up (pixel-art look), the shared `assets` dict, and the clock (60 FPS). All gameplay draws to `display` at native resolution; `scale` converts screen↔game coordinates (important for mouse aiming — see `Weapon.handle_input`).

Scenes are selected by `GameState` enum via `scene_factories`. `Game.run()` drives an outer loop; `run_scene()` runs the inner per-frame loop while `scene.running` and no scene change is pending. Scene transitions:
- A scene requests a change by calling `game.change_scene(GameState.X)` (sets `next_scene`).
- Pausing pushes the current `GameplayScene` onto `scene_stack`; when the pause scene ends (`running = False`), the gameplay scene is popped and resumed — so **pause preserves game state**, other transitions rebuild the scene from scratch.

### Scenes (`scripts/scenes/`)
All extend `Scene` (`scene.py`) with `handle_events(events)` / `update(dt)` / `render(screen)`. Scenes: `MainMenuScene`, `GameplayScene`, `PauseScene`, `DeathScene`, `OptionsMenuScene`. `GameplayScene` is the core: it owns `player`, `EnemyList`, `projectiles`, `coins`, `tilemap`, `wallet`, wave counter, and the camera `offset` (keeps player centered; `render_offset` is the int-rounded version passed to every `render(...offset=...)`).

### Entities and collision
- `Collide` (`collide.py`) — base for anything with a position/image. Position is a float `Vector2` **centered** on the sprite; `rect()` and `aabb_collide(rect)` derive bounds from `pos ± size/2`. Never instantiate directly.
- `Entity` (`entities/entities.py`) extends `Collide` with velocity, friction, health, a `HealthBar`, and `update(dt)` that applies velocity, resolves tilemap collisions per-axis via `check_wall_collisions`, clamps to world bounds, and applies friction. Subclasses override `on_death()`.
- `Player` (`entities/player.py`) — WASD/arrow movement (set in `GameplayScene.handle_events` into the `movement` array, netted into a direction in `update`). Drops to `DEATH` scene at 0 health.
- `Enemy` + subclasses (`entities/enemy.py`) — `CircleEnemy`, `LungeEnemy`, `RotateEnemy`, each pairing a movement/attack behavior with a weapon. Stats scale with `level` (= wave number). `Enemy.create_wave(scene, wave_number, count)` is the spawn factory; `GameplayScene.update` advances to the next wave when `EnemyList` empties. `on_death()` drops a `Coin`.

### Weapons (`scripts/weapon.py`, `scripts/weaponmanager.py`)
`Weapon` base handles cooldown/`attack_speed` and `use()` (respects cooldown) vs `attack()` (does damage). Subclasses: `CircleWeapon` (AoE radius), `LungeWeapon` (sets user velocity toward target), `RotateWeapon` (orbiting melee), `Gun` (spawns `Bullet` projectiles). Weapons are used by both enemies (targeting the player) and the player. `WeaponType` enum tags them.

`WeaponManager` is the player's single weapon system: it owns the swappable weapon list (`CircleWeapon`, `RotateWeapon`, `Gun`), cycles them with `Q`, and fires the active weapon on **left mouse** by delegating to that weapon's `handle_input`. Aiming reads the mouse, unscales it via `scene.game.scale`, and adds `render_offset` to get world coordinates — any mouse-based feature must do the same conversion.

### Tilemap (`scripts/tilemap.py`)
Maps are **Tiled** JSON exports in `assets/tiled/maps/<n>.json` (currently only `0.json`); tile metadata (type, properties) comes from `assets/tiled/spritesheet.json`. Tile `type == 'physics'` → solid collision; `type == 'spawn'` with an `entity` property (+ optional `subclass`) defines spawn points read into `tilemap.spawns`. `physics_rects_around(pos)` returns only the 3×3 neighborhood of solid tiles for cheap collision. Note: the tilemap-spawn path is read but then discarded — see **Known bugs**.

### Assets and animation
`Game.assets` is a dict built at startup. Two loading styles coexist:
- **Folder-of-frames** animations via `load_images('foldername', alpha=True)` — each folder under `assets/images/` is one animation (naming prefixes: `p*`=player, `c*`=crawler enemy, `f*`=flyer, `s*`=sword).
- **Single images** (`load_image`) and **spritesheets** (`spritesheet_to_surf_list`, used for `tiles` from `spritesheet.png` at 16×16).

`Animation` (`utils.py`) is a named-state animator (`set_animation(name)`, `update(dt)`, `get_current_frame()`). `Text` (`utils.py`) wraps font rendering with `assets/fonts/pixel.ttf`.

### Other systems
- `economy.py` — `Wallet` (balance, `add`/`spend`); coins credit it on pickup.
- `item.py` — `Item`/`Coin` (auto-pickup on AABB overlap with player).
- `music.py` — `Music` static class maps each `GameState` to background tracks; `Game.run` calls `Music.play` on scene changes and forwards events to `Music.update`. Tracks must be commercially licensed (see header note).
- `button.py` — `Button` / `NavButton` (hover + click, `NavButton` triggers a `GameState` transition).

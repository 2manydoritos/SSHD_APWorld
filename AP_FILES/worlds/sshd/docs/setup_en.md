# Skyward Sword HD Archipelago Setup Guide

This guide will help you set up Skyward Sword HD for Archipelago multiplayer randomizer using Ryujinx.

## Prerequisites

### 1. Ryujinx Emulator
- Download Ryujinx emulator
- Must have Skyward Sword HD ROM (v1.0.0 or v1.0.1) and keys configured
- Game must boot and run properly in Ryujinx

### 2. Python 3.10+
- Download from: https://www.python.org/
- Ensure Python is added to PATH during installation

### 3. Archipelago 0.5.0+
- Download from: https://archipelago.gg/
- Install the main Archipelago application

### 4. SSHD Randomizer Extract
- Download sshd-rando from: https://github.com/mint-choc-chip-skyblade/sshd-rando
- Extract your Skyward Sword HD ROM using the randomizer's extract feature
- Note the path where files are extracted (needed later)

## Installation

### Step 1: Install the SSHD APWorld

**Option A: Install from .apworld file**
1. Download `SSHD.apworld` from the releases
2. Double-click the file to install (if Archipelago is installed)
3. Or copy it to: `%localappdata%/Archipelago/custom_worlds/`

**Option B: Install from source**
1. Copy the entire `SSHD_APWorld` folder to your Archipelago installation:
   ```
   C:\ProgramData\Archipelago\lib\worlds\sshd\
   ```

### Step 2: Set Up sshd-rando Backend

1. Create folder: `SSHD_APWorld/sshd-rando-backend/`
2. Copy these folders from your sshd-rando installation:
   - `asm/`
   - `assets/`
   - `constants/`
   - `data/`
   - `logic/`
   - `patches/`
   - `sslib/`
   - `util/`
   - `filepathconstants.py`
   - `gui/dialogs/dialog_header.py` (only this file)
   - `gui/guithreads.py` (stub version provided)

**Note**: The included `gui/guithreads.py` is a no-GUI stub that doesn't require PySide6.

### Step 3: Configure Extract Path

1. Edit `sshd-rando-backend/filepathconstants.py`
2. Update `SSHD_EXTRACT_PATH` to point to your extracted ROM folder:
   ```python
   SSHD_EXTRACT_PATH = Path("C:/path/to/your/sshd-extract")
   ```

### Step 4: Add Custom Logo (Optional)

To replace the randomizer logo with Archipelago branding:
1. Create 3 TPL files with your custom logo:
   - `archipelago-logo.tpl` (main logo)
   - `archipelago-rogo_03.tpl` (shiny layer 1)
   - `archipelago-rogo_04.tpl` (shiny layer 2)
2. Place them in: `SSHD_APWorld/assets/`

See `assets/README.md` for details on creating TPL files.

### Step 5: Install Python Dependencies

Open command prompt and run:
```bash
pip install pymem psutil
```

### Step 6: Install the Client

**Option A: Use pre-built executable**
1. Download `ArchipelagoSSHDClient.exe` from releases
2. Place it anywhere convenient

**Option B: Run from source**
```bash
cd SSHD_APWorld
python SSHDClient.py
```

### Step 7: Verify Installation

1. Launch `ArchipelagoLauncher.exe`
2. You should see "Skyward Sword HD" in the game list
3. Check that the client appears in the launcher

## Generating a Seed

### Step 1: Create Your YAML Configuration

Create a YAML file with your settings (example: `SSHD_Settings.yaml`):

```yaml
name: YourPlayerName
game: Skyward Sword HD

Skyward Sword HD:
  progression_balancing: 50
  
  # Completion requirements
  required_dungeon_count: 2
  triforce_required: true
  triforce_shuffle: anywhere
  gate_of_time_sword_requirement: true_master_sword
  
  # Starting inventory
  starting_sword: practice_sword
  start_with_sailcloth: true
  
  # Quality of Life
  open_lake_floria_gate: true
  open_thunderhead: true
  fast_bird_statues: true
  skip_intro: true
  
  # Difficulty
  damage_multiplier: normal
  
  # Death Link (optional - careful!)
  death_link: false
```

### Step 2: Generate the Seed

1. Open `ArchipelagoLauncher.exe`
2. Click "Generate Game"
3. Select your YAML file
4. Click "Generate"
5. You'll get a `.apsshd` file in the output folder

## Playing

### Step 1: Extract Patch Data

The `.apsshd` file contains:
- Item placements for your seed
- Connection information for multiplayer
- Configuration for the client

**NOTE**: Currently, you need to manually integrate this with sshd-rando to generate the RomFS mod.
This step will be automated in a future update.

### Step 2: Apply RomFS Mod

1. Use `sshd-rando` to generate a randomized RomFS mod using the data from the `.apsshd` file
2. Configure Ryujinx to use the RomFS mod:
   - Right-click Skyward Sword HD in Ryujinx
   - Select "Open Mods Directory"
   - Place the generated mod folder there
   - Enable the mod in Ryujinx settings

### Step 3: Launch the Client

1. Start Ryujinx and boot Skyward Sword HD
2. Wait for the game to fully load (reach the title screen or in-game)
3. Launch `SSHDClient.py`:

```bash
python SSHDClient.py
```

Or use the Archipelago Launcher's "Skyward Sword HD Client" button.

### Step 4: Connect to Server

In the client window:

1. Type `/connect <server>:<port>` (e.g., `/connect archipelago.gg:38281`)
2. Enter your player name when prompted
3. Enter the room password if required
4. The client will:
   - Scan Ryujinx memory for SSHD (takes 8-10 seconds)
   - Connect to the Archipelago server
   - Begin syncing items in real-time

### Step 5: Play!

- Collect checks in-game (chests, bosses, NPCs, etc.)
- Items you collect will be sent to other players
- Items from other players will appear in your game automatically
- The client window shows connection status and item sync

## Troubleshooting

### "Ryujinx.exe not found"
- Ensure Ryujinx is running
- Ensure the game is loaded (not just at the emulator menu)

### "Could not find SSHD signature in memory"
- The game must be running and loaded into memory
- Try restarting the game and waiting for it to fully load
- Check if you're using a compatible Ryujinx version

### "Failed to connect to Archipelago server"
- Verify the server address and port
- Check your internet connection
- Ensure the server is online

### Items not appearing in-game
- Currently, item giving requires pointer chain implementation
- This feature is still in development
- Location checking should work (items you collect are sent to others)

### Base address scan takes too long
- This is normal (7-10 seconds)
- The scan only happens once when you launch the client
- Future versions may cache the signature location for faster reconnection

## Current Limitations

- **Partial Implementation**: Not all features are fully implemented yet
- **Manual RomFS Generation**: Patch → RomFS conversion is manual for now
- **Limited Locations**: Only ~30 locations defined (full game has ~400+)
- **Item Giving**: Receiving items from other players needs pointer chain work
- **Testing Required**: This is an early version and needs extensive testing

## Advanced Configuration

### Memory Offsets

If you need to update memory offsets (e.g., after a game update):

1. Use `sshd-tools/Cheat Table/sshd-cheat-table.CT` as reference
2. Edit `SSHDClient.py` and update the `OFFSET_*` constants
3. Test with `test_ryujinx_memory.py` to verify offsets work

### Custom Options

Edit `Options.py` to add new randomization options for your playthrough style.

### Logic Modifications

Edit `Rules.py` to customize access logic and completion requirements.

## Getting Help

- **Discord**: Join the Archipelago Discord server
- **GitHub**: Report issues on the project repository
- **Documentation**: See `README.md` for technical details

## Credits

- **Archipelago Framework**: archipelago.gg
- **SSHD Randomizer**: sshd-rando project
- **Ryujinx Emulator**: ryujinx.org
- **Memory Access**: pymem library

---

Happy randomizing! May the Goddess smile upon your seed. ✨

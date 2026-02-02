# Skyward Sword HD - Archipelago World

An [Archipelago](https://archipelago.gg) multiworld randomizer integration for **The Legend of Zelda: Skyward Sword HD**.

## Overview

This implementation allows you to play Skyward Sword HD in a multiworld randomizer with other Archipelago-supported games. Items are shuffled across all players, creating a cooperative experience where finding items in your world sends them to other players.

## Quick Start

1. **Install this APWorld**
   - Extract files to `C:\ProgramData\Archipelago\custom_worlds\sshd\`
   - Or place `sshd.apworld` in `C:\ProgramData\Archipelago\custom_worlds\` (auto-extracts)

2. **Download sshd-rando Backend**
   - Place in `C:\ProgramData\Archipelago\custom_worlds\sshd\sshd-rando-backend\`
   - Extract your SSHD ROM files

3. **Setup Environment**
   ```powershell
   # Set extract path (required)
   $env:ROMFS_EXTRACT_PATH = "C:\path\to\your\extracted\romfs"
   ```

4. **Generate Your Seed**
   - Create a YAML with your player options
   - Upload to Archipelago website or generate locally
   - Receive `.apsshd` patch file

5. **Play**
   - Launch `SSHDClient.py` to connect to the server
   - Load your patched game in Ryujinx
   - Items you find are sent to other players automatically!

## Features

- **400+ Locations**: All chests, goddess cubes, NPCs, dungeons, minigames
- **300+ Items**: Progression items, equipment, tablets, keys, consumables
- **Full Logic Support**: Ensures you always have items needed to progress
- **40+ Options**: Customize starting items, logic difficulty, item placement
- **Custom Logos**: Replace title screen with Archipelago branding
- **Multiworld**: Play cooperatively with any Archipelago-supported game

## Documentation

- **[Setup Guide](docs/setup_en.md)**: Complete installation and configuration instructions
- **[Game Info](docs/en_Skyward%20Sword%20HD.md)**: What gets randomized and how the game works
- **[Server Setup](SSHD_SERVER_SETUP.md)**: For self-hosted Archipelago server administrators

## System Requirements

- **Python**: 3.10 or newer
- **Archipelago**: Latest stable release (0.6.5+)
- **Ryujinx**: Latest version (for running SSHD)
- **SSHD ROM**: Legally obtained copy with extracted romfs
- **sshd-rando**: Backend randomizer (downloaded separately)

## Current Status

### ✅ Fully Functional
- Location checking (400+ locations tracked)
- Item sending to other players
- Logic rules and access requirements
- Player option configuration (40+ settings)
- Client-server communication
- Patch file generation
- Custom logo replacement

### 🔄 Known Limitations
- Patch generation only maps basic options (4 of 40+)
- No user-friendly extract path configuration UI
- Game icon needs creation (placeholder currently)

## Installation Methods

### Method 1: Extract Files
Extract all files to your Archipelago custom worlds folder:
```
C:\ProgramData\Archipelago\custom_worlds\sshd\
```

### Method 2: APWorld Package (Recommended)
Place the `sshd.apworld` file in:
```
C:\ProgramData\Archipelago\custom_worlds\
```
Archipelago will automatically extract it to `custom_worlds\sshd\` on next launch.

## Backend Setup

The sshd-rando backend is **not included** and must be downloaded separately:

1. Clone or download [sshd-rando](https://github.com/mint-choc-chip-skyblade/sshd-rando)
2. Place in `C:\ProgramData\Archipelago\custom_worlds\sshd\sshd-rando-backend\`
3. Extract your SSHD ROM using the tools provided
4. Set `ROMFS_EXTRACT_PATH` environment variable

See [docs/setup_en.md](docs/setup_en.md) for detailed instructions.

## Custom Logos

You can customize the title screen and credits logos:

1. Create custom TPL files (Wii texture format)
2. Place in `assets/` folder:
   - `sshdr-logo.tpl` - Main title logo
   - `th_rogo_03.tpl` - Sub logo 1
   - `th_rogo_04.tpl` - Sub logo 2
3. Generate your seed - logos are automatically patched

See [assets/README.md](assets/README.md) for TPL creation instructions.

## Contributing

Contributions are welcome! Priority areas:
- Complete option mapping in patch generation
- Extract path configuration UI
- Game icon creation (64x64 PNG)
- Additional logic modes and goals

## Files Included

### Core World Files
- `__init__.py` - World definition and registration
- `Items.py` - Item database with classifications
- `Locations.py` - Location database
- `Options.py` - Player-configurable options
- `Rules.py` - Logic and access rules
- `SSHDClient.py` - Game client

### Support Files
- `rando/ArcPatcher.py` - Logo patching system
- `archipelago.json` - World metadata
- `docs/` - Setup and game information
- `assets/` - Logo TPL files

### Not Included
- `sshd-rando-backend/` - **Download separately** (copyrighted content)

## License

See LICENSE file for details. Note that sshd-rando is separate software with its own license.

## Support & Links

- **Archipelago**: https://archipelago.gg
- **Setup Issues**: See [docs/setup_en.md](docs/setup_en.md)
- **sshd-rando**: https://github.com/mint-choc-chip-skyblade/sshd-rando

---

**World Version**: 0.1.0  
**Archipelago Version**: 0.6.5+  
**Game**: The Legend of Zelda: Skyward Sword HD (Nintendo Switch via Ryujinx)

# SSHD Archipelago - Cross-Platform Setup Guide

This project is now fully cross-platform and supports **Windows, Linux, and macOS**.

## Installation by Operating System

### Windows Setup

1. **Install Archipelago**
   - Download from [archipelago.gg](https://archipelago.gg)
   - Install to default location: `C:\ProgramData\Archipelago`

2. **Copy world files**
   ```
   Copy sshd.apworld to: C:\ProgramData\Archipelago\custom_worlds\
   ```

3. **Extract SSHD ROM**
   - Use hactool to extract your SSHD rom into romfs/ and exefs/ folders
   - Place in: `C:\ProgramData\Archipelago\sshd_extract\`
   ```
   C:\ProgramData\Archipelago\sshd_extract\
   ├── romfs/
   └── exefs/
   ```

4. **Configure YAML**
   - Create `SkywardSwordHD.yaml` in `C:\ProgramData\Archipelago\Players\`
   - Leave `extract_path` empty to use default (or specify your custom path)

5. **Run the client**
   - Option 1: Use Archipelago Launcher GUI → SSHD
   - Option 2: Run `python launch_sshd_wrapper.py` from `C:\ProgramData\Archipelago\`

### Linux Setup

1. **Install Archipelago**
   - Use package manager or install from source
   - Default location: `~/.local/share/Archipelago`

2. **Copy world files**
   ```bash
   mkdir -p ~/.local/share/Archipelago/custom_worlds
   cp sshd.apworld ~/.local/share/Archipelago/custom_worlds/
   ```

3. **Extract SSHD ROM**
   - Use hactool to extract your SSHD rom into romfs/ and exefs/ folders
   - Place in: `~/.local/share/Archipelago/sshd_extract/`
   ```
   ~/.local/share/Archipelago/sshd_extract/
   ├── romfs/
   └── exefs/
   ```

4. **Configure YAML**
   - Create `SkywardSwordHD.yaml` in `~/.local/share/Archipelago/Players/`
   - Leave `extract_path` empty to use default

5. **Run the client**
   ```bash
   python ~/.local/share/Archipelago/sshd/SSHDClient.py &
   ```
   Or from the Archipelago Launcher menu if available.

### macOS Setup

1. **Install Archipelago**
   - Download from [archipelago.gg](https://archipelago.gg)
   - Default location: `~/Library/Application Support/Archipelago`

2. **Copy world files**
   ```bash
   mkdir -p ~/Library/Application\ Support/Archipelago/custom_worlds
   cp sshd.apworld ~/Library/Application\ Support/Archipelago/custom_worlds/
   ```

3. **Extract SSHD ROM**
   - Use hactool to extract your SSHD rom into romfs/ and exefs/ folders
   - Place in: `~/Library/Application Support/Archipelago/sshd_extract/`
   ```
   ~/Library/Application Support/Archipelago/sshd_extract/
   ├── romfs/
   └── exefs/
   ```

4. **Configure YAML**
   - Create `SkywardSwordHD.yaml` in `~/Library/Application Support/Archipelago/Players/`
   - Leave `extract_path` empty to use default

5. **Run the client**
   ```bash
   python ~/Library/Application\ Support/Archipelago/sshd/SSHDClient.py &
   ```

## Default Paths by OS

| Purpose | Windows | Linux | macOS |
|---------|---------|-------|-------|
| **Archipelago** | `C:\ProgramData\Archipelago` | `~/.local/share/Archipelago` | `~/Library/Application Support/Archipelago` |
| **SSHD Extract** | `C:\ProgramData\Archipelago\sshd_extract` | `~/.local/share/Archipelago/sshd_extract` | `~/Library/Application Support/Archipelago/sshd_extract` |
| **Ryujinx Config** | `%APPDATA%\Ryujinx` | `~/.config/Ryujinx` | `~/Library/Application Support/Ryujinx` |
| **Ryujinx Mods** | `%APPDATA%\Ryujinx\sdcard\atmosphere\contents\01002da013484000` | `~/.config/Ryujinx/sdcard/atmosphere/contents/01002da013484000` | `~/Library/Application Support/Ryujinx/sdcard/atmosphere/contents/01002da013484000` |

## YAML Configuration

All three platforms use the same YAML format. Create `SkywardSwordHD.yaml` with:

```yaml
name: Player1
game: Skyward Sword HD
description: SSHD Archipelago

Skyward Sword HD:
  # Leave blank to use OS-specific default
  extract_path: ""
  
  # Game options
  logic_rules: all_locations_reachable
  item_pool: standard
  required_dungeon_count: 2
  triforce_required: true
  
  # etc...
```

## Ryujinx Setup (All Platforms)

1. **Install Ryujinx** emulator for your OS
2. **Extract SSHD**: Use hactool or xdelta to extract SSHD ROM
3. **Place in Archipelago directory** (default paths above)
4. **Run the SSHD Client**:
   - Client will auto-detect Ryujinx and install LayeredFS mod
   - If not auto-detected, manually copy:
     - `romfs/` → `[Ryujinx Path]/sdcard/atmosphere/contents/01002da013484000/Archipelago/`
     - `exefs/` → same location

5. **Launch game in Ryujinx**:
   - LayeredFS will automatically apply Archipelago patches
   - Connect to Archipelago server via the client

## Troubleshooting

### Client says "Ryujinx not found"
- Make sure Ryujinx is installed in the standard location for your OS
- On Linux: `~/.config/Ryujinx`
- On macOS: `~/Library/Application Support/Ryujinx`
- On Windows: `%APPDATA%\Ryujinx`

### Extract path not found
- Verify you extracted SSHD correctly:
  ```
  sshd_extract/
  ├── romfs/          ← Contains game data
  └── exefs/          ← Contains game executable
  ```
- Check the path in your YAML matches your extraction

### Custom paths
- To use a custom extract or Ryujinx location, set in YAML:
  ```yaml
  extract_path: "/path/to/your/extract"
  ```

## Building from Source

To build the apworld for all platforms:

```bash
cd sshd-archipelago
python build_apworld.py
```

The built `sshd.apworld` is platform-independent and works on Windows, Linux, and macOS.

# Skyward Sword HD Archipelago - Troubleshooting Guide

## Common Issues

### Issue 1: Fi Doesn't Talk / Fledge Missing Marker / Game Crashes

**Symptoms:**
- Fi doesn't speak during tutorial
- Fledge has no quest marker (bubble)
- Character animations broken
- Soft lock at game start

**Root Causes:**

1. **Sailcloth not in starting inventory** (MOST COMMON)
   - In the Archipelago version, Sailcloth is NOT a valid starting item
   - The `start_with_sailcloth` YAML option is currently non-functional
   - Sail cloth must be obtained as a progression item from Archipelago
   - **Workaround**: You MUST have Sailcloth in your item pool and receive it early

2. **Wrong starting items from settings**
   - The conversion from Archipelago YAML to sshd-rando config may not match your expectations
   - Check the generation log for "Starting items from sshd-rando:" to see what you actually got

3. **Memory address mismatch** (Fixed in recent versions)
   - If you're using an older .apworld, the item memory addresses may be incorrect
   - Rebuild with `python build_apworld.py` to get the latest fixes

### Issue 2: Settings Don't Match Randomizer GUI

**Problem**: You configure settings in the sshd-rando GUI, but Archipelago uses different settings.

**Why This Happens**:
- The sshd-rando GUI stores settings in a compressed "Setting String" format
- Archipelago uses YAML configuration files
- There's currently NO direct import of Setting Strings into Archipelago
- The YAML → sshd-rando conversion may be incomplete

**Workarounds**:

1. **Manual Configuration**:
   - Open your YAML file (e.g., `SkywardSwordHD.yaml`)
   - Match each setting to the randomizer GUI values
   - List of YAML options: see `SSHD_Options.py`

2. **Check What Settings Were Actually Used**:
   - After generation, look for "Setting String:" in the output
   - Compare with your expected settings

3. **Starting Items Specifically**:
   - sshd-rando determines starting items based on:
     - `starting_tablets` setting (which tablets you start with)
     - `starting_sword` setting (which sword level)
     - Random starting items if that option is enabled
   - Archipelago version may have different defaults than vanilla sshd-rando

### Issue 3: "Invalid Starting Items" Warning

**Symptoms**:
```
WARNING: Invalid starting items found. The invalid entries have been removed. Invalid starting items: ['Sailcloth']
```

**Cause**: Sailcloth is not in the `STARTABLE_ITEMS` list in the Archipelago version.

**Fix**: This is expected behavior. Sailcloth will be removed from starting inventory and must be obtained through Archipelago.

### Issue 4: Cross-World Items Not Working

**Symptoms**: Locations that should have cross-world items instead have local items or errors.

**Cause**: Protected locations list or item mapping issue.

**Check**: Look for "Note: Cross-world item" messages in generation log.

## Diagnostic Commands

### Check Your Starting Items
After generation, search the log for:
```
[__init__.py] Starting items from sshd-rando:
```

This shows exactly what the game will give you at start.

### Verify Item Pool Size
Look for:
```
[__init__.py] Overlay results:
  Total locations: XXX
  Replaced items: XXX
```

If "Replaced items" is much less than "Total locations", starting items may not have been excluded properly.

### Check Memory Addresses
If items aren't being tracked:
```powershell
python -c "from ALL_ITEM_MEMORY_ADDRESSES import ITEM_MEMORY_ADDRESSES; print(list(ITEM_MEMORY_ADDRESSES.items())[:5])"
```

Should show addresses like `('Progressive Sword', ('0x4232100C', 2, 0))` with proper byte/bit pairs.

## Getting Help

When reporting issues, include:
1. Your YAML configuration file
2. Full generation log (from `ArchipelagoGenerate.exe`)
3. What you expected vs. what actually happened
4. Your sshd-rando version (check the .apworld file date)

## Known Limitations

1. **No Setting String Import**: You cannot paste a Setting String from the GUI directly into Archipelago
2. **Sailcloth Must Be Progression**: Cannot start with Sailcloth in Archipelago version
3. **Settings Conversion Incomplete**: Some advanced sshd-rando options may not be available in Archipelago

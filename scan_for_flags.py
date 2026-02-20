"""
Diagnostic script to find where sceneflags are actually stored in memory.
Run this BEFORE and AFTER picking up an item to see what changed.
"""

import pymem
import pymem.process
import time

def scan_memory_region(pm, start_addr, size, stride=2):
    """Scan a memory region for non-zero u16 values."""
    non_zero_addrs = []
    for offset in range(0, size, stride):
        try:
            addr = start_addr + offset
            value = pm.read_ushort(addr)
            if value != 0:
                non_zero_addrs.append((addr, value))
        except:
            pass
    return non_zero_addrs

def find_sshd_base(pm):
    """Get SSHD base address from user."""
    print("[*] Enter the base address from the client output")
    print("    (Look for 'Found SSHD base address: 0x...')")
    base_hex = input("Base address (hex without 0x, e.g., 232FCF24000): ")
    return int(base_hex, 16)

def main():
    # Connect to Ryujinx
    try:
        pm = pymem.Pymem("Ryujinx.exe")
        print(f"[+] Connected to Ryujinx (PID: {pm.process_id})")
    except:
        print("[-] Failed to connect to Ryujinx")
        return
    
    # Find base
    base = find_sshd_base(pm)
    if not base:
        print("[-] Could not find SSHD base address")
        return
    
    # Calculate expected SaveFile location
    savefile_offset = 0x5AEAD54
    expected_savefile_addr = base + savefile_offset
    expected_sceneflags_offset = 0x2264
    expected_sceneflags_addr = expected_savefile_addr + expected_sceneflags_offset
    
    print(f"[*] Base: 0x{base:X}")
    print(f"[*] Expected SaveFile: 0x{expected_savefile_addr:X}")
    print(f"[*] Expected Sceneflags: 0x{expected_sceneflags_addr:X}")
    
    # Scan the sceneflags array (26 scenes * 16 bytes = 416 bytes)
    print("\n[*] Scanning expected sceneflags location for non-zero values...")
    non_zero_before = scan_memory_region(pm, expected_sceneflags_addr, 416)
    print(f"[*] Found {len(non_zero_before)} non-zero u16 values at expected location")
    for addr, val in non_zero_before[:10]:  # Show first 10
        print(f"    0x{addr:X}: 0x{val:04X}")
    
    # Scan a wider area around expected location (±64KB)
    print("\n[*] Scanning ±64KB around expected location...")
    scan_start = expected_sceneflags_addr - 0x10000
    scan_size = 0x20000
    non_zero_wide = scan_memory_region(pm, scan_start, scan_size)
    print(f"[*] Found {len(non_zero_wide)} non-zero u16 values in wider scan")
    
    print("\n[!] Now pick up an item in-game and press Enter...")
    input()
    
    # Scan again after item pickup
    print("\n[*] Scanning after item pickup...")
    non_zero_after = scan_memory_region(pm, expected_sceneflags_addr, 416)
    print(f"[*] Found {len(non_zero_after)} non-zero u16 values at expected location")
    
    # Find differences
    before_set = set((addr, val) for addr, val in non_zero_before)
    after_set = set((addr, val) for addr, val in non_zero_after)
    new_values = after_set - before_set
    
    if new_values:
        print(f"\n[+] FOUND {len(new_values)} NEW VALUES:")
        for addr, val in new_values:
            offset_from_expected = addr - expected_sceneflags_addr
            print(f"    0x{addr:X} (offset +0x{offset_from_expected:X}): 0x{val:04X}")
    else:
        print("\n[-] No changes detected at expected location")
        print("[!] Flags may be written to a different memory location")
        print("[!] FILE_MGR pointer may point elsewhere")
    
    # Scan entire memory region for ANY changes
    print("\n[*] Scanning wide area again for changes...")
    non_zero_wide_after = scan_memory_region(pm, scan_start, scan_size)
    before_wide_set = set((addr, val) for addr, val in non_zero_wide)
    after_wide_set = set((addr, val) for addr, val in non_zero_wide_after)
    new_wide = after_wide_set - before_wide_set
    
    if new_wide:
        print(f"\n[+] FOUND {len(new_wide)} NEW VALUES IN WIDER SCAN:")
        for addr, val in list(new_wide)[:20]:  # Show first 20
            offset_from_base = addr - base
            offset_from_expected = addr - expected_sceneflags_addr
            print(f"    0x{addr:X} (base+0x{offset_from_base:X}, expected+0x{offset_from_expected:X}): 0x{val:04X}")
    else:
        print("\n[-] No changes detected in wider scan either")

if __name__ == "__main__":
    main()

"""
Cross-platform utilities for Windows, Linux, and macOS support.

Handles:
- Default directory paths for each OS
- Environment variable lookups
- Path normalization
"""

import os
import sys
from pathlib import Path
from typing import List, Optional


def get_os_name() -> str:
    """Get OS identifier: 'windows', 'linux', or 'darwin' (macOS)."""
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "linux":
        return "linux"
    elif sys.platform == "darwin":
        return "darwin"
    else:
        return sys.platform


def get_archipelago_dir() -> Path:
    """
    Get the Archipelago base directory for the current OS.
    
    Windows: C:\\ProgramData\\Archipelago or %APPDATA%\\Archipelago
    Linux: ~/.local/share/Archipelago
    macOS: ~/Library/Application Support/Archipelago
    """
    if get_os_name() == "windows":
        # Try PROGRAMDATA first (system-wide)
        if "PROGRAMDATA" in os.environ:
            return Path(os.environ["PROGRAMDATA"]) / "Archipelago"
        # Fall back to user AppData
        if "APPDATA" in os.environ:
            return Path(os.environ["APPDATA"]) / "Archipelago"
        # Ultimate fallback
        return Path("C:/ProgramData/Archipelago")
    
    elif get_os_name() == "linux":
        return Path.home() / ".local" / "share" / "Archipelago"
    
    elif get_os_name() == "darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Archipelago"
    
    else:
        # Fallback for unknown OS
        return Path.home() / "Archipelago"


def get_default_sshd_extract_path() -> Path:
    """Get the default path to extract SSHD ROM files."""
    return get_archipelago_dir() / "sshd_extract"


def get_ryujinx_dir() -> Path:
    """
    Get the Ryujinx base directory for the current OS.
    
    Windows: %APPDATA%\\Ryujinx
    Linux: ~/.config/Ryujinx
    macOS: ~/Library/Application Support/Ryujinx
    """
    if get_os_name() == "windows":
        if "APPDATA" in os.environ:
            return Path(os.environ["APPDATA"]) / "Ryujinx"
        return Path.home() / "AppData" / "Roaming" / "Ryujinx"
    
    elif get_os_name() == "linux":
        return Path.home() / ".config" / "Ryujinx"
    
    elif get_os_name() == "darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Ryujinx"
    
    else:
        return Path.home() / "Ryujinx"


def get_ryujinx_mod_dirs() -> List[Path]:
    """
    Get possible Ryujinx LayeredFS mod directories for SSHD (01002da013484000).
    
    Returns a list of paths to check, in order of preference.
    """
    ryujinx_base = get_ryujinx_dir()
    game_id = "01002da013484000"
    
    paths = [
        ryujinx_base / "sdcard" / "atmosphere" / "contents" / game_id,
    ]
    
    # On Windows, also check alternative locations
    if get_os_name() == "windows":
        appdata = Path(os.environ.get("APPDATA", ""))
        if appdata.exists():
            paths.append(appdata / "Ryujinx" / "sdcard" / "atmosphere" / "contents" / game_id)
    
    return paths


def find_ryujinx_mod_dir() -> Optional[Path]:
    """
    Find the Ryujinx LayeredFS mod directory for SSHD.
    
    Returns the first existing directory, or None if not found.
    """
    for path in get_ryujinx_mod_dirs():
        if path.parent.parent.parent.exists():  # Check if sdcard/atmosphere exists
            return path
    return None


def normalize_path(path_str: str) -> Path:
    """
    Normalize a path string to a Path object, handling cross-platform separators.
    
    Converts Windows backslashes to forward slashes for consistency.
    """
    if not path_str:
        return Path()
    
    # Replace backslashes with forward slashes for consistency
    normalized = path_str.replace("\\", "/")
    return Path(normalized)


def get_custom_worlds_dir() -> Path:
    """Get the directory where custom .apworld files should be placed."""
    arch_dir = get_archipelago_dir()
    return arch_dir / "custom_worlds"


def print_os_info():
    """Print OS and path information for debugging."""
    os_name = get_os_name()
    print(f"OS: {os_name}")
    print(f"Archipelago dir: {get_archipelago_dir()}")
    print(f"Default SSHD extract: {get_default_sshd_extract_path()}")
    print(f"Ryujinx dir: {get_ryujinx_dir()}")
    print(f"Possible mod dirs: {get_ryujinx_mod_dirs()}")

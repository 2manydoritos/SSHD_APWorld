"""
Helper module to decode sshd-rando Setting Strings for Archipelago integration.
Implements the proper binary unpacking algorithm based on sshd-rando's encoder.
"""

import base64
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import yaml

WORLD_DELIMITER = b"\x00:W"


def decode_setting_string_to_config(setting_string: str, output_dir: Path, seed: str = None) -> Any:
    """
    Decode a Setting String and create a fully populated Config object.
    
    Implements the correct binary unpacking that matches sshd-rando's encoder:
    - LSB-first bit ordering within bytes (PackedBitsWriter/Reader)
    - Proper bit width calculation: (option_count - 1).bit_length()
    - Settings in exact order from backend settings_list.yaml (includes random option)
    
    Args:
        setting_string: Base64-encoded Setting String from sshd-rando GUI
        output_dir: Output directory for generated files
        seed: Optional seed override
        
    Returns:
        Config object with all settings populated from the Setting String
    """
    from logic.config import Config, create_default_setting
    from logic.settings import get_all_settings_info, SettingMap
    
    # Decode base64
    try:
        decoded = base64.b64decode(setting_string)
    except Exception as e:
        raise ValueError(f"Failed to decode Setting String (invalid base64): {e}")
    
    # Parse header and world data: "SSHDR-X.X.X\0[spoiler]\0[seed]\0:W[packed_bytes]"
    try:
        header, *worlds = decoded.split(WORLD_DELIMITER)
    except Exception:
        raise ValueError("Invalid Setting String format: missing world delimiter")

    header_parts = header.split(b"\x00", 2)
    if len(header_parts) < 3:
        raise ValueError("Invalid Setting String format: missing header fields")

    version_str = header_parts[0].decode("ascii")
    if not version_str.startswith("SSHDR-"):
        raise ValueError(f"Invalid Setting String: expected 'SSHDR-' prefix, got '{version_str}'")

    print(f"[SettingStringDecoder] Setting String version: {version_str}")

    spoiler_value = header_parts[1]
    embedded_seed = header_parts[2].decode("utf-8")

    if not worlds:
        raise ValueError("Invalid Setting String format: missing world data")

    # Use first world packed bytes
    settings_data = worlds[0]

    print(f"[SettingStringDecoder] Extracted seed: {embedded_seed}")
    print(f"[SettingStringDecoder] Spoiler field (raw bytes): {spoiler_value}")
    print(f"[SettingStringDecoder] Spoiler field (decoded): {spoiler_value.decode('utf-8', errors='replace')}")
    print(f"[SettingStringDecoder] Settings data size: {len(settings_data)} bytes")
    
    # Create config object
    config = Config()
    config.output_dir = output_dir
    config.generate_spoiler_log = False
    
    # Add SettingMap for one world
    config.settings.append(SettingMap())
    setting_map = config.settings[0]
    
    # Initialize all settings to defaults first
    for setting_name in get_all_settings_info():
        setting_map.settings[setting_name] = create_default_setting(setting_name)
    
    # Unpack the binary settings data using correct algorithm
    try:
        # First, decode ALL settings from the bit stream
        print(f"[SettingStringDecoder] Starting bit unpacking from {len(settings_data)} bytes...")
        all_unpacked_settings, bit_position = _unpack_all_settings_data(settings_data)
        
        # Print all decoded settings for debugging
        print(f"[SettingStringDecoder] Total decoded settings: {len(all_unpacked_settings)}")
        for setting_name in sorted(all_unpacked_settings.keys()):
            print(f"[SettingStringDecoder] DEBUG: {setting_name} = {all_unpacked_settings[setting_name]}")
        
        # Create a dictionary to hold all settings for the config
        # This includes settings that may not exist in Archipelago but are needed for hash calculation
        all_settings_dict = {}
        for setting_name, value in all_unpacked_settings.items():
            all_settings_dict[setting_name] = value
        
        # Store all settings in the config object's first world settings
        # This ensures sshd-rando gets all settings when calculating the hash
        for setting_name, value in all_settings_dict.items():
            if setting_name in setting_map.settings:
                setting = setting_map.settings[setting_name]
                # Set the value - catch IndexError for out-of-range values
                try:
                    if hasattr(setting, "info") and hasattr(setting.info, "options"):
                        option_count = len(setting.info.options)
                        random_option = getattr(setting.info, "random_option", None)
                        
                        # Special case: value == option_count encodes the "random" option
                        # (GUI uses value=3 for 3-option settings to mean "random")
                        # Keep it as "random" - sshd-rando will resolve it during generation
                        if value == option_count and random_option and random_option in setting.info.options:
                            value = setting.info.options.index(random_option)
                            print(
                                f"[SettingStringDecoder] INFO: {setting_name} index {option_count} -> "
                                f"'random' option (index {value})"
                            )
                        elif value > option_count - 1:
                            # Genuine out-of-range: clamp to default
                            default_index = getattr(setting.info, "default_option_index", 0)
                            print(
                                f"[SettingStringDecoder] WARNING: {setting_name} index {value} out of range "
                                f"(max {option_count - 1}); clamped to default index {default_index}"
                            )
                            value = default_index

                    if hasattr(setting, "update_current_value"):
                        setting.update_current_value(value)
                    elif hasattr(setting, "update_value"):
                        setting.update_value(value)
                    print(f"[SettingStringDecoder] Applied {setting_name} = {value}")
                except IndexError:
                    print(
                        f"[SettingStringDecoder] WARNING: {setting_name} = {value} is out of range for Archipelago version (skipped)"
                    )
                except Exception as e:
                    print(
                        f"[SettingStringDecoder] WARNING: Error applying {setting_name} = {value}: {e}"
                    )
            else:
                # Setting doesn't exist in Archipelago - try to add it anyway
                print(f"[SettingStringDecoder] Note: {setting_name} = {value} (not in Archipelago, but stored in config)")
                # Store in the settings dict directly if possible
                try:
                    setting_map.settings[setting_name] = value
                except:
                    pass
        
        print(f"[SettingStringDecoder] Successfully decoded and stored {len(all_settings_dict)} settings")
        print(f"[SettingStringDecoder] Consumed {bit_position} bits from Setting String")
        
        # Parse location exclusions and starting inventory
        print(f"[SettingStringDecoder] Parsing location exclusions and starting inventory...")
        try:
            (
                excluded_locations,
                excluded_hint_locations,
                starting_items,
                mixed_entrance_pools,
                inventory_bit_pos,
            ) = _unpack_location_exclusions_and_inventory(settings_data, bit_position)
            print(f"[SettingStringDecoder] Decoded {len(starting_items)} starting items")
            for item_name, count in starting_items.items():
                print(f"[SettingStringDecoder] Starting item: {item_name} x{count}")

            setting_map.excluded_locations = excluded_locations
            setting_map.excluded_hint_locations = excluded_hint_locations
            setting_map.starting_inventory = Counter(starting_items)
            setting_map.mixed_entrance_pools = mixed_entrance_pools
            print(
                f"[SettingStringDecoder] Applied {len(excluded_locations)} excluded locations, "
                f"{len(excluded_hint_locations)} excluded hint locations, "
                f"and {len(starting_items)} starting items"
            )
            print(f"[SettingStringDecoder] Inventory parsing ended at bit {inventory_bit_pos}")
        except Exception as e:
            import traceback
            print(f"[SettingStringDecoder] Warning: Could not decode location exclusions/inventory: {e}")
            print(f"[SettingStringDecoder] Traceback: {traceback.format_exc()}")
            setting_map.excluded_locations = []
            setting_map.excluded_hint_locations = []
            setting_map.starting_inventory = Counter()
            setting_map.mixed_entrance_pools = []
    except Exception as e:
        import traceback
        print(f"[SettingStringDecoder] Warning: Failed to unpack some settings: {e}")
        print(f"[SettingStringDecoder] Traceback: {traceback.format_exc()}")
        print(f"[SettingStringDecoder] Using defaults for unparseable settings")
    
    # Set the seed directly on the config object (not in settings map)
    if seed:
        config.seed = seed
        print(f"[SettingStringDecoder] Using override seed: {seed}")
    elif embedded_seed:
        config.seed = embedded_seed
        print(f"[SettingStringDecoder] Using embedded seed: {embedded_seed}")
    
    # Set the spoiler log flag from the Setting String
    # spoiler_value is b'0' or b'1' - whether to generate spoiler logs
    # This flag affects hash calculation, so it must match the original
    try:
        spoiler_flag_str = spoiler_value.decode("utf-8").strip()
        config.generate_spoiler_log = spoiler_flag_str == "1"
        print(f"[SettingStringDecoder] Setting generate_spoiler_log = {config.generate_spoiler_log} (from spoiler field: {spoiler_flag_str})")
    except Exception as e:
        print(f"[SettingStringDecoder] Warning: Could not decode spoiler flag: {e}")
        config.generate_spoiler_log = False  # Default to False (no spoiler log)
    
    return config


class BitReader:
    """Helper class to read packed bits using sshd-rando's LSB-first order."""

    def __init__(self, data: bytes):
        self.bytes = bytearray(data)
        self.current_byte_index = 0
        self.current_bit_index = 0
        self.bit_pos = 0

    def read(self, num_bits: int) -> int:
        """Read num_bits bits and return as integer (LSB-first)."""
        if num_bits == 0:
            return 0

        bits_read = 0
        value = 0
        bits_left_to_read = num_bits

        while bits_read != num_bits:
            bits_to_read = 8 if bits_left_to_read > 8 else bits_left_to_read
            if bits_to_read + self.current_bit_index > 8:
                bits_to_read = 8 - self.current_bit_index

            mask = ((1 << bits_to_read) - 1) << self.current_bit_index
            if self.current_byte_index >= len(self.bytes):
                raise ValueError(f"Ran out of data reading Setting String at bit {self.bit_pos}")

            current_byte = self.bytes[self.current_byte_index]
            value = ((current_byte & mask) >> self.current_bit_index) << bits_read | value

            self.current_bit_index += bits_to_read
            self.current_byte_index += self.current_bit_index >> 3
            self.current_bit_index %= 8
            bits_left_to_read -= bits_to_read
            bits_read += bits_to_read

        self.bit_pos = self.current_byte_index * 8 + self.current_bit_index
        return value


def _unpack_settings_data(data: bytes) -> Dict[str, int]:
    """
    Unpack bit-packed settings data from Setting String using correct LSB-first algorithm.
    Only returns settings that exist in Archipelago.
    
    Args:
        data: Binary packed settings data
        
    Returns:
        Dictionary mapping setting names to their option indices
    """
    from logic.settings import get_all_settings_info
    
    reader = BitReader(data)
    unpacked = {}
    
    # Get all settings info (Archipelago subset)
    setting_info_dict = get_all_settings_info()
    
    # Settings and their bit widths - MUST include all vanilla settings to stay in sync
    settings_with_bits = _get_settings_with_bitwidths()
    
    for setting_name, bit_width in settings_with_bits:
        if bit_width > 0:
            try:
                value = reader.read(bit_width)
                
                # Only store if this setting exists in Archipelago
                if setting_name in setting_info_dict:
                    unpacked[setting_name] = value
                    print(f"[SettingStringDecoder] BIT READ #{len(unpacked)}: {setting_name} = {value} ({bit_width} bits)")
                # else: skip silently - this setting doesn't exist in Archipelago version
                    
            except ValueError as e:
                print(f"[SettingStringDecoder] WARNING: Failed at {setting_name} after {len(unpacked)} decoded settings")
                print(f"[SettingStringDecoder] Error: {e}")
                break
    
    return unpacked


def _unpack_all_settings_data(data: bytes) -> tuple:
    """
    Unpack bit-packed settings data from Setting String, returning ALL settings.
    
    Args:
        data: Binary packed settings data
        
    Returns:
        Tuple of (dict of all settings, bit position after reading)
    """
    reader = BitReader(data)
    unpacked = {}
    
    # Settings and their bit widths - MUST include all vanilla settings to stay in sync
    settings_with_bits = _get_settings_with_bitwidths()
    
    for setting_name, bit_width in settings_with_bits:
        if bit_width > 0:
            try:
                value = reader.read(bit_width)
                unpacked[setting_name] = value
                    
            except ValueError as e:
                print(f"[SettingStringDecoder] WARNING: Failed at {setting_name}")
                print(f"[SettingStringDecoder] Error: {e}")
                break
    
    return unpacked, reader.bit_pos


def _get_settings_with_bitwidths() -> List[tuple]:
    """
    Get ordered list of (setting_name, bit_width) for ALL sshd-rando settings.
    
    This must be kept in sync with the actual sshd-rando settings_list.yaml
    and the encoder's setting order. Even settings not in Archipelago must be
    included to avoid bit stream desynchronization.
    
    Returns:
        List of (setting_name, bit_width) tuples in encoding order
    """
    # Prefer backend settings list when available (authoritative order)
    backend_settings = _get_backend_settings_with_bitwidths()
    if backend_settings:
        return backend_settings

    # Fallback to parsing settings_list.yaml directly (full-source or backend copy)
    yaml_settings = _get_settings_with_bitwidths_from_yaml()
    if yaml_settings:
        return yaml_settings

    # Final fallback to hardcoded list (may be out of date)
    return [
        ('logic_rules', 2),                                    # 3 options
        ('item_pool', 2),                                      # 4 options
        ('enable_back_in_time', 1),                           # 2 options
        ('gratitude_crystal_shuffle', 1),                     # 2 options
        ('stamina_fruit_shuffle', 1),                         # 2 options
        ('npc_closet_shuffle', 1),                            # 2 options
        ('hidden_item_shuffle', 1),                           # 2 options
        ('rupee_shuffle', 2),                                 # 4 options
        ('underground_rupee_shuffle', 1),                     # 2 options
        ('beedle_shop_shuffle', 2),                           # 3 options
        ('goddess_chest_shuffle', 1),                         # 2 options
        ('trial_treasure_shuffle', 4),                        # 11 options (0-10)
        ('tadtone_shuffle', 1),                               # 2 options
        ('gossip_stone_treasure_shuffle', 1),                 # 2 options
        ('full_wallet_upgrades', 1),                          # 2 options
        ('skip_harp_playing', 1),                             # 2 options
        ('random_trial_object_positions', 2),                 # 4 options
        ('randomize_skykeep_layout', 1),                      # 2 options
        ('peatrice_conversations', 3),                        # 7 options (0-6)
        ('small_keys', 3),                                    # 7 options
        ('lanayru_caves_keys', 2),                            # 4 options
        ('boss_keys', 3),                                     # 7 options
        ('map_mode', 3),                                      # 7 options
        ('chest_type_matches_contents', 2),                   # 3 options
        ('small_keys_in_fancy_chests', 1),                    # 2 options
        ('path_hints', 3),                                    # 8 options (0-7)
        ('path_hints_on_fi', 1),                              # 2 options
        ('path_hints_on_gossip_stones', 1),                   # 2 options
        ('barren_hints', 3),                                  # 8 options (0-7)
        ('barren_hints_on_fi', 1),                            # 2 options
        ('barren_hints_on_gossip_stones', 1),                 # 2 options
        ('location_hints', 3),                                # 8 options (0-7)
        ('location_hints_on_fi', 1),                          # 2 options
        ('location_hints_on_gossip_stones', 1),               # 2 options
        ('item_hints', 3),                                    # 8 options (0-7)
        ('item_hints_on_fi', 1),                              # 2 options
        ('item_hints_on_gossip_stones', 1),                   # 2 options
        ('song_hints', 2),                                    # 4 options
        ('impa_sot_hint', 1),                                 # 2 options
        ('cryptic_hint_text', 1),                             # 2 options
        ('always_hints', 1),                                  # 2 options
        ('hint_importance', 1),                               # 2 options
        ('random_starting_statues', 1),                       # 2 options
        ('random_starting_spawn', 2),                         # 4 options
        ('limit_starting_spawn', 1),                          # 2 options
        ('randomize_dungeon_entrances', 1),                   # 2 options
        ('randomize_trial_gate_entrances', 1),                # 2 options
        ('randomize_door_entrances', 1),                      # 2 options
        ('decouple_double_doors', 1),                         # 2 options
        ('randomize_interior_entrances', 1),                  # 2 options
        ('randomize_overworld_entrances', 1),                 # 2 options
        ('decouple_entrances', 1),                            # 2 options
        ('natural_night_connections', 1),                     # 2 options
        ('allow_flying_at_night', 1),                         # 2 options
        ('skip_horde', 1),                                    # 2 options
        ('skip_g3', 1),                                       # 2 options
        ('skip_demise', 1),                                   # 2 options
        ('required_dungeons', 3),                             # 8 options (0-7)
        ('dungeons_include_sky_keep', 1),                     # 2 options
        ('empty_unrequired_dungeons', 1),                     # 2 options ← position 60
        ('randomize_shop_prices', 1),                         # 2 options
        ('random_bottle_contents', 1),                        # 2 options
        ('trap_mode', 3),                                     # 5 options (0-4)
        ('trappable_items', 2),                               # 3 options
        ('burn_traps', 1),                                    # 2 options
        ('curse_traps', 1),                                   # 2 options
        ('noise_traps', 1),                                   # 2 options
        ('groose_traps', 1),                                  # 2 options
        ('health_traps', 1),                                  # 2 options
        ('ammo_availability', 2),                             # 4 options
        ('boss_key_puzzles', 2),                              # 3 options
        ('got_sword_requirement', 3),                         # 5 options (0-4)
        ('upgraded_skyward_strike', 1),                       # 2 options
        ('faster_air_meter_depletion', 1),                    # 2 options
        ('spawn_hearts', 1),                                  # 2 options
        ('damage_multiplier', 7),                             # 81 options (0-80)
        ('unlock_all_groosenator_destinations', 1),           # 2 options
        ('minigame_difficulty', 2),                           # 4 options
        ('skip_misc_small_cutscenes', 1),                     # 2 options
        # Cosmetic settings are SKIPPED in encoding order
        ('open_thunderhead', 1),                              # 2 options
        ('open_lake_floria', 2),                              # 3 options
        ('open_earth_temple', 2),                             # 3 options
        ('open_lmf', 2),                                      # 3 options
        ('open_batreaux_shed', 1),                            # 2 options
        ('shortcut_ios_bridge_complete', 1),                  # 2 options
        ('shortcut_spiral_log_to_btt', 1),                    # 2 options
        ('shortcut_logs_near_machi', 1),                      # 2 options
        ('shortcut_faron_log_to_floria', 1),                  # 2 options
        ('shortcut_deep_woods_log_before_tightrope', 1),      # 2 options
        ('shortcut_deep_woods_log_before_temple', 1),         # 2 options
        ('shortcut_eldin_entrance_boulder', 1),               # 2 options
        ('shortcut_eldin_ascent_boulder', 1),                 # 2 options
        ('shortcut_vs_flames', 1),                            # 2 options
        ('shortcut_lanayru_bars', 1),                         # 2 options
        ('shortcut_west_wall_minecart', 1),                   # 2 options
        ('shortcut_sand_oasis_minecart', 1),                  # 2 options
        ('shortcut_minecart_before_caves', 1),                # 2 options
        ('shortcut_skyview_boards', 1),                       # 2 options
        ('shortcut_skyview_bars', 1),                         # 2 options
        ('shortcut_earth_temple_bridge', 1),                  # 2 options
        ('shortcut_lmf_wind_gates', 1),                       # 2 options
        ('shortcut_lmf_boxes', 1),                            # 2 options
        ('shortcut_lmf_bars_to_west_side', 1),                # 2 options
        ('shortcut_ac_bridge', 1),                            # 2 options
        ('shortcut_ac_water_vents', 1),                       # 2 options
        ('shortcut_sandship_windows', 1),                     # 2 options
        ('shortcut_sandship_brig_bars', 1),                   # 2 options
        ('shortcut_fs_outside_bars', 1),                      # 2 options
        ('shortcut_fs_lava_flow', 1),                         # 2 options
        ('shortcut_sky_keep_svt_room_bars', 1),               # 2 options
        ('shortcut_sky_keep_fs_room_lower_bars', 1),          # 2 options
        ('shortcut_sky_keep_fs_room_upper_bars', 1),          # 2 options
        # Logic/trick settings (all 1 bit each)
        ('logic_early_lake_floria', 1),
        ('logic_beedles_island_cage_chest_dive', 1),
        ('logic_volcanic_island_dive', 1),
        ('logic_east_island_dive', 1),
        ('logic_advanced_lizalfos_combat', 1),
        ('logic_long_ranged_skyward_strikes', 1),
        ('logic_gravestone_jump', 1),
        ('logic_waterfall_cave_jump', 1),
        ('logic_bird_nest_item_from_beedles_shop', 1),
        ('logic_beedles_shop_with_bombs', 1),
        ('logic_stuttersprint', 1),
        ('logic_precise_beetle', 1),
        ('logic_bomb_throws', 1),
        ('logic_faron_woods_with_groosenator', 1),
        ('logic_itemless_first_timeshift_stone', 1),
        ('logic_stamina_potion_through_sink_sand', 1),
        ('logic_brakeslide', 1),
        ('logic_lanayru_mine_quick_bomb', 1),
        ('logic_tot_skip_brakeslide', 1),
        ('logic_tot_slingshot', 1),
        ('logic_fire_node_without_hook_beetle', 1),
        ('logic_cactus_bomb_whip', 1),
        ('logic_skippers_fast_clawshots', 1),
        ('logic_skyview_spider_roll', 1),
        ('logic_skyview_coiled_rupee_jump', 1),
        ('logic_skyview_precise_slingshot', 1),
        ('logic_et_keese_skyward_strike', 1),
        ('logic_et_slope_stuttersprint', 1),
        ('logic_et_bombless_scaldera', 1),
        ('logic_lmf_whip_switch', 1),
        ('logic_lmf_ceiling_precise_slingshot', 1),
        ('logic_lmf_whip_armos_room_timeshift_stone', 1),
        ('logic_lmf_minecart_jump', 1),
        ('logic_lmf_bellowsless_moldarach', 1),
        ('logic_ac_lever_jump_trick', 1),
        ('logic_ac_chest_after_whip_hooks_jump', 1),
        ('logic_sandship_jump_to_stern', 1),
        ('logic_sandship_itemless_spume', 1),
        ('logic_sandship_no_combination_hint', 1),
        ('logic_fs_pillar_jump', 1),
        ('logic_fs_practice_sword_ghirahim_2', 1),
        ('logic_present_bow_switches', 1),
        ('logic_skykeep_vineclip', 1),
        # Starting inventory
        ('starting_sword', 3),                                # 7 options (0-6) ← position 156
        ('random_starting_tablet_count', 2),                  # 4 options (0-3)
        ('random_starting_item_count', 3),                    # 8 options (0-7)
        ('starting_hearts', 4),                               # 13 options (6-18)
        ('start_with_all_bugs', 1),                           # 2 options
        ('start_with_all_treasures', 1),                      # 2 options
    ]


def _get_option_count_from_yaml_options(options: Any) -> int:
    """Compute option count from settings_list.yaml options, including numeric ranges."""
    if not isinstance(options, list):
        return len(options) if options else 0

    if len(options) == 1 and isinstance(options[0], dict) and options[0]:
        key = next(iter(options[0].keys()))
        if isinstance(key, str):
            import re
            range_match = re.match(r"^\s*(-?\d+)\s*-\s*(-?\d+)\s*$", key)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                if end >= start:
                    return end - start + 1

    return len(options)


def _find_backend_path() -> Path | None:
    """Locate the extracted sshd-rando-backend path when running from apworld or source."""
    try:
        import logic

        return Path(logic.__file__).resolve().parent.parent
    except Exception:
        pass

    try:
        from . import SSHD_RANDO_PATH, SSHD_RANDO_TEMP_DIR

        if SSHD_RANDO_TEMP_DIR:
            candidate = Path(SSHD_RANDO_TEMP_DIR) / "sshd-rando-backend"
            if candidate.exists():
                return candidate

        if SSHD_RANDO_PATH and Path(SSHD_RANDO_PATH).exists():
            return Path(SSHD_RANDO_PATH)
    except Exception:
        pass

    candidate = Path(__file__).resolve().parent / "sshd-rando-backend"
    if candidate.exists():
        return candidate

    return None


def _find_settings_list_path() -> Path | None:
    """Locate settings_list.yaml from backend or full-source repo."""
    backend_path = _find_backend_path()
    if backend_path:
        backend_settings = backend_path / "data" / "settings_list.yaml"
        if backend_settings.exists():
            return backend_settings

    full_source_settings = (
        Path(__file__).resolve().parent
        / "sshd-rando-full-source-code"
        / "data"
        / "settings_list.yaml"
    )
    if full_source_settings.exists():
        return full_source_settings

    return None


def _get_settings_with_bitwidths_from_yaml() -> List[tuple]:
    """
    Parse settings_list.yaml directly to derive setting order and bit widths.

    This mirrors sshd-rando's YAML parsing logic, including auto-appending
    the random option when applicable.
    """
    settings_path = _find_settings_list_path()
    if not settings_path:
        return []

    try:
        settings_yaml = yaml.safe_load(settings_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(
            f"[SettingStringDecoder] WARNING: Could not read settings_list.yaml: {e}"
        )
        return []

    settings_with_bits: List[tuple] = []

    for setting_node in settings_yaml:
        if setting_node.get("type") == "Cosmetic":
            continue

        name_str = str(setting_node["name"])
        names = [name.strip() for name in name_str.split(",")]

        pretty_options: list[str] = []
        for pretty_option in setting_node.get("pretty_options", []):
            pretty_option = str(pretty_option)
            if "-" in pretty_option:
                lower_bound, upper_bound = [
                    int(bound) for bound in pretty_option.split("-")
                ]
                pretty_options.extend(
                    str(o) for o in list(range(lower_bound, upper_bound + 1))
                )
            else:
                pretty_options.append(pretty_option)

        options: list[str] = []
        for option in setting_node.get("options", []):
            for option_name in option.keys():
                for op in str(option_name).split("/"):
                    if "-" in op:
                        lower_bound, upper_bound = [int(bound) for bound in op.split("-")]
                        options.extend(
                            str(o) for o in list(range(lower_bound, upper_bound + 1))
                        )
                    else:
                        options.append(op)

        if "no_autogenerate_random" not in setting_node:
            random_option = setting_node.get("random_alias", "random")
            if random_option not in options:
                options.append(random_option)

        option_count = len(options)
        bit_width = (option_count - 1).bit_length() if option_count > 1 else 0

        for name in names:
            settings_with_bits.append((name, bit_width))

    return settings_with_bits


def _get_backend_settings_with_bitwidths() -> List[tuple]:
    """
    Attempt to load settings order and bit widths from sshd-rando-backend.

    Returns an empty list if backend settings cannot be loaded.
    """
    try:
        import sys

        backend_path = _find_backend_path()
        if backend_path and str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))

        from logic.settings import get_all_settings_info, SettingType

        settings_with_bits: List[tuple] = []
        settings_info = get_all_settings_info()

        for setting_name, setting_info in settings_info.items():
            if setting_info.type == SettingType.COSMETIC:
                continue

            option_count = len(setting_info.options)
            bit_width = (option_count - 1).bit_length() if option_count > 1 else 0
            settings_with_bits.append((setting_name, bit_width))

        return settings_with_bits
    except Exception as e:
        print(f"[SettingStringDecoder] WARNING: Could not load backend settings list: {e}")
        return []


def _is_cosmetic_setting(setting_name: str) -> bool:
    """Check if a setting is cosmetic (excluded from Setting String)."""
    cosmetic_prefixes = ['text_', 'color_', 'ui_']
    for prefix in cosmetic_prefixes:
        if setting_name.startswith(prefix):
            return True
    
    # List of known cosmetic settings
    cosmetic_settings = {
        'language',
        'skip_cutscenes_text',
        'hero_mode_music_swap',
        'heroine_mode_music_swap',
        'music_selection',
    }
    
    return setting_name in cosmetic_settings


def _get_setting_pack_order() -> List[str]:
    """
    Get the exact order in which settings are packed in Setting Strings.
    This order MUST match sshd-rando's encoder (non-cosmetic settings only).
    
    Based on sshd-rando's actual binary encoder implementation.
    """
    return [
        'logic_rules',
        'item_pool',
        'enable_back_in_time',
        'gratitude_crystal_shuffle',
        'stamina_fruit_shuffle',
        'npc_closet_shuffle',
        'hidden_item_shuffle',
        'rupee_shuffle',
        'underground_rupee_shuffle',
        'beedle_shop_shuffle',
        'goddess_chest_shuffle',
        'trial_treasure_shuffle',
        'tadtone_shuffle',
        'gossip_stone_treasure_shuffle',
        'full_wallet_upgrades',
        'skip_harp_playing',
        'random_trial_object_positions',
        'randomize_skykeep_layout',
        'peatrice_conversations',
        'small_keys',
        'lanayru_caves_keys',
        'boss_keys',
        'map_mode',
        'chest_type_matches_contents',
        'small_keys_in_fancy_chests',
        'path_hints',
        'path_hints_on_fi',
        'path_hints_on_gossip_stones',
        'barren_hints',
        'barren_hints_on_fi',
        'barren_hints_on_gossip_stones',
        'location_hints',
        'location_hints_on_fi',
        'location_hints_on_gossip_stones',
        'item_hints',
        'item_hints_on_fi',
        'item_hints_on_gossip_stones',
        'song_hints',
        'impa_sot_hint',
        'cryptic_hint_text',
        'always_hints',
        'hint_importance',
        'random_starting_statues',
        'random_starting_spawn',
        'limit_starting_spawn',
        'randomize_dungeon_entrances',
        'randomize_trial_gate_entrances',
        'randomize_door_entrances',
        'decouple_double_doors',
        'randomize_interior_entrances',
        'randomize_overworld_entrances',
        'decouple_entrances',
        'natural_night_connections',
        'allow_flying_at_night',
        'skip_horde',
        'skip_g3',
        'skip_demise',
        'required_dungeons',
        'dungeons_include_sky_keep',
        'empty_unrequired_dungeons',
        'randomize_shop_prices',
        'random_bottle_contents',
        'trap_mode',
        'trappable_items',
        'burn_traps',
        'curse_traps',
        'noise_traps',
        'groose_traps',
        'health_traps',
        'ammo_availability',
        'boss_key_puzzles',
        'got_sword_requirement',
        'upgraded_skyward_strike',
        'faster_air_meter_depletion',
        'spawn_hearts',
        'damage_multiplier',
        'unlock_all_groosenator_destinations',
        'minigame_difficulty',
        'skip_misc_small_cutscenes',
        # Cosmetic settings are SKIPPED in Setting String
        # language, tunic_swap, lightning_skyward_strike, starry_skies, etc.
        'open_thunderhead',
        'open_lake_floria',
        'open_earth_temple',
        'open_lmf',
        'open_batreaux_shed',
        'shortcut_ios_bridge_complete',
        'shortcut_spiral_log_to_btt',
        'shortcut_logs_near_machi',
        'shortcut_faron_log_to_floria',
        'shortcut_deep_woods_log_before_tightrope',
        'shortcut_deep_woods_log_before_temple',
        'shortcut_eldin_entrance_boulder',
        'shortcut_eldin_ascent_boulder',
        'shortcut_vs_flames',
        'shortcut_lanayru_bars',
        'shortcut_west_wall_minecart',
        'shortcut_sand_oasis_minecart',
        'shortcut_minecart_before_caves',
        'shortcut_skyview_boards',
        'shortcut_skyview_bars',
        'shortcut_earth_temple_bridge',
        'shortcut_lmf_wind_gates',
        'shortcut_lmf_boxes',
        'shortcut_lmf_bars_to_west_side',
        'shortcut_ac_bridge',
        'shortcut_ac_water_vents',
        'shortcut_sandship_windows',
        'shortcut_sandship_brig_bars',
        'shortcut_fs_outside_bars',
        'shortcut_fs_lava_flow',
        'shortcut_sky_keep_svt_room_bars',
        'shortcut_sky_keep_fs_room_lower_bars',
        'shortcut_sky_keep_fs_room_upper_bars',
        # Logic/trick settings (all 1 bit each)
        'logic_early_lake_floria',
        'logic_beedles_island_cage_chest_dive',
        'logic_volcanic_island_dive',
        'logic_east_island_dive',
        'logic_advanced_lizalfos_combat',
        'logic_long_ranged_skyward_strikes',
        'logic_gravestone_jump',
        'logic_waterfall_cave_jump',
        'logic_bird_nest_item_from_beedles_shop',
        'logic_beedles_shop_with_bombs',
        'logic_stuttersprint',
        'logic_precise_beetle',
        'logic_bomb_throws',
        'logic_faron_woods_with_groosenator',
        'logic_itemless_first_timeshift_stone',
        'logic_stamina_potion_through_sink_sand',
        'logic_brakeslide',
        'logic_lanayru_mine_quick_bomb',
        'logic_tot_skip_brakeslide',
        'logic_tot_slingshot',
        'logic_fire_node_without_hook_beetle',
        'logic_cactus_bomb_whip',
        'logic_skippers_fast_clawshots',
        'logic_skyview_spider_roll',
        'logic_skyview_coiled_rupee_jump',
        'logic_skyview_precise_slingshot',
        'logic_et_keese_skyward_strike',
        'logic_et_slope_stuttersprint',
        'logic_et_bombless_scaldera',
        'logic_lmf_whip_switch',
        'logic_lmf_ceiling_precise_slingshot',
        'logic_lmf_whip_armos_room_timeshift_stone',
        'logic_lmf_minecart_jump',
        'logic_lmf_bellowsless_moldarach',
        'logic_ac_lever_jump_trick',
        'logic_ac_chest_after_whip_hooks_jump',
        'logic_sandship_jump_to_stern',
        'logic_sandship_itemless_spume',
        'logic_sandship_no_combination_hint',
        'logic_fs_pillar_jump',
        'logic_fs_practice_sword_ghirahim_2',
        'logic_present_bow_switches',
        'logic_skykeep_vineclip',
        # Starting inventory
        'starting_sword',
        'random_starting_tablet_count',
        'random_starting_item_count',
        'starting_hearts',
        'start_with_all_bugs',
        'start_with_all_treasures',
    ]


def _unpack_settings_data(data: bytes) -> Dict[str, int]:
    """
    Unpack bit-packed settings data from Setting String.
    
    sshd-rando packs settings as variable-length bit fields based on option count.
    Settings are packed in a specific order defined by the randomizer.
    
    Args:
        data: Binary packed settings data
        
    Returns:
        Dictionary mapping setting names to their values (option index or list for multi-value)
    """
    from logic.settings import get_all_settings_info
    
    # Convert bytes to bit array (LSB first within each byte)
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> i) & 1)
    
    # Get all setting info
    setting_info_dict = get_all_settings_info()
    
    # Define setting order - must match sshd-rando's encode order
    setting_order = _get_setting_pack_order()
    
    unpacked = {}
    bit_pos = 0
    
    for setting_name in setting_order:
        if bit_pos >= len(bits):
            break
            
        if setting_name not in setting_info_dict:
            continue
            
        setting = setting_info_dict[setting_name]
        
        # Handle multi-value settings (like starting_items)
        if hasattr(setting, 'is_list') and setting.is_list:
            # For list settings, first read the count
            count_bits = 8  # Assume 8 bits for count
            if bit_pos + count_bits > len(bits):
                break
                
            item_count = 0
            for i in range(count_bits):
                if bits[bit_pos + i]:
                    item_count |= (1 << i)
            bit_pos += count_bits
            
            # Now read each item ID
            items = []
            for _ in range(item_count):
                item_bits = 10  # Assume 10 bits per item ID
                if bit_pos + item_bits > len(bits):
                    break
                    
                item_id = 0
                for i in range(item_bits):
                    if bits[bit_pos + i]:
                        item_id |= (1 << i)
                bit_pos += item_bits
                items.append(item_id)
            
            unpacked[setting_name] = items
        else:
            # Regular single-value setting
            # Calculate bits needed
            if hasattr(setting, 'options'):
                option_count = len(setting.options)
            elif hasattr(setting, 'type') and setting.type == 'boolean':
                option_count = 2
            else:
                option_count = 2  # Default to boolean
            
            bits_needed = _calculate_bits_needed(option_count)
            
            if bits_needed == 0 or bit_pos + bits_needed > len(bits):
                bit_pos += bits_needed if bits_needed > 0 else 0
                continue
            
            # Extract value (LSB first)
            value = 0
            for i in range(bits_needed):
                if bits[bit_pos + i]:
                    value |= (1 << i)
            
            unpacked[setting_name] = value
            bit_pos += bits_needed
    
    return unpacked


def _calculate_bits_needed(option_count: int) -> int:
    """Calculate number of bits needed to represent option_count values."""
    if option_count <= 1:
        return 0
    bits = 0
    value = option_count - 1
    while value > 0:
        bits += 1
        value >>= 1
    return bits


def _get_setting_pack_order() -> List[str]:
    """
    Get the order in which settings are packed in Setting Strings.
    
    This must match the order used by sshd-rando's Setting String encoder.
    Based on sshd-rando 2.2.x setting pack order.
    """
    return [
        'logic_mode',
        'empty_unrequired_dungeons',
        'required_dungeon_count',
        'triforce_required',
        'triforce_shuffle',
        'starting_sword',
        'starting_tablet_count',
        'small_keys',
        'boss_keys',
        'map_mode',
        'gratitude_crystal_shuffle',
        'gratitude_crystal_amount',
        'stamina_fruit_shuffle',
        'npc_closet_shuffle',
        'hidden_item_shuffle',
        'rupee_mode',
        'goddess_chest_shuffle',
        'trial_treasure_amount',
        'tadtone_shuffle',
        'gossip_stone_treasure_shuffle',
        'randomize_dungeon_entrances',
        'randomize_trial_gate_entrances',
        'randomize_silent_realm_entrances',
        'randomize_boss_entrances',
        'randomize_bird_statue_destinations',
        'damage_multiplier',
        'randomize_music',
        'cutoff_game_over_music',
        'open_lake_floria',
        'open_thunderhead',
        'skip_skyward_strike',
        'skip_harp_playing',
        'skip_mine_cart_cutscenes',
        'skip_imprisoned_fight',
        'skip_ghirahim_3_fight',
        'skip_demise_fight',
        'skip_skykeep_door_cutscene',
        'skip_misc_small_cutscenes',
        'starting_pouch_capacity',
        'starting_items',  # This is a multi-value field
        'rupeesanity',
        'treasuresanity',
        'upgradesanity',
        'materialsanity',
        'bugsanity',
        'heromode_hp_multiplier',
        'spawn_hearts',
    ]


def _unpack_location_exclusions_and_inventory(data: bytes, bit_offset: int) -> tuple:
    """
    Unpack location exclusions and starting inventory from Setting String.

    Format:
    - After all 161 settings
    - 1 bit per location in location_table order
    - Variable-width starting inventory counts using Counter(STARTABLE_ITEMS)

    Args:
        data: Binary settings data
        bit_offset: Starting bit position (after all settings have been read)

    Returns:
        Tuple of (excluded_locations, excluded_hint_locations, starting_items, mixed_entrance_pools, bit_pos)
    """
    reader = BitReader(data)
    reader.current_byte_index = bit_offset // 8
    reader.current_bit_index = bit_offset % 8
    reader.bit_pos = bit_offset

    excluded_locations: list[str] = []
    excluded_hint_locations: list[str] = []

    # Import backend data to match sshd-rando's exact order
    import sys

    backend_path = _find_backend_path()
    if backend_path and str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

    try:
        from sslib.yaml import yaml_load
    except Exception:
        yaml_load = None

    from logic.location_table import build_location_table
    from constants.itemconstants import STARTABLE_ITEMS
    from constants.configconstants import ENTRANCE_TYPES

    if backend_path:
        locations_path = backend_path / "data" / "locations.yaml"
        if yaml_load and locations_path.exists():
            yaml_load(locations_path)

    location_table = build_location_table(None)

    all_locations = list(location_table.items())
    non_hint_locations = [
        (name, loc)
        for name, loc in all_locations
        if "Hint Location" not in loc.types
    ]

    remaining_bits = (len(data) * 8) - bit_offset
    startable_items = Counter(STARTABLE_ITEMS)
    startable_bits = sum(
        startable_items[item_name].bit_length() for item_name in startable_items
    )
    entrance_bits = len(ENTRANCE_TYPES) * (len(ENTRANCE_TYPES).bit_length())
    location_bits_available = remaining_bits - (startable_bits + entrance_bits)

    print("[SettingStringDecoder] Inventory/exclusions bit accounting:")
    print(f"[SettingStringDecoder]   Total bits: {len(data) * 8}")
    print(f"[SettingStringDecoder]   Remaining bits: {remaining_bits}")
    print(f"[SettingStringDecoder]   Startable bits: {startable_bits}")
    print(f"[SettingStringDecoder]   Entrance bits: {entrance_bits}")
    print(f"[SettingStringDecoder]   Location bits available: {location_bits_available}")

    if location_bits_available == len(all_locations):
        locations_to_read = all_locations
    elif location_bits_available == len(non_hint_locations):
        locations_to_read = non_hint_locations
        print(
            "[SettingStringDecoder] INFO: Excluding hint locations from exclusion bitfield"
        )
    else:
        locations_to_read = all_locations
        print(
            f"[SettingStringDecoder] WARNING: Unexpected location bit count ({location_bits_available}); "
            f"defaulting to full location list ({len(all_locations)})"
        )

    print(f"[SettingStringDecoder] Location exclusion parsing:")
    print(f"[SettingStringDecoder]   Bit position after settings: {bit_offset}")
    print(f"[SettingStringDecoder]   Location count: {len(locations_to_read)}")

    for location_name, location in locations_to_read:
        if reader.read(1):
            if "Hint Location" in location.types:
                excluded_hint_locations.append(location_name)
            else:
                excluded_locations.append(location_name)

    starting_items: Dict[str, int] = {}

    for item_name in startable_items:
        bit_width = startable_items[item_name].bit_length()
        item_count = reader.read(bit_width)
        if item_count > 0:
            starting_items[item_name] = item_count

    mixed_entrance_pools: list[list[str]] = [
        list() for _ in range(len(ENTRANCE_TYPES) - 1)
    ]
    entrance_bit_width = len(ENTRANCE_TYPES).bit_length()

    for entrance_type in ENTRANCE_TYPES:
        pool_index = reader.read(entrance_bit_width)
        if pool_index >= len(mixed_entrance_pools):
            continue
        mixed_entrance_pools[pool_index].append(entrance_type)

    return (
        excluded_locations,
        excluded_hint_locations,
        starting_items,
        mixed_entrance_pools,
        reader.bit_pos,
    )


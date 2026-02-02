"""
Stub implementation of setting_string module for Archipelago integration.
This provides compatibility functions for the sshd-rando-backend logic module.
"""

def setting_string_from_config(config, location_table):
    """
    Generate a setting string from config for display/logging purposes.
    
    Args:
        config: Config object containing randomizer settings
        location_table: Location table from the world
        
    Returns:
        str: A formatted string representing the configuration
    """
    # Generate a basic setting string from config attributes
    parts = []
    
    if hasattr(config, 'seed'):
        parts.append(f"Seed:{config.seed}")
    
    if hasattr(config, 'settings') and config.settings:
        # Get first world settings if available
        if len(config.settings) > 0:
            setting_map = config.settings[0]
            
            # Add key settings to the string
            key_settings = [
                'logic_mode',
                'empty_unrequired_dungeons',
                'starting_sword',
                'starting_tablet_count',
                'damage_multiplier'
            ]
            
            for setting_key in key_settings:
                try:
                    # Try to get the setting value using getattr or dict access
                    if hasattr(setting_map, setting_key):
                        value = getattr(setting_map, setting_key)
                        parts.append(f"{setting_key}:{value}")
                    elif hasattr(setting_map, '__getitem__'):
                        value = setting_map.get(setting_key)
                        if value is not None:
                            parts.append(f"{setting_key}:{value}")
                except (AttributeError, KeyError, TypeError):
                    # Skip settings that can't be accessed
                    pass
    
    return "|".join(parts) if parts else "default"

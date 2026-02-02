"""
Hint system for Skyward Sword HD Archipelago.

This module handles receiving hints from the Archipelago server and
making them available to the player in-game via gossip stones or the client UI.
"""

from typing import Dict, List, Optional, Set, Tuple


class HintSystem:
    """
    Manages hints for multiworld items.
    
    Hints are received from the Archipelago server and can be:
    - Displayed in the client UI
    - Written to in-game gossip stones (requires memory address research)
    - Stored for player reference
    """
    
    def __init__(self):
        self.hints: Dict[int, str] = {}  # location_id -> hint_text
        self.gossip_stones: Dict[str, int] = {}  # stone_name -> location_id
        self.revealed_hints: Set[int] = set()  # location_ids that have been revealed
        
    def add_hint(self, location_id: int, hint_text: str):
        """
        Add a hint for a specific location.
        
        Args:
            location_id: The Archipelago location ID
            hint_text: The hint text (e.g., "The item at Skyview Temple is Link's Bow")
        """
        self.hints[location_id] = hint_text
        
    def get_hint(self, location_id: int) -> Optional[str]:
        """Get the hint for a specific location."""
        return self.hints.get(location_id)
    
    def get_all_hints(self) -> List[Tuple[int, str]]:
        """Get all available hints."""
        return [(loc_id, hint) for loc_id, hint in self.hints.items()]
    
    def reveal_hint(self, location_id: int):
        """Mark a hint as revealed (player has read it)."""
        self.revealed_hints.add(location_id)
        
    def is_revealed(self, location_id: int) -> bool:
        """Check if a hint has been revealed."""
        return location_id in self.revealed_hints
    
    def assign_hint_to_gossip_stone(self, stone_name: str, location_id: int):
        """
        Assign a hint to a specific gossip stone.
        
        Args:
            stone_name: Name of the gossip stone (e.g., "Skyloft - Waterfall Cave")
            location_id: The location ID this stone hints about
        """
        self.gossip_stones[stone_name] = location_id
    
    def get_gossip_stone_hint(self, stone_name: str) -> Optional[str]:
        """Get the hint text for a specific gossip stone."""
        location_id = self.gossip_stones.get(stone_name)
        if location_id is not None:
            return self.get_hint(location_id)
        return None
    
    def parse_server_hints(self, hint_data: List[Dict]) -> None:
        """
        Parse hint data from the Archipelago server.
        
        The server sends hints in LocationInfo packets:
        {
            "location": location_id,
            "item": item_id,
            "player": player_id,
            "found": bool,
        }
        
        We convert this to readable hint text.
        """
        # This will be populated with item/player name mappings from the context
        pass
    
    def format_hint(self, location_name: str, item_name: str, player_name: str, 
                   is_local: bool = False) -> str:
        """
        Format a hint into readable text.
        
        Args:
            location_name: Name of the location
            item_name: Name of the item
            player_name: Name of the player who gets the item
            is_local: Whether this is a local player's item
            
        Returns:
            Formatted hint string
        """
        if is_local:
            return f"{location_name} contains {item_name}"
        else:
            return f"{location_name} contains {player_name}'s {item_name}"


# Gossip Stone locations in SSHD
# These are the in-game gossip stones where hints could be written
GOSSIP_STONE_LOCATIONS = {
    # Skyloft
    "Skyloft - Waterfall Cave": {"scene": "Skyloft", "id": 0},
    "Skyloft - Near Bazaar": {"scene": "Skyloft", "id": 1},
    
    # Sealed Grounds
    "Sealed Grounds - Near Temple": {"scene": "Sealed Grounds", "id": 0},
    "Sealed Grounds - Gorko": {"scene": "Sealed Grounds", "id": 1},
    
    # Faron Woods
    "Faron Woods - Great Tree": {"scene": "Faron Woods", "id": 0},
    "Faron Woods - Deep Woods": {"scene": "Faron Woods", "id": 1},
    
    # Eldin Volcano
    "Eldin Volcano - First Area": {"scene": "Eldin Volcano", "id": 0},
    "Eldin Volcano - Volcano Summit": {"scene": "Eldin Volcano", "id": 1},
    
    # Lanayru Desert
    "Lanayru Desert - Desert Entrance": {"scene": "Lanayru Desert", "id": 0},
    "Lanayru Desert - Temple of Time": {"scene": "Lanayru Desert", "id": 1},
}


def write_hint_to_gossip_stone(memory, stone_name: str, hint_text: str) -> bool:
    """
    Write a hint to an in-game gossip stone.
    
    ⚠️ WARNING: This requires knowing the correct memory addresses for gossip stone text.
    TODO: Research where gossip stone text is stored in SSHD memory.
    
    Args:
        memory: RyujinxMemoryReader instance
        stone_name: Name of the gossip stone
        hint_text: The hint text to write
        
    Returns:
        True if successful, False otherwise
    """
    if stone_name not in GOSSIP_STONE_LOCATIONS:
        return False
    
    # TODO: Find memory address for gossip stone text
    # Likely stored in a text table that can be modified
    # Need to research with Ryujinx debugger
    
    # Placeholder implementation
    stone_info = GOSSIP_STONE_LOCATIONS[stone_name]
    print(f"Would write hint to {stone_name}: {hint_text}")
    
    # Future implementation:
    # 1. Find text table address for gossip stones
    # 2. Calculate offset for this specific stone
    # 3. Write hint_text to that memory location
    # 4. Handle text encoding (likely UTF-16)
    
    return False  # Not yet implemented


def get_all_gossip_stone_names() -> List[str]:
    """Get list of all gossip stone names."""
    return list(GOSSIP_STONE_LOCATIONS.keys())

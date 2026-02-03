"""
Access rules for Skyward Sword HD Archipelago World.

Defines logical requirements for accessing locations and regions.
"""

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from .Locations import LOCATION_TABLE

if TYPE_CHECKING:
    from . import SSHDWorld


def set_rules(world: "SSHDWorld") -> None:
    """
    Set all access rules for the world.
    
    This is called during world generation to establish what items are
    needed to access each location.
    """
    multiworld = world.multiworld
    player = world.player
    options = world.options
    
    # Get regions
    menu = multiworld.get_region("Menu", player)
    
    # Helper functions for checking items
    def has(state: CollectionState, item: str) -> bool:
        """Check if player has an item."""
        return state.has(item, player)
    
    def has_all(state: CollectionState, *items: str) -> bool:
        """Check if player has all specified items."""
        return all(state.has(item, player) for item in items)
    
    def has_any(state: CollectionState, *items: str) -> bool:
        """Check if player has any of the specified items."""
        return any(state.has(item, player) for item in items)
    
    def count(state: CollectionState, item: str) -> int:
        """Count how many of an item the player has."""
        return state.count(item, player)
    
    # Progressive item helpers
    def has_sword(state: CollectionState, level: int = 1) -> bool:
        """Check if player has sword of at least the specified level."""
        return count(state, "Progressive Sword") >= level
    
    def has_slingshot(state: CollectionState) -> bool:
        """Check if player has any slingshot."""
        return count(state, "Progressive Slingshot") >= 1
    
    def has_beetle(state: CollectionState) -> bool:
        """Check if player has any beetle."""
        return count(state, "Progressive Beetle") >= 1
    
    def has_mitts(state: CollectionState) -> bool:
        """Check if player has digging mitts."""
        return count(state, "Progressive Mitts") >= 1
    
    def has_bow(state: CollectionState) -> bool:
        """Check if player has any bow."""
        return count(state, "Progressive Bow") >= 1
    
    def can_use_bombs(state: CollectionState) -> bool:
        """Check if player can use bombs."""
        return has(state, "Bomb Bag")
    
    def can_swim_underwater(state: CollectionState) -> bool:
        """Check if player can swim underwater."""
        return has(state, "Water Scale")
    
    def can_fly(state: CollectionState) -> bool:
        """Check if player can fly in the sky."""
        return has(state, "Sailcloth")
    
    # Apply entrance rules from Regions.py connections
    from .Regions import REGION_CONNECTIONS
    
    for source_name, connections in REGION_CONNECTIONS.items():
        try:
            source_region = multiworld.get_region(source_name, player)
        except KeyError:
            continue  # Region doesn't exist, skip
        
        for dest_name, rule_name in connections:
            try:
                dest_region = multiworld.get_region(dest_name, player)
            except KeyError:
                continue  # Destination doesn't exist, skip
            
            # Get the entrance
            entrance = source_region.get_entrance(f"{source_name} -> {dest_name}")
            if not entrance:
                continue
            
            # Apply access rules based on rule name
            if rule_name == "has_sword":
                entrance.access_rule = lambda state: has_sword(state, 1)
            elif rule_name == "can_fly":
                entrance.access_rule = lambda state: can_fly(state)
            elif rule_name == "can_enter_faron":
                entrance.access_rule = lambda state: can_fly(state)
            elif rule_name == "can_enter_eldin":
                entrance.access_rule = lambda state: can_fly(state)
            elif rule_name == "can_enter_lanayru":
                entrance.access_rule = lambda state: can_fly(state)
            elif rule_name == "can_progress_faron":
                entrance.access_rule = lambda state: has_sword(state, 1)
            elif rule_name == "can_enter_skyview":
                entrance.access_rule = lambda state: has_slingshot(state)
            elif rule_name == "has_skyview_boss_key":
                entrance.access_rule = lambda state: has(state, "Skyview Boss Key")
            elif rule_name == "can_reach_lake_floria":
                entrance.access_rule = lambda state: has(state, "Water Dragon's Scale")
            elif rule_name == "can_reach_flooded_faron":
                entrance.access_rule = lambda state: has(state, "Whip") and can_swim_underwater(state)
            elif rule_name == "can_enter_ancient_cistern":
                entrance.access_rule = lambda state: has(state, "Whip") and can_swim_underwater(state)
            elif rule_name == "can_enter_earth_temple":
                entrance.access_rule = lambda state: can_use_bombs(state) and has_beetle(state)
            elif rule_name == "has_earth_temple_boss_key":
                entrance.access_rule = lambda state: has(state, "Earth Temple Boss Key")
            elif rule_name == "can_enter_fire_sanctuary":
                entrance.access_rule = lambda state: has(state, "Fire Dragon's Key") and can_use_bombs(state)
            elif rule_name == "can_enter_temple_of_time":
                entrance.access_rule = lambda state: has(state, "Goddess's Harp")
            elif rule_name == "can_enter_lanayru_mining_facility":
                entrance.access_rule = lambda state: has(state, "Gust Bellows")
            elif rule_name == "can_reach_lanayru_gorge":
                entrance.access_rule = lambda state: has(state, "Clawshots")
            elif rule_name == "can_board_sandship":
                entrance.access_rule = lambda state: has(state, "Clawshots") and has_bow(state)
            elif rule_name == "can_reach_thunderhead":
                entrance.access_rule = lambda state: has(state, "Ballad of the Goddess") and has_sword(state, 4)
            elif rule_name == "can_reach_isle_of_songs":
                entrance.access_rule = lambda state: has(state, "Clawshots")
            elif rule_name == "can_enter_sky_keep":
                entrance.access_rule = lambda state: has(state, "Stone of Trials")
            elif rule_name == "can_reach_past":
                entrance.access_rule = lambda state: has(state, "Gate of Time Access")
            elif rule_name == "can_reach_present":
                entrance.access_rule = lambda state: has(state, "Gate of Time Access")
            # If rule_name is None or unknown, no access rule applied (always accessible)
    
    def has_slingshot(state: CollectionState) -> bool:
        """Check if player has any slingshot."""
        return count(state, "Progressive Slingshot") >= 1
    
    def has_beetle(state: CollectionState) -> bool:
        """Check if player has any beetle."""
        return count(state, "Progressive Beetle") >= 1
    
    def has_mitts(state: CollectionState) -> bool:
        """Check if player has digging mitts."""
        return count(state, "Progressive Mitts") >= 1
    
    def has_bow(state: CollectionState) -> bool:
        """Check if player has any bow."""
        return count(state, "Progressive Bow") >= 1
    
    def can_use_bombs(state: CollectionState) -> bool:
        """Check if player can use bombs."""
        return has(state, "Bomb Bag")
    
    def can_swim_underwater(state: CollectionState) -> bool:
        """Check if player can swim underwater."""
        return has(state, "Water Scale")
    
    def can_fly(state: CollectionState) -> bool:
        """Check if player can fly in the sky."""
        return has(state, "Sailcloth")
    
    def can_cut_grass(state: CollectionState) -> bool:
        """Check if player can cut grass/vines."""
        return has_sword(state, 1)  # Any sword works
    
    def can_dousing(state: CollectionState) -> bool:
        """Check if player can use dowsing."""
        return has_sword(state, 1)  # Goddess Sword enables dowsing
    
    def can_use_goddess_walls(state: CollectionState) -> bool:
        """Check if player can use goddess walls."""
        return has_sword(state, 1)  # Goddess Sword enables walls
    
    def can_open_goddess_chests(state: CollectionState) -> bool:
        """Check if player can open goddess chests."""
        return has_sword(state, 1) and can_dousing(state)
    
    # Wallet capacity helpers
    def wallet_capacity(state: CollectionState) -> int:
        """Get current wallet capacity."""
        wallet_count = count(state, "Progressive Wallet")
        extra_wallets = count(state, "Extra Wallet")
        
        # Progressive wallet: 300 -> 500 -> 1000 -> 5000 -> 9000
        capacities = [300, 500, 1000, 5000, 9000]
        capacity = capacities[min(wallet_count, len(capacities) - 1)]
        
        # Each extra wallet adds +300
        capacity += extra_wallets * 300
        
        return capacity
    
    def can_afford(state: CollectionState, cost: int) -> bool:
        """Check if player can afford something."""
        return wallet_capacity(state) >= cost
    
    # Region access helpers for major areas
    def can_access_faron(state: CollectionState) -> bool:
        """Check if player can access Faron Woods region."""
        return can_fly(state)  # Need sailcloth to reach surface
    
    def can_access_eldin(state: CollectionState) -> bool:
        """Check if player can access Eldin Volcano region."""
        return can_fly(state)  # Need sailcloth to reach surface
    
    def can_access_lanayru(state: CollectionState) -> bool:
        """Check if player can access Lanayru Desert region."""
        return can_fly(state)  # Need sailcloth to reach surface
    
    # Dungeon access requirements
    def can_access_skyview(state: CollectionState) -> bool:
        """Check if player can access Skyview Temple."""
        return can_access_faron(state) and has_slingshot(state)
    
    def can_access_earth_temple(state: CollectionState) -> bool:
        """Check if player can access Earth Temple."""
        return can_access_eldin(state) and can_use_bombs(state) and has_beetle(state)
    
    def can_access_lanayru_mining_facility(state: CollectionState) -> bool:
        """Check if player can access Lanayru Mining Facility."""
        return can_access_lanayru(state) and has(state, "Gust Bellows")
    
    def can_access_ancient_cistern(state: CollectionState) -> bool:
        """Check if player can access Ancient Cistern."""
        return can_access_faron(state) and has(state, "Whip") and can_swim_underwater(state)
    
    def can_access_sandship(state: CollectionState) -> bool:
        """Check if player can access Sandship."""
        return can_access_lanayru(state) and has(state, "Clawshots") and has_bow(state)
    
    def can_access_fire_sanctuary(state: CollectionState) -> bool:
        """Check if player can access Fire Sanctuary."""
        return can_access_eldin(state) and has_mitts(state) and has(state, "Water Basin")
    
    # Set location access rules
    # These are BASIC rules - full logic would be much more complex
    for location in multiworld.get_locations(player):
        location_name = location.name
        location_types = LOCATION_TABLE.get(location_name)
        
        if not location_types:
            continue
        
        types = location_types.types if hasattr(location_types, 'types') else []
        
        # Dungeon-specific rules
        if "Skyview Temple" in location_name:
            location.access_rule = lambda state: has_slingshot(state)
        
        elif "Earth Temple" in location_name:
            location.access_rule = lambda state: has_all(state, "Bomb Bag", "Progressive Beetle")
        
        elif "Lanayru Mining Facility" in location_name:
            location.access_rule = lambda state: has_all(state, "Gust Bellows")
        
        elif "Ancient Cistern" in location_name:
            location.access_rule = lambda state: has_all(state, "Whip", "Water Scale")
        
        elif "Sandship" in location_name:
            location.access_rule = lambda state: has_all(state, "Bow", "Clawshots")
        
        elif "Fire Sanctuary" in location_name:
            location.access_rule = lambda state: has_all(state, "Mogma Mitts", "Water Basin")
        
        elif "Sky Keep" in location_name:
            # Sky Keep requires beating all dungeons
            location.access_rule = lambda state: has_all(
                state,
                "Skyview Temple Boss Key",
                "Earth Temple Boss Key", 
                "Lanayru Mining Facility Boss Key",
                "Ancient Cistern Boss Key",
                "Sandship Boss Key",
                "Fire Sanctuary Boss Key"
            )
        
        # Boss fights require boss keys
        if "Defeat Boss" in location_name or "Boss Key" in location_name:
            if "Skyview" in location_name:
                location.access_rule = lambda state: has(state, "Skyview Temple Boss Key")
            elif "Earth Temple" in location_name:
                location.access_rule = lambda state: has(state, "Earth Temple Boss Key")
            elif "Lanayru Mining Facility" in location_name:
                location.access_rule = lambda state: has(state, "Lanayru Mining Facility Boss Key")
            elif "Ancient Cistern" in location_name:
                location.access_rule = lambda state: has(state, "Ancient Cistern Boss Key")
            elif "Sandship" in location_name:
                location.access_rule = lambda state: has(state, "Sandship Boss Key")
            elif "Fire Sanctuary" in location_name:
                location.access_rule = lambda state: has(state, "Fire Sanctuary Boss Key")
        
        # Goddess Cube checks require various items
        if "Goddess Cube" in location_name or "Goddess Chest" in location_name:
            if "Clawshot" in location_name:
                location.access_rule = lambda state: has(state, "Clawshots")
            elif "Beetle" in location_name:
                location.access_rule = lambda state: has_beetle(state)
        
        # Silent Realm checks require completing trials
        if "Silent Realm" in location_name:
            if "Farore" in location_name:
                location.access_rule = lambda state: has(state, "Farore's Courage")
            elif "Nayru" in location_name:
                location.access_rule = lambda state: has(state, "Nayru's Wisdom")
            elif "Din" in location_name:
                location.access_rule = lambda state: has(state, "Din's Power")
            elif "Goddess" in location_name:
                location.access_rule = lambda state: has(state, "Song of the Hero")
    
    # Set goal/victory condition
    # Victory requires collecting Game Beatable event (defeating Demise) AND meeting completion requirements
    multiworld.completion_condition[player] = lambda state: has(state, "Game Beatable") and _can_complete_game(state, world)
    # TODO: Implement dungeon-specific logic
    # TODO: Implement trick-based logic if options enable it
    
    # Set completion condition
    multiworld.completion_condition[player] = lambda state: _can_complete_game(state, world)


def _can_complete_game(state: CollectionState, world: "SSHDWorld") -> bool:
    """
    Check if the player can complete the game.
    
    Requirements depend on options:
    - Required number of dungeons beaten
    - Triforce pieces collected (if required)
    - Gate of Time opened (sword + dungeons)
    - Final boss accessible
    """
    player = world.player
    options = world.options
    
    # Check required dungeon count
    required_dungeons = options.required_dungeon_count.value
    dungeons_beaten = 0
    
    # Count dungeons that can be beaten
    dungeon_items = [
        "Skyview Boss Key",
        "Earth Temple Boss Key", 
        "Lanayru Mining Facility Boss Key",
        "Ancient Cistern Boss Key",
        "Sandship Boss Key",
        "Fire Sanctuary Boss Key"
    ]
    
    for dungeon_key in dungeon_items:
        if state.has(dungeon_key, player):
            dungeons_beaten += 1
    
    if dungeons_beaten < required_dungeons:
        return False
    
    # Check if Triforce is required
    if options.triforce_required.value:
        triforce_pieces = [
            "Triforce of Courage",
            "Triforce of Power",
            "Triforce of Wisdom"
        ]
        if not all(state.has(piece, player) for piece in triforce_pieces):
            return False
    
    # Check Gate of Time sword requirement
    gate_sword_level = options.gate_of_time_sword_requirement.value
    sword_count_needed = gate_sword_level + 1  # Goddess Sword = 1, True Master = 5
    
    if state.count("Progressive Sword", player) < sword_count_needed:
        return False
    
    # Check Gate of Time dungeon requirements
    if options.gate_of_time_dungeon_requirements.value == 0:  # Required
        if dungeons_beaten < required_dungeons:
            return False
    
    # All conditions met
    return True


def _has_sword_level(state: CollectionState, player: int, level: int) -> bool:
    """
    Check if player has at least the specified sword level.
    
    Levels:
    0 = Practice Sword
    1 = Goddess Sword
    2 = Goddess Longsword
    3 = Goddess White Sword
    4 = Master Sword
    5 = True Master Sword
    """
    return state.count("Progressive Sword", player) >= level


def _can_access_surface(state: CollectionState, player: int) -> bool:
    """Check if player can access the Surface from Skyloft."""
    # Need Sailcloth to safely reach the surface
    return state.has("Sailcloth", player)


def _can_open_gate_of_time(state: CollectionState, world: "SSHDWorld") -> bool:
    """Check if player can open the Gate of Time."""
    player = world.player
    options = world.options
    
    # Check sword requirement
    sword_level = options.gate_of_time_sword_requirement.value
    if not _has_sword_level(state, player, sword_level + 1):
        return False
    
    # Check dungeon requirement (if enabled)
    if options.gate_of_time_dungeon_requirements.value == 0:  # Required
        required_count = options.required_dungeon_count.value
        # Would need to check dungeon completion here
        # For now, simplified
        pass
    
    return True


# Additional helper functions for specific checks
# These will be expanded as the logic is implemented

def _can_use_gust_bellows(state: CollectionState, player: int) -> bool:
    """Check if player has Gust Bellows."""
    return state.has("Gust Bellows", player)


def _can_use_clawshots(state: CollectionState, player: int) -> bool:
    """Check if player has Clawshots."""
    return state.has("Clawshots", player)


def _can_use_bow(state: CollectionState, player: int) -> bool:
    """Check if player has any Bow."""
    return state.has("Progressive Bow", player)


def _can_use_whip(state: CollectionState, player: int) -> bool:
    """Check if player has Whip."""
    return state.has("Whip", player)


def _can_use_bombs(state: CollectionState, player: int) -> bool:
    """Check if player has Bomb Bag."""
    return state.has("Bomb Bag", player)

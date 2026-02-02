"""
Options for Skyward Sword HD Archipelago World.
"""

from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    DefaultOnToggle,
    FreeText,
    ItemDict,
    PerGameCommonOptions,
    Range,
    Toggle,
)


# === Core Logic Settings ===

class LogicRules(Choice):
    """
    Determines what logic the randomizer uses.
    All Locations Reachable: The randomizer ensures that all locations can be reached. If a location's item is required to beat the game, that item is placed where it can be obtained.
    Beatable Only: The randomizer only ensures the game is beatable. Some locations may be unreachable, and items required to reach those locations will not be placed at them.
    """
    display_name = "Logic Rules"
    option_all_locations_reachable = 0
    option_beatable_only = 1
    default = 0


class ItemPool(Choice):
    """
    Determines the size of the item pool.
    Minimal: Only essential items are included.
    Standard: Normal item pool with standard items.
    Extra: Extra items added for more variety.
    Plentiful: Maximum items for a more relaxed experience.
    """
    display_name = "Item Pool"
    option_minimal = 0
    option_standard = 1
    option_extra = 2
    option_plentiful = 3
    default = 1


# === Completion Requirements ===

class RequiredDungeonCount(Range):
    """
    Determines the number of dungeons required to beat the seed.
    Beating Sky Keep is NOT required.
    Lanayru Mining Facility is beaten when exiting to the Temple of Time.
    Other dungeons are beaten when the Goddess Crest is struck with a Skyward Strike.
    """
    display_name = "Required Dungeon Count"
    range_start = 0
    range_end = 6
    default = 2


class TriforceRequired(DefaultOnToggle):
    """
    If enabled, the three Triforces will be required to open the door to Hylia's Realm at the end.
    """
    display_name = "Triforce Required"


class TriforceShuffle(Choice):
    """
    Choose where Triforces will appear in the game.
    Vanilla: Triforces are placed in their vanilla locations in Sky Keep.
    Sky Keep: Triforces are shuffled only within Sky Keep.
    Anywhere: Triforces are shuffled with all other valid locations in the game.
    """
    display_name = "Triforce Shuffle"
    option_vanilla = 0
    option_sky_keep = 1
    option_anywhere = 2
    default = 2


class GateOfTimeSwordRequirement(Choice):
    """
    Determines the sword needed to open the Gate of Time.
    """
    display_name = "Gate of Time Sword Requirement"
    option_goddess_sword = 0
    option_goddess_longsword = 1
    option_goddess_white_sword = 2
    option_master_sword = 3
    option_true_master_sword = 4
    default = 4


class GateOfTimeDungeonRequirements(Choice):
    """
    Enables dungeon requirements for opening the Gate of Time.
    Required: beating the required dungeons is necessary to open the Gate of Time.
    Unrequired: the Gate of Time can be opened without beating the required dungeons.
    """
    display_name = "Gate of Time Dungeon Requirements"
    option_required = 0
    option_unrequired = 1
    default = 0


class Imp2Skip(DefaultOnToggle):
    """
    If enabled, the requirement to defeat Imprisoned 2 at the end is skipped.
    """
    display_name = "Imp 2 Skip"


class SkipHorde(Toggle):
    """
    If enabled, the requirement to defeat The Horde at the end is skipped.
    """
    display_name = "Skip Horde"


class SkipGhirahim3(Toggle):
    """
    If enabled, the requirement to defeat Ghirahim 3 at the end is skipped.
    """
    display_name = "Skip Ghirahim 3"


# === Randomization Settings ===

class GratitudeCrystalShuffle(Toggle):
    """Shuffle gratitude crystals into the item pool."""
    display_name = "Gratitude Crystal Shuffle"

class StaminaFruitShuffle(Toggle):
    """Shuffle stamina fruits into the item pool."""
    display_name = "Stamina Fruit Shuffle"

class NpcClosetShuffle(Toggle):
    """Shuffle NPC closets."""
    display_name = "NPC Closet Shuffle"

class HiddenItemShuffle(Toggle):
    """Shuffle hidden items."""
    display_name = "Hidden Item Shuffle"

class RupeeShuffle(Choice):
    """Shuffle rupees with varying difficulty."""
    display_name = "Rupee Shuffle"
    option_vanilla = 0
    option_beginner = 1
    option_intermediate = 2
    option_advanced = 3
    default = 0

class GoddessChestShuffle(Toggle):
    """Shuffle goddess chests."""
    display_name = "Goddess Chest Shuffle"

class TrialTreasureShuffle(Range):
    """Number of trial treasures to shuffle (0-10)."""
    display_name = "Trial Treasure Shuffle"
    range_start = 0
    range_end = 10
    default = 0

class TadtoneShuffle(Toggle):
    """Shuffle tadtones."""
    display_name = "Tadtone Shuffle"

class GossipStoneTreasureShuffle(Toggle):
    """Shuffle gossip stone treasures."""
    display_name = "Gossip Stone Treasure Shuffle"

class SmallKeyShuffle(Choice):
    """Where small keys can appear."""
    display_name = "Small Key Shuffle"
    option_own_dungeon = 0
    option_any_dungeon = 1
    option_anywhere = 2
    option_keysy = 3
    default = 0

class BossKeyShuffle(Choice):
    """Where boss keys can appear."""
    display_name = "Boss Key Shuffle"
    option_own_dungeon = 0
    option_any_dungeon = 1
    option_anywhere = 2
    option_keysy = 3
    default = 0

class MapShuffle(Choice):
    """Where dungeon maps can appear."""
    display_name = "Map Shuffle"
    option_vanilla = 0
    option_own_dungeon_restricted = 1
    option_anywhere = 2
    default = 0

class RandomizeEntrances(Toggle):
    """
    Randomize dungeon entrances and major area connections.
    """
    display_name = "Randomize Entrances"


class RandomizeDungeons(Toggle):
    """
    Randomize dungeon entrances only.
    """
    display_name = "Randomize Dungeons"


class RandomizeTrials(Toggle):
    """
    Randomize Silent Realm trial entrances.
    """
    display_name = "Randomize Trials"


# === Starting Inventory ===

class StartingTablets(Range):
    """
    Number of tablets (Ruby, Amber, Emerald) to start with.
    """
    display_name = "Starting Tablets"
    range_start = 0
    range_end = 3
    default = 0


class StartingSword(Choice):
    """
    Which sword to start with.
    """
    display_name = "Starting Sword"
    option_none = 0
    option_practice_sword = 1
    option_goddess_sword = 2
    option_goddess_longsword = 3
    option_goddess_white_sword = 4
    option_master_sword = 5
    option_true_master_sword = 6
    default = 1


class StartWithSailcloth(DefaultOnToggle):
    """
    Start with the Sailcloth.
    """
    display_name = "Start With Sailcloth"


class CustomStartingItems(ItemDict):
    """
    Add custom items to starting inventory as a YAML dictionary.
    Format: {"Item Name": count, "Another Item": count}
    Leave empty {} for no custom items.
    See Available_Starting_Items.yaml for all available items.
    """
    display_name = "Custom Starting Items"
    default = {}


# === Quality of Life ===

class OpenLakeFloriaGate(DefaultOnToggle):
    """
    If enabled, the gate to Lake Floria is open from the start.
    """
    display_name = "Open Lake Floria Gate"


class OpenThunderhead(DefaultOnToggle):
    """
    If enabled, the Thunderhead is open from the start.
    """
    display_name = "Open Thunderhead"


class FastBirdStatues(DefaultOnToggle):
    """
    If enabled, bird statues activate immediately without the animation.
    """
    display_name = "Fast Bird Statues"


class SkipIntro(DefaultOnToggle):
    """
    If enabled, skip the intro sequence and start at Link's room.
    """
    display_name = "Skip Intro"


class SkipSkykeepDoorCutscene(DefaultOnToggle):
    """
    If enabled, skip the Sky Keep door opening cutscene.
    """
    display_name = "Skip Sky Keep Door Cutscene"


class SkipHarpPlaying(Toggle):
    """Skip harp playing mini-games."""
    display_name = "Skip Harp Playing"


class SkipMiscCutscenes(Toggle):
    """Skip miscellaneous small cutscenes."""
    display_name = "Skip Misc Cutscenes"


# === Difficulty Settings ===

class NoSpoilerLog(Toggle):
    """
    If enabled, no spoiler log will be generated.
    """
    display_name = "No Spoiler Log"


class EmptyUnreachableLocations(Toggle):
    """
    If enabled, locations that are unreachable will contain junk items.
    """
    display_name = "Empty Unreachable Locations"


class DamageMultiplier(Choice):
    """
    Multiplier for damage taken.
    """
    display_name = "Damage Multiplier"
    option_half = 0
    option_normal = 1
    option_double = 2
    option_quadruple = 3
    option_ohko = 4
    default = 1


# === Item Pool Settings ===

class AddJunkItems(Toggle):
    """
    If enabled, add extra junk items to the item pool (rupees, treasures, etc.).
    """
    display_name = "Add Junk Items"


class JunkItemRate(Range):
    """
    Percentage of junk items to add to the pool (if Add Junk Items is enabled).
    """
    display_name = "Junk Item Rate"
    range_start = 0
    range_end = 100
    default = 50


class ProgressiveItems(DefaultOnToggle):
    """
    If enabled, items with multiple tiers (Sword, Beetle, Bow, etc.) will be progressive.
    """
    display_name = "Progressive Items"


class MusicRandomization(Choice):
    """
    Randomize background music throughout the game.
    
    - Vanilla: No music shuffling
    - Shuffled: Background music randomly shuffled
    - Shuffled (Limit Vanilla): Minimize unchanged tracks
    """
    display_name = "Music Randomization"
    option_vanilla = 0
    option_shuffled = 1
    option_shuffled_limit_vanilla = 2
    default = 0


class CutoffGameOverMusic(Toggle):
    """
    If music randomization places a very long song as the game over music,
    this will cut it off after a reasonable duration instead of playing the entire song.
    """
    display_name = "Cutoff Game Over Music"


class ExtractPath(FreeText):
    """
    Path to the extracted SSHD romfs folder.
    If not specified, defaults to C:\\ProgramData\\Archipelago\\sshd_extract\\
    This folder must contain the extracted romfs files from your SSHD ROM.
    """
    display_name = "Extract Path"
    default = "C:\\\\ProgramData\\\\Archipelago\\\\sshd_extract\\\\"


class SshdrSeed(FreeText):
    """
    The seed to use for randomization. If not specified, a random seed will be generated.
    Use word-based seeds like 'AirStrongholdPlantSkipper' or leave blank for random.
    """
    display_name = "SSHD-Rando Seed"
    default = ""


class SettingString(FreeText):
    """
    The sshd-rando Setting String for this seed. This is an advanced option - leave blank to auto-generate.
    This string uniquely identifies all randomization settings and can be used to recreate an exact seed.
    """
    display_name = "Setting String"
    default = ""


# === Archipelago-specific ===

class SSHDDeathLink(DeathLink):
    """
    When you die, everyone dies. Of course the reverse is true too.
    """


@dataclass
class SSHDOptions(PerGameCommonOptions):
    """
    All options for Skyward Sword HD.
    """
    # Core Logic
    logic_rules: LogicRules
    item_pool: ItemPool
    
    # Completion
    required_dungeon_count: RequiredDungeonCount
    triforce_required: TriforceRequired
    triforce_shuffle: TriforceShuffle
    gate_of_time_sword_requirement: GateOfTimeSwordRequirement
    gate_of_time_dungeon_requirements: GateOfTimeDungeonRequirements
    imp2_skip: Imp2Skip
    skip_horde: SkipHorde
    skip_ghirahim3: SkipGhirahim3
    
    # Randomization
    gratitude_crystal_shuffle: GratitudeCrystalShuffle
    stamina_fruit_shuffle: StaminaFruitShuffle
    npc_closet_shuffle: NpcClosetShuffle
    hidden_item_shuffle: HiddenItemShuffle
    rupee_shuffle: RupeeShuffle
    goddess_chest_shuffle: GoddessChestShuffle
    trial_treasure_shuffle: TrialTreasureShuffle
    tadtone_shuffle: TadtoneShuffle
    gossip_stone_treasure_shuffle: GossipStoneTreasureShuffle
    small_key_shuffle: SmallKeyShuffle
    boss_key_shuffle: BossKeyShuffle
    map_shuffle: MapShuffle
    randomize_entrances: RandomizeEntrances
    randomize_dungeons: RandomizeDungeons
    randomize_trials: RandomizeTrials
    music_randomization: MusicRandomization
    cutoff_game_over_music: CutoffGameOverMusic
    
    # Starting Inventory
    starting_tablets: StartingTablets
    starting_sword: StartingSword
    start_with_sailcloth: StartWithSailcloth
    custom_starting_items: CustomStartingItems
    
    # Quality of Life
    open_lake_floria_gate: OpenLakeFloriaGate
    open_thunderhead: OpenThunderhead
    fast_bird_statues: FastBirdStatues
    skip_intro: SkipIntro
    skip_skykeep_door_cutscene: SkipSkykeepDoorCutscene
    skip_harp_playing: SkipHarpPlaying
    skip_misc_cutscenes: SkipMiscCutscenes
    
    # Difficulty
    no_spoiler_log: NoSpoilerLog
    empty_unreachable_locations: EmptyUnreachableLocations
    damage_multiplier: DamageMultiplier
    
    # Item Pool
    add_junk_items: AddJunkItems
    junk_item_rate: JunkItemRate
    progressive_items: ProgressiveItems
    
    # Configuration
    extract_path: ExtractPath
    sshdr_seed: SshdrSeed
    setting_string: SettingString
    
    # Archipelago
    death_link: SSHDDeathLink

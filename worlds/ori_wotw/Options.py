"""Options for Ori and the Will of the Wisps Randomizer."""

from Options import Choice, Toggle, DefaultOnToggle, PerGameCommonOptions, OptionGroup, OptionSet
from dataclasses import dataclass


class LogicDifficulty(Choice):
    """
    Difficulty of the logic.

    - **Moki** (or easy): Recommended for beginners, who only played the game casually.
    - **Gorlek** (or medium): Harder paths that can use sword and hammer as movement options, and damage boosts.
    - **Kii** (or hard): Hard and precise paths that use energy weapons as movement.
    - **Unsafe**: Very hard and unverified paths. Warning: some paths are **extremely hard**.
    """
    display_name = "Logic difficulty"
    rich_text_doc = True
    default = 0
    option_moki = 0
    option_gorlek = 1
    option_kii = 2
    option_unsafe = 3
    alias_easy = 0
    alias_medium = 1
    alias_hard = 2


class Glitches(Toggle):
    """
    Whether the logic includes paths with glitches.

    - **Gorlek**: includes grounded sentry jumps, sentry as a fire source, breaking walls with Shuriken, and removing the kill plane in Feeding Grounds.
    - **Kii**: glitches are not included in Kii logic yet.
    - **Unsafe**: everything else.
    """
    display_name = "Glitches"
    rich_text_doc = True


class StartingLocation(Choice):
    """Choose the starting location."""
    display_name = "Starting location"
    option_marsh = 0
    option_burrows = 1
    option_howlsden = 2
    option_hollow = 3
    option_glades = 4
    option_wellspring = 5
    option_westwoods = 6
    option_eastwoods = 7
    option_reach = 8
    option_depths = 9
    option_eastpools = 10
    option_westpools = 11
    option_westwastes = 12
    option_eastwastes = 13
    option_outerruins = 14
    option_innerruins = 15
    option_willow = 16
    default = 0


class Goal(OptionSet):
    """Set conditions for entering the final boss. Use the rando wheel (with **V**) to check goal progress.

    - **Trees**: All trees must be collected.
    - **Wisps**: All wisps must be collected.
    - **Quests**: All quests have to be finished.
    """
    display_name = "Goal"
    rich_text_doc = True
    valid_keys_casefold = True
    valid_keys = ["trees", "wisps", "quests"]
    default = frozenset(["trees"])


class HardMode(Toggle):
    """Play the game in hard difficulty."""
    display_name = "Hard mode"


class QualityOfLife(DefaultOnToggle):
    """Activate QOL features and gameplay improvements."""
    display_name = "Quality of life"


class ShrineTrialHints(DefaultOnToggle):
    """Displays the reward for shrines and trials when activating them."""
    display_name = "Shrines and trials hints"


class Teleporters(DefaultOnToggle):
    """Add most teleporters to the item pool."""
    display_name = "Teleporters"


class ExtraTeleporters(Toggle):
    """Add Ruins, West Pools and Shriek teleporters to the pool."""
    display_name = "Extra teleporters"


class BonusItems(DefaultOnToggle):
    """Add to the pool items specific to the randomizer."""
    display_name = "Bonus items"


class ExtraBonusItems(Toggle):
    """Add to the pool powerful items specific to the randomizer."""
    display_name = "Extra bonus items"


class SkillUpgrades(Toggle):
    """Add to the pool upgrades to skills specific to the randomizer."""
    display_name = "Skill upgrades"


class BetterSpawn(Toggle):
    """Opens some doors so random spawn works better."""
    display_name = "Better random spawn"


class BetterWellspring(Toggle):
    """The top door of Wellspring Glades is opened by default."""
    display_name = "Better Wellspring"


class NoRain(Toggle):
    """ Remove the rain in Marsh, and remove Howl."""
    display_name = "No Rain"


class NoCombat(OptionSet):
    """Skip all combat heavy parts.

    - Everything: the same as if you include all the following
    - Shrines: Shrine have their pickup floating above them before the fight
    - Arenas: the arenas start as completed
    - Demi Bosses: Demi Bosses like Howl, Beetle and Rock boss start as defeated
    - Bosses: Bosses like Kwolok, Mora and Shriek's combat phases are skipped
    """
    display_name = "No Combat"
    rich_text_doc = True
    valid_keys = ["Everything", "Shrines", "Arenas", "Demi Bosses", "Bosses"]
    default = frozenset()


class NoTrials(Toggle):
    """Trials only contain filler items."""
    display_name = "No Trials"


class NoWillowHearts(Toggle):
    """The door to Shriek is open from the beginning."""
    display_name = "No Willow hearts"


class NoQuests(Toggle):
    """Talking to NPCs gives no item, and locations locked behind them are accessible."""
    display_name = "No Quests"


class NoKeystonesDoors(Toggle):
    """Open keystone doors by default (and remove keystones from the pool)."""
    display_name = "No Keystone doors"


class OpenMode(Toggle):
    """Open most of the doors and obstacles."""
    display_name = "Open mode"


class GladesDone(Toggle):
    """Start with Glades rebuilt and regrown."""
    display_name = "Glades Done"

class ShopKeywordsIcons(Toggle):
    """Have the non local items attempt to use a keyword system to choose icons
    for example, item with 'map' in their name will have a map icon
    if no keyword fit then the icon fall back to Classification
    """
    display_name = "Shop Keywords Icons"

class SpawnSword(DefaultOnToggle):
    """Choose to have Sword at the beginning."""
    display_name = "Spawn with Sword"


class VanillaShopUpgrades(Toggle):
    """Weapon upgrades and shards in shops are not randomized."""
    display_name = "Vanilla shop upgrades"


option_groups = [
    OptionGroup("Seed Settings", [
        LogicDifficulty,
        Glitches,
        StartingLocation,
        Goal,
        HardMode,
        QualityOfLife,
        ShrineTrialHints
    ]),
    OptionGroup("Item Pool", [
        Teleporters,
        ExtraTeleporters,
        BonusItems,
        ExtraBonusItems,
        SkillUpgrades
    ]),
    OptionGroup("World Changes", [
        BetterSpawn,
        BetterWellspring,
        NoRain,
        NoCombat,
        NoTrials,
        NoWillowHearts,
        NoQuests,
        NoKeystonesDoors,
        OpenMode,
        GladesDone,
        ShopKeywordsIcons
    ]),
    OptionGroup("Item Placements", [
        SpawnSword,
        VanillaShopUpgrades
    ])
]


@dataclass
class WotWOptions(PerGameCommonOptions):
    difficulty: LogicDifficulty  # Seed Settings
    glitches: Glitches
    spawn: StartingLocation
    goal: Goal
    hard_mode: HardMode
    qol: QualityOfLife
    hints: ShrineTrialHints
    tp: Teleporters  # Item Pool
    extratp: ExtraTeleporters
    bonus: BonusItems
    extra_bonus: ExtraBonusItems
    skill_upgrade: SkillUpgrades
    better_spawn: BetterSpawn  # World Changes
    better_wellspring: BetterWellspring
    no_rain: NoRain
    no_combat: NoCombat
    no_trials: NoTrials
    no_hearts: NoWillowHearts
    no_quests: NoQuests
    no_ks: NoKeystonesDoors
    open_mode: OpenMode
    glades_done: GladesDone
    shop_keywords: ShopKeywordsIcons
    sword: SpawnSword  # Item Placements
    vanilla_shop_upgrades: VanillaShopUpgrades

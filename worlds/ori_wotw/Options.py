"""Options for Ori and the Will of the Wisps Randomizer."""

from Options import Choice, Toggle, DefaultOnToggle, PerGameCommonOptions
from dataclasses import dataclass


class LogicDifficulty(Choice):
    """Difficulty of the logic."""
    display_name = "Logic difficulty"
    default = 0
    option_moki = 0
    option_gorlek = 1
    option_kii = 2
    option_unsafe = 3
    alias_easy = 0
    alias_medium = 1
    alias_hard = 2


class Glitches(Toggle):
    """Whether the logic includes paths using glitches."""
    display_name = "Glitches"


class HardMode(Toggle):
    """Play the game in hard difficulty."""
    display_name = "Hard mode"


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


class SpawnSword(DefaultOnToggle):
    """Choose to have Sword at the beginning."""
    display_name = "Spawn with Sword"


class Teleporters(DefaultOnToggle):
    """Add most teleporters to the item pool."""
    display_name = "Teleporters"


class ExtraTeleporters(Toggle):
    """Add two extra teleporters."""
    display_name = "Extra teleporters"


class Goal(Choice):
    """Set a condition for entering the final boss."""
    display_name = "Goal"
    option_trees = 0
    option_wisps = 1
    option_quests = 2
    default = 0


class BonusItems(DefaultOnToggle):
    """Add to the pool items specific to the randomizer."""
    display_name = "Bonus items"


class ExtraBonusItems(Toggle):
    """Add to the pool powerful items specific to the randomizer."""
    display_name = "Extra bonus items"


class SkillUpgrades(Toggle):
    """Add to the pool upgrades to skills specific to the randomizer."""
    display_name = "Skill upgrades"


class SkipCombat(Toggle):  # TODO: implement
    """Skip most of the combats."""
    display_name = "Skip combat"


class VanillaShopUpgrades(Toggle):
    """Weapon upgrades and shards in shops are not randomized."""
    display_name = "Vanilla shop upgrades"


class SkipTrials(Toggle):  # TODO
    """Trials are already completed."""
    display_name = "Skip Trials"


class BetterWellspring(Toggle):  # TODO
    """The top door of Wellspring Glades is opened by default."""
    display_name = "Better Wellspring"


@dataclass
class WotWOptions(PerGameCommonOptions):
    difficulty: LogicDifficulty
    glitches: Glitches
    hard_mode: HardMode
    spawn: StartingLocation
    sword: SpawnSword
    tp: Teleporters
    extratp: ExtraTeleporters
    goal: Goal
    bonus: BonusItems
    extra_bonus: ExtraBonusItems
    skill_upgrade: SkillUpgrades
    skip_combat: SkipCombat
    vanilla_shop_upgrades: VanillaShopUpgrades
    skip_trials: SkipTrials
    better_wellspring: BetterWellspring
# TODO open world, hearts, keystones, QOL

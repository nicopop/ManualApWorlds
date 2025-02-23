"""Additional location rules that are not extracted from `areas.wotw`."""

from worlds.generic.Rules import set_rule
from .Options import WotWOptions


def combat_rules(world, player: int, options: WotWOptions):
    """Defines rules for combat and light."""
    menu = world.get_region("Menu", player)
    diff = options.difficulty

    if diff == 0:  # Moki
        menu.connect(world.get_region("DepthsLight", player),
                     rule=lambda state: state.has_any(("UpperDepths.ForestsEyes", "Flash"), player))
        menu.connect(world.get_region("Combat.Ranged", player),
                     rule=lambda state: state.has_any(("Bow", "Spear"), player))
        menu.connect(world.get_region("Combat.Aerial", player),
                     rule=lambda s: s.has_any(("Double Jump", "Launch"), player))
        menu.connect(world.get_region("Combat.Dangerous", player),
                     rule=lambda s: s.has_any(("Double Jump", "Dash", "Bash", "Launch"), player))
        menu.connect(world.get_region("Combat.Shielded", player),
                     rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        menu.connect(world.get_region("Combat.Bat", player), rule=lambda s: s.has("Bash", player))
        menu.connect(world.get_region("Combat.Sand", player), rule=lambda s: s.has("Burrow", player))
        menu.connect(world.get_region("BreakCrystal", player),
                     rule=lambda s: s.has_any(("Sword", "Hammer", "Bow"), player))

    elif diff == 1:  # Gorlek
        menu.connect(world.get_region("DepthsLight", player),
                     rule=lambda state: state.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        menu.connect(world.get_region("Combat.Ranged", player),
                     rule=lambda state: state.has_any(("Grenade", "Bow", "Shuriken", "Sentry", "Spear"), player))
        menu.connect(world.get_region("Combat.Aerial", player),
                     rule=lambda s: s.has_any(("Double Jump", "Launch", "Bash"), player))
        menu.connect(world.get_region("Combat.Dangerous", player),
                     rule=lambda s: s.has_any(("Double Jump", "Dash", "Bash", "Launch"), player))
        menu.connect(world.get_region("Combat.Shielded", player),
                     rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        menu.connect(world.get_region("Combat.Bat", player), rule=lambda s: s.has("Bash", player))
        menu.connect(world.get_region("Combat.Sand", player), rule=lambda s: s.has("Burrow", player))
        menu.connect(world.get_region("BreakCrystal", player),
                     rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade"), player))

    elif diff == 2:  # Kii
        menu.connect(world.get_region("DepthsLight", player),
                     rule=lambda state: state.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        menu.connect(world.get_region("Combat.Ranged", player),
                     rule=lambda state: state.has_any(("Grenade", "Bow", "Shuriken", "Sentry", "Spear"), player))
        menu.connect(world.get_region("Combat.Aerial", player), rule=lambda s: True)
        menu.connect(world.get_region("Combat.Dangerous", player),
                     rule=lambda s: s.has_any(("Double Jump", "Dash", "Bash", "Launch"), player))
        menu.connect(world.get_region("Combat.Shielded", player),
                     rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        menu.connect(world.get_region("Combat.Bat", player), rule=lambda s: True)
        menu.connect(world.get_region("Combat.Sand", player), rule=lambda s: s.has("Burrow", player))
        menu.connect(world.get_region("BreakCrystal", player),
                     rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade"), player))

    else:  # Unsafe
        menu.connect(world.get_region("DepthsLight", player),
                     rule=lambda state: state.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        menu.connect(world.get_region("Combat.Ranged", player),
                     rule=lambda state:
                     state.has_any(("Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"), player))
        menu.connect(world.get_region("Combat.Aerial", player), rule=lambda s: True)
        menu.connect(world.get_region("Combat.Dangerous", player),
                     rule=lambda s: s.has_any(("Double Jump", "Dash", "Bash", "Launch"), player))
        menu.connect(world.get_region("Combat.Shielded", player),
                     rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        menu.connect(world.get_region("Combat.Bat", player), rule=lambda s: True)
        menu.connect(world.get_region("Combat.Sand", player), rule=lambda s: s.has("Burrow", player))
        menu.connect(world.get_region("BreakCrystal", player),
                     rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade", "Spear"), player))


def glitch_rules(world, player: int, options: WotWOptions):
    """Defines rules for some glitches."""
    menu = world.get_region("Menu", player)
    if options.glitches:
        menu.connect(world.get_region("WaveDash", player), rule=lambda s: s.has_all(("Dash", "Regenerate"), player))
        menu.connect(world.get_region("HammerJump", player), rule=lambda s: s.has_all(("Double Jump", "Hammer"), player))
        menu.connect(world.get_region("SwordJump", player), rule=lambda s: s.has_all(("Double Jump", "Sword"), player))
        menu.connect(world.get_region("GlideHammerJump", player), rule=lambda s: s.has_all(("Glide", "Hammer"), player))
    else:  # Connect these events when the seed is completed, to make them reachable.
        menu.connect(world.get_region("WaveDash", player), rule=lambda s: s.has("Victory", player))
        menu.connect(world.get_region("HammerJump", player), rule=lambda s: s.has("Victory", player))
        menu.connect(world.get_region("SwordJump", player), rule=lambda s: s.has("Victory", player))
        menu.connect(world.get_region("GlideHammerJump", player), rule=lambda s: s.has("Victory", player))


def unreachable_rules(world, player: int, options: WotWOptions):
    """Rules to handle unreachable events."""
    diff = options.difficulty
    if diff == 0:
        unreach = ("WestHollow.AboveJumppad_to_WestHollow.LowerTongueRetracted",
                   "OuterWellspring.EntranceDoor_to_OuterWellspring.FallingWheel",
                   "MarshSpawn.PoolsBurrowsSignpost_to_E.MarshSpawn.PoolsBurrowsSignpost",
                   "GladesTown.MotayHut_to_C.GladesTown.MotayHut",
                   "GladesTown.UpperWest_to_C.GladesTown.UpperWest",
                   "GladesTown.AcornMoki_to_C.GladesTown.AcornMoki",
                   "GladesTown.AboveOpher_to_C.GladesTown.AboveOpher",
                   "GladesTown.HoleHutEntrance_to_C.GladesTown.HoleHutEntrance",
                   "OuterWellspring.EntranceDoor_to_H.OuterWellspring.EntranceDoor",
                   "OuterWellspring.EntranceDoor_to_E.OuterWellspring.EntranceDoor",
                   "WoodsMain.TrialStart_to_C.WoodsMain.TrialStart",
                   "WoodsMain.AbovePit_to_E.WoodsMain.AbovePit",
                   "UpperReach.TreeRoom_to_C.UpperReach.TreeRoom",
                   "UpperDepths.FirstKSRoom_to_C.UpperDepths.FirstKSRoom",
                   "UpperDepths.FirstKSRoom_to_E.UpperDepths.FirstKSRoom",
                   "UpperDepths.Central_to_E.UpperDepths.Central",
                   "LowerDepths.West_to_H.LowerDepths.West",
                   "LowerDepths.West_to_E.LowerDepths.West",
                   "UpperWastes.MissilePuzzleMiddle_to_C.UpperWastes.MissilePuzzleMiddle",
                   "WillowsEnd.Upper_to_E.WillowsEnd.Upper")
    elif diff == 1:
        unreach = ("OuterWellspring.EntranceDoor_to_OuterWellspring.FallingWheel",
                   "MarshSpawn.PoolsBurrowsSignpost_to_E.MarshSpawn.PoolsBurrowsSignpost",
                   "GladesTown.MotayHut_to_C.GladesTown.MotayHut",
                   "GladesTown.UpperWest_to_C.GladesTown.UpperWest",
                   "GladesTown.AcornMoki_to_C.GladesTown.AcornMoki",
                   "GladesTown.AboveOpher_to_C.GladesTown.AboveOpher",
                   "GladesTown.HoleHutEntrance_to_C.GladesTown.HoleHutEntrance",
                   "OuterWellspring.EntranceDoor_to_E.OuterWellspring.EntranceDoor",
                   "WoodsMain.TrialStart_to_C.WoodsMain.TrialStart",
                   "WoodsMain.AbovePit_to_E.WoodsMain.AbovePit",
                   "UpperReach.TreeRoom_to_C.UpperReach.TreeRoom",
                   "UpperDepths.FirstKSRoom_to_C.UpperDepths.FirstKSRoom",
                   "UpperDepths.FirstKSRoom_to_E.UpperDepths.FirstKSRoom",
                   "UpperDepths.Central_to_E.UpperDepths.Central")
    elif diff == 2:
        unreach = ("OuterWellspring.EntranceDoor_to_OuterWellspring.FallingWheel",
                   "GladesTown.MotayHut_to_C.GladesTown.MotayHut",
                   "GladesTown.UpperWest_to_C.GladesTown.UpperWest",
                   "GladesTown.AcornMoki_to_C.GladesTown.AcornMoki",
                   "GladesTown.AboveOpher_to_C.GladesTown.AboveOpher",
                   "GladesTown.HoleHutEntrance_to_C.GladesTown.HoleHutEntrance",
                   "OuterWellspring.EntranceDoor_to_E.OuterWellspring.EntranceDoor",
                   "WoodsMain.TrialStart_to_C.WoodsMain.TrialStart",
                   "WoodsMain.AbovePit_to_E.WoodsMain.AbovePit",
                   "UpperReach.TreeRoom_to_C.UpperReach.TreeRoom",
                   "UpperDepths.FirstKSRoom_to_C.UpperDepths.FirstKSRoom",
                   "UpperDepths.FirstKSRoom_to_E.UpperDepths.FirstKSRoom",
                   "UpperDepths.Central_to_E.UpperDepths.Central")
    else:
        unreach = ()

    for entr in unreach:  # Connect these events when the seed is completed, to make them reachable.
        set_rule(world.get_entrance(entr, player), lambda s: s.has("Victory", player))

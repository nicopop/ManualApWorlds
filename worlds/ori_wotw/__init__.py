"""AP world for Ori and the Will of the Wisps."""

# TODO Relics ? Black market ? Also make location groups for each area
# TODO fix player name with _
# TODO fix the in-game location counter


from typing import List, Dict, Tuple
from collections import Counter

from .Rules import (set_moki_rules, set_gorlek_rules, set_gorlek_glitched_rules, set_kii_rules,
                    set_kii_glitched_rules, set_unsafe_rules, set_unsafe_glitched_rules)
from .Additional_Rules import combat_rules, glitch_rules, unreachable_rules
from .Items import item_table, group_table
from .Items_Icons import get_item_iconpath
from .Locations import loc_table
from .Quests import quest_table
from .LocationGroups import loc_sets
from .Events import event_table
from .Regions import region_table
from .Entrances import entrance_table
from .Refills import refill_events
from .Options import WotWOptions, option_groups, LogicDifficulty, Quests
from .Spawn_items import spawn_items, spawn_names
from .Presets import options_presets
from .Headers import (h_core, h_better_spawn, h_no_combat_shrines, h_no_combat_arenas, h_no_combat_demibosses,
                      h_no_combat_bosses, h_no_hearts, h_no_quests, h_no_hand, h_no_trials, h_qol, h_no_ks,
                      h_open_mode, h_glades_done, h_hints, h_no_rain, h_knowledge)

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, set_rule
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, LocationProgressType


class WotWWeb(WebWorld):
    theme = "ocean"  # TODO documentation
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Ori and the Will of the Wisps randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Satisha"]
    )]
    options_presets = options_presets
    option_groups = option_groups
    bug_report_page = "https://discord.com/channels/731205301247803413/1272952565843103765"


class WotWWorld(World):
    """Ori and the Will of the Wisps is a 2D Metroidvania;
    The sequel to Ori and the blind forest, a platform game emphasizing exploration, collecting items and upgrades, and backtracking to previously inaccessible areas.
    The player controls the titular Ori, a white guardian spirit.
    """
    game = "Ori and the Will of the Wisps"
    web = WotWWeb()

    item_name_to_id = {name: data[2] for name, data in item_table.items()}
    location_name_to_id = loc_table

    item_name_groups = group_table

    options_dataclass = WotWOptions
    options: WotWOptions
    explicit_indirect_conditions = False

    required_client_version = (0, 5, 0)

    def __init__(self, multiworld, player):
        super(WotWWorld, self).__init__(multiworld, player)

    def generate_early(self):
        """Options checking"""
        if self.options.open_mode:
            self.options.no_rain.value = True

    def create_regions(self):
        world = self.multiworld
        player = self.player
        options = self.options

        # Contain all the locations that are used
        loc_list: List[str] = loc_sets["Base"] + loc_sets["ExtraQuests"]
        if not options.glades_done:
            loc_list += loc_sets["Rebuild"]
        if not options.no_trials:
            loc_list += loc_sets["Trials"]
        if not options.qol and not options.quests != Quests.option_none:
            loc_list += loc_sets["QOL"]
        if options.quests == Quests.option_no_hand:
            loc_list += loc_sets["Quests"]
        elif options.quests == Quests.option_all:
            loc_list += loc_sets["HandToHand"]
            loc_list += loc_sets["Quests"]

        for region_name in region_table:
            region = Region(region_name, player, world)
            world.regions.append(region)

        menu_region = Region("Menu", player, world)
        world.regions.append(menu_region)

        spawn_name = spawn_names[options.spawn]
        spawn_region = world.get_region(spawn_name, player)  # Links menu with spawn point
        menu_region.connect(spawn_region)

        menu_region.connect(world.get_region("HeaderStates", player))

        for loc_name in loc_table.keys():  # Create regions on locations
            region = Region(loc_name, player, world)
            world.regions.append(region)
        for quest_name in quest_table:  # Quests are locations that have to be tracked like events
            event_name = quest_name + ".quest"
            region = Region(event_name, player, world)
            world.regions.append(region)
            event = WotWLocation(player, event_name, None, region)
            event.show_in_spoiler = False
            event.place_locked_item(self.create_event(quest_name))
            region.locations.append(event)
            base_region = world.get_region(quest_name, player)
            base_region.connect(region)
        for loc_name in loc_list:  # Attach the used locations to their region
            region = world.get_region(loc_name, player)
            region.locations.append(WotWLocation(player, loc_name, self.location_name_to_id[loc_name], region))

        for event in event_table:  # Create events, their item, and a region to attach them
            region = Region(event, player, world)
            ev = WotWLocation(player, event, None, region)
            ev.show_in_spoiler = False
            ev.place_locked_item(self.create_event(event))
            world.regions.append(region)
            region.locations.append(ev)
        for event in refill_events:  # Create refill events, their item, and attach to their region
            region = Region(event, player, world)
            ev = WotWLocation(player, event, None, region)
            ev.show_in_spoiler = False
            ev.place_locked_item(self.create_event(event))
            world.regions.append(region)
            region.locations.append(ev)

        for entrance_name in entrance_table:  # Creates and connects the entrances
            (parent, connected) = entrance_name.split("_to_")
            parent_region = world.get_region(parent, player)
            connected_region = world.get_region(connected, player)
            entrance = parent_region.create_exit(entrance_name)
            entrance.access_rule = lambda state: False
            entrance.connect(connected_region)

        region = Region("Victory", player, world)  # Victory event
        ev = WotWLocation(player, "Victory", None, region)
        ev.place_locked_item(WotWItem("Victory", ItemClassification.progression, None, player))
        world.regions.append(region)
        region.locations.append(ev)

        world.completion_condition[player] = lambda state: state.has("Victory", player)

    def create_item(self, name: str) -> "WotWItem":
        return WotWItem(name, item_table[name][1], item_table[name][2], player=self.player)

    def create_items(self):
        world = self.multiworld
        player = self.player
        options = self.options

        skipped_items: List[str] = []  # Remove one instance of the item
        removed_items: List[str] = []  # Remove all instances of the item

        for item in spawn_items(world, options.spawn, options.difficulty):  # Staring items
            world.push_precollected(self.create_item(item))
            skipped_items.append(item)

        for item, count in options.start_inventory.value.items():
            for _ in range(count):
                skipped_items.append(item)

        if options.sword:
            world.push_precollected(self.create_item("Sword"))
            removed_items.append("Sword")

        if not options.tp:
            for item in group_table["teleporters"]:
                removed_items.append(item)

        if not options.extratp:
            for item in group_table["extra_tp"]:
                removed_items.append(item)

        if not options.bonus:
            for item in group_table["bonus"]:
                removed_items.append(item)

        if not options.extra_bonus:
            for item in group_table["bonus+"]:
                removed_items.append(item)

        if not options.skill_upgrade:
            for item in group_table["skill_upgrades"]:
                removed_items.append(item)

        if options.glades_done:
            removed_items.append("Ore")

        if options.no_ks:
            removed_items.append("Keystone")

        if options.vanilla_shop_upgrades:
            shop_items = {"OpherShop.ExplodingSpike": "Exploding Spear",
                          "OpherShop.ShockSmash": "Hammer Shockwave",
                          "OpherShop.StaticStar": "Static Shuriken",
                          "OpherShop.ChargeBlaze": "Charge Blaze",
                          "OpherShop.RapidSentry": "Rapid Sentry",
                          "OpherShop.WaterBreath": "Water Breath",
                          "TwillenShop.Overcharge": "Overcharge",
                          "TwillenShop.TripleJump": "Triple Jump",
                          "TwillenShop.Wingclip": "Wingclip",
                          "TwillenShop.Swap": "Swap",
                          "TwillenShop.LightHarvest": "Light Harvest",
                          "TwillenShop.Vitality": "Vitality",
                          "TwillenShop.Energy": "Energy (Shard)",
                          "TwillenShop.Finesse": "Finesse"}
            for location, item in shop_items.items():
                loc = world.get_location(location, player)
                loc.place_locked_item(self.create_item(item))
                removed_items.append(item)

        if options.launch_on_seir:
            world.get_location("WindtornRuins.Seir", player).place_locked_item(self.create_item("Launch"))
            removed_items.append("Launch")

        counter = Counter(skipped_items)
        pool: List[WotWItem] = []

        for item, data in item_table.items():
            if item in removed_items:
                count = -counter[item]
            else:
                count = data[0] - counter[item]
            if count <= 0:  # This can happen with starting inventory
                count = 0

            for _ in range(count):
                pool.append(self.create_item(item))

        extras = len(world.get_unfilled_locations(player=self.player)) - len(pool)
        for _ in range(extras):
            pool.append(self.create_item(self.get_filler_item_name()))

        world.itempool += pool

        if options.difficulty == LogicDifficulty.option_moki:
            # Exclude a location that is inaccessible in the lowest difficulty.
            skipped_loc = world.get_location("WestPools.BurrowOre", player)
            skipped_loc.progress_type = LocationProgressType.EXCLUDED

    def create_event(self, event: str) -> "WotWItem":
        return WotWItem(event, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(["50 Spirit Light", "100 Spirit Light"])

    def set_rules(self):
        world = self.multiworld
        player = self.player
        options = self.options
        menu = world.get_region("Menu", player)
        difficulty = options.difficulty

        # Add the basic rules.
        set_moki_rules(world, player, options)
        combat_rules(world, player, options)
        glitch_rules(world, player, options)
        unreachable_rules(world, player, options)

        # Add rules depending on the logic difficulty.
        if difficulty == LogicDifficulty.option_moki:
            # Extra rule for a location that is inaccessible in the lowest difficulty.
            add_rule(world.get_entrance("WestPools.Teleporter_to_WestPools.BurrowOre", player),
                     lambda state: state.has_all(("Burrow", "Clean Water", "Water Dash"), player), "or")
        if difficulty >= LogicDifficulty.option_gorlek:
            set_gorlek_rules(world, player, options)
            if options.glitches:
                set_gorlek_glitched_rules(world, player, options)
        if difficulty >= LogicDifficulty.option_kii:
            set_kii_rules(world, player, options)
            if options.glitches:
                set_kii_glitched_rules(world, player, options)
        if difficulty == LogicDifficulty.option_unsafe:
            set_unsafe_rules(world, player, options)
            if options.glitches:
                set_unsafe_glitched_rules(world, player, options)

        # Add victory condition
        victory_conn = world.get_region("WillowsEnd.Upper", player).connect(world.get_region("Victory", player))
        set_rule(victory_conn, lambda s: s.has_any(("Sword", "Hammer"), player)
                         and s.has_all(("Double Jump", "Dash", "Bash", "Grapple", "Glide", "Burrow", "Launch"), player))

        if "trees" in options.goal:
            add_rule(victory_conn, lambda s: all([s.can_reach_region(tree, player)
                          for tree in ["MarshSpawn.RegenTree",
                                       "MarshSpawn.DamageTree",
                                       "HowlsDen.SwordTree",
                                       "HowlsDen.DoubleJumpTree",
                                       "MarshPastOpher.BowTree",
                                       "WestHollow.DashTree",
                                       "EastHollow.BashTree",
                                       "GladesTown.DamageTree",
                                       "InnerWellspring.GrappleTree",
                                       "UpperPools.SwimDashTree",
                                       "UpperReach.LightBurstTree",
                                       "LowerDepths.FlashTree",
                                       "LowerWastes.BurrowTree",
                                       "WeepingRidge.LaunchTree",
                                       ]
                          ])
                     )

        if "wisps" in options.goal:
            add_rule(victory_conn, lambda s: s.has_all(("EastHollow.ForestsVoice", "LowerReach.ForestsMemory",
                                                        "UpperDepths.ForestsEyes", "WestPools.ForestsStrength",
                                                        "WindtornRuins.Seir"), player)
                     )
        if "quests" in options.goal:
            quest_list: List[str] = loc_sets["ExtraQuests"]
            if options.quests == Quests.option_no_hand:
                quest_list += loc_sets["Quests"]
            elif options.quests == Quests.option_all:
                quest_list += loc_sets["Quests"] + loc_sets["HandToHand"]
            if not options.glades_done:
                quest_list += loc_sets["Rebuild"]
            if not options.qol and options.quests != Quests.option_none:
                quest_list += loc_sets["QOL"]
            add_rule(victory_conn, lambda s: s.has_all((quests for quests in quest_list), player))

        def try_connect(region_in: Region, region_out: Region, connection: str|None = None, rule=None):
            """Create the region connection if it doesn't already exist."""
            if connection is None:
                connection = f"{region_in.name} -> {region_out.name}"
            if not world.regions.entrance_cache[player].get(connection):
                region_in.connect(region_out, connection, rule)

        # Rules for specific options
        if options.qol:
            try_connect(menu, world.get_region("GladesTown.TuleySpawned", player))
            world.get_region("WoodsEntry.LastTreeBranch", player).connect(
                world.get_region("WoodsEntry.TreeSeed", player))
        if options.better_spawn:
            try_connect(menu, world.get_region("MarshSpawn.HowlBurnt", player))
            try_connect(menu, world.get_region("HowlsDen.BoneBarrier", player))
            try_connect(menu, world.get_region("EastPools.EntryLever", player))
            try_connect(menu, world.get_region("UpperWastes.LeverDoor", player))

        if "Everything" in options.no_combat or "Bosses" in options.no_combat:
            for entrance in ("HeaderStates_to_SkipKwolok",
                             "HeaderStates_to_SkipMora1",
                             "HeaderStates_to_SkipMora2"):
                set_rule(world.get_entrance(entrance, player), lambda s: True)
        else:  # Connect these events when the seed is completed, to make them reachable.
            set_rule(world.get_entrance("HeaderStates_to_SkipKwolok", player),
                     lambda s: s.has("Victory", player))
            set_rule(world.get_entrance("HeaderStates_to_SkipMora1", player),
                     lambda s: s.has("Victory", player))
            set_rule(world.get_entrance("HeaderStates_to_SkipMora2", player),
                     lambda s: s.has("Victory", player))
        if "Everything" in options.no_combat or "Shrines" in options.no_combat:
            for entrance in (
                        "DenShrine_to_HowlsDen.CombatShrineCompleted",
                        "MarshShrine_to_MarshPastOpher.CombatShrineCompleted",
                        "GladesShrine_to_WestGlades.CombatShrineCompleted",
                        "WoodsShrine_to_WoodsMain.CombatShrineCompleted",
                        "DepthsShrine_to_LowerDepths.CombatShrineCompleted"):
                set_rule(world.get_entrance(entrance, player), lambda s: True)

        if options.better_wellspring:
            try_connect(menu, world.get_region("InnerWellspring.TopDoorOpen", player))
        if options.no_ks:
            for event in ("MarshSpawn.KeystoneDoor",
                          "HowlsDen.KeystoneDoor",
                          "MidnightBurrows.KeystoneDoor",
                          "WoodsEntry.KeystoneDoor",
                          "WoodsMain.KeystoneDoor",
                          "LowerReach.KeystoneDoor",
                          "UpperReach.KeystoneDoor",
                          "UpperDepths.EntryKeystoneDoor",
                          "UpperDepths.CentralKeystoneDoor",
                          "UpperPools.KeystoneRoomBubbleFree",
                          "UpperPools.KeystoneDoor",
                          "UpperWastes.KeystoneDoor"):
                try_connect(menu, world.get_region(event, player))
        if options.open_mode:
            for event in ("HowlsDen.BoneBarrier",
                          "MarshSpawn.ToOpherBarrier",
                          "MarshSpawn.TokkBarrier",
                          "MarshSpawn.LogBroken",
                          "MarshSpawn.BurrowsOpen",
                          "MidnightBurrows.HowlsDenShortcut",
                          "MarshPastOpher.EyestoneDoor",
                          "WestHollow.PurpleDoorOpen",
                          "EastHollow.DepthsLever",
                          "GladesTown.GromsWall",
                          "OuterWellspring.EntranceDoorOpen",
                          "InnerWellspring.MiddleDoorsOpen",
                          "InnerWellspring.TopDoorOpen",
                          "EastHollow.DepthsOpen",
                          "LowerReach.Lever",
                          "LowerReach.TPLantern",
                          "LowerReach.RolledSnowball",
                          "LowerReach.EastDoorLantern",
                          "LowerReach.ArenaBeaten",
                          "UpperWastes.LeverDoor",
                          "WindtornRuins.RuinsLever",
                          "WeepingRidge.ElevatorFightCompleted",
                          "EastPools.EntryLever",
                          "EastPools.CentralRoomPurpleWall",
                          "UpperPools.UpperWaterDrained",
                          "UpperPools.ButtonDoorAboveTree",):
                try_connect(menu, world.get_region(event, player))
        if options.no_rain:
            for event in ("HowlsDen.UpperLoopExitBarrier",
                          "HowlsDen.UpperLoopEntranceBarrier",
                          "HowlsDen.RainLifted",):
                try_connect(menu, world.get_region(event, player))
            if not options.better_spawn:
                try_connect(menu, world.get_region("MarshSpawn.HowlBurnt", player))
        if options.glades_done:
            for quest in ("InnerWellspring.BlueMoonSeed",
                          "EastPools.GrassSeed",
                          "UpperDepths.LightcatcherSeed",
                          "UpperReach.SpringSeed",
                          "UpperWastes.FlowersSeed",
                          "WoodsEntry.TreeSeed",
                          "GladesTown.RebuildTheGlades",
                          "GladesTown.RegrowTheGlades",):
                try_connect(menu, world.get_region(quest + ".quest", player))
            for event in ("GladesTown.BuildHuts",
                          "GladesTown.RoofsOverHeads",
                          "GladesTown.OnwardsAndUpwards",
                          "GladesTown.ClearThorns",
                          "GladesTown.CaveEntrance"):
                try_connect(menu, world.get_region(event, player))

        if options.quests != Quests.option_none:  # Open locations locked behind NPCs
            for quest in ("WoodsEntry.LastTreeBranch",
                          "WoodsEntry.DollQI",
                          "GladesTown.FamilyReunionKey"):
                try_connect(menu, world.get_region(quest + ".quest", player))

    def generate_output(self, output_directory: str) -> None:
        world = self.multiworld
        player = self.player
        options = self.options

        logic_difficulty: List[str] = ["Moki", "Gorlek", "Kii", "Unsafe"]
        coord: List[str] = [
            r"-799, -4310  // MarshSpawn.Main",  # Spawn coordinates
            r"-945, -4582  // MidnightBurrows.Teleporter",
            r"-328, -4536  // HowlsDen.Teleporter",
            r"-150, -4238  // EastHollow.Teleporter",
            r"-307, -4153  // GladesTown.Teleporter",
            r"-1308, -3675  // InnerWellspring.Teleporter",
            r"611, -4162  // WoodsEntry.Teleporter",
            r"1083, -4052  // WoodsMain.Teleporter",
            r"-259, -3962  // LowerReach.Teleporter",
            r"513, -4361  // UpperDepths.Teleporter",
            r"-1316, -4153  // EastPools.Teleporter",
            r"-1656, -4171  // WestPools.Teleporter",
            r"1456, -3997  // LowerWastes.WestTP",
            r"1992, -3902  // LowerWastes.EastTP",
            r"2044, -3679  // UpperWastes.NorthTP",
            r"2130, -3984  // WindtornRuins.RuinsTP",
            r"422, -3864  // WillowsEnd.InnerTP"
        ]
        shops: Dict[str, Tuple] = {
            "TwillenShop.Overcharge": ("2|1", "2|101"),  # Location name: (Uberstate, Price State)
            "TwillenShop.TripleJump": ("2|2", "2|102"),
            "TwillenShop.Wingclip": ("2|3", "2|103"),
            "TwillenShop.Swap": ("2|5", "2|105"),
            "TwillenShop.LightHarvest": ("2|19", "2|119"),
            "TwillenShop.Vitality": ("2|22", "2|122"),
            "TwillenShop.Energy": ("2|26", "2|126"),
            "TwillenShop.Finesse": ("2|40", "2|140"),
            "OpherShop.WaterBreath": ("1|23", "1|10023"),
            "OpherShop.Spike": ("1|74", "1|10074"),
            "OpherShop.SpiritSmash": ("1|98", "1|10098"),
            "OpherShop.Teleport": ("1|105", "1|10105"),
            "OpherShop.SpiritStar": ("1|106", "1|10106"),
            "OpherShop.Blaze": ("1|115", "1|10115"),
            "OpherShop.Sentry": ("1|116", "1|10116"),
            "OpherShop.ExplodingSpike": ("1|1074", "1|11074"),
            "OpherShop.ShockSmash": ("1|1098", "1|11098"),
            "OpherShop.StaticStar": ("1|1106", "1|11106"),
            "OpherShop.ChargeBlaze": ("1|1115", "1|11115"),
            "OpherShop.RapidSentry": ("1|1116", "1|11116"),
            "LupoShop.HCMapIcon": ("48248|19396", "48248|19397"),
            "LupoShop.ECMapIcon": ("48248|57987", "48248|57988"),
            "LupoShop.ShardMapIcon": ("48248|41666", "48248|41667")
        }

        trials: Dict[str, List[str]] = {
            "MarshPastOpher.SpiritTrial":
                [r"44964|45951=1|6|Complete the Marsh Spirit Trial to gain\n", r"3|100|4|29|100|Reward: "],
            "WestHollow.SpiritTrial":
                [r"44964|25545=1|6|Complete the Hollow Spirit Trial to gain\n", r"3|101|4|29|101|Reward: "],
            "OuterWellspring.SpiritTrial":
                [r"44964|11512=1|6|Complete the Wellspring Spirit Trial to gain\n", r"3|102|4|29|102|Reward: "],
            "WoodsMain.SpiritTrial":
                [r"44964|22703=1|6|Complete the Woods Spirit Trial to gain\n", r"3|103|4|29|103|Reward: "],
            "LowerReach.SpiritTrial":
                [r"44964|23661=1|6|Complete the Reach Spirit Trial to gain\n", r"3|104|4|29|104|Reward: "],
            "LowerDepths.SpiritTrial":
                [r"44964|28552=1|6|Complete the Mouldwood Spirit Trial to gain\n", r"3|105|4|29|105|Reward: "],
            "EastPools.SpiritTrial":
                [r"44964|54686=1|6|Complete the Luma Spirit Trial to gain\n", r"3|106|4|29|106|Reward: "],
            "LowerWastes.SpiritTrial":
                [r"44964|30767=1|6|Complete the Wastes Spirit Trial to gain\n", r"3|107|4|29|107|Reward: "]
        }

        shrines: Dict[str, str] = {
            "MarshPastOpher.CombatShrine": r"9|14|6|Complete the Marsh Combat Shrine to gain\n",
            "HowlsDen.CombatShrine": r"9|15|6|Complete the Howl's Den Combat Shrine to gain\n",
            "WestGlades.CombatShrine": r"9|16|6|Complete the Glades Combat Shrine to gain\n",
            "WoodsMain.CombatShrine": r"9|17|6|Complete the Woods Combat Shrine to gain\n",
            "LowerDepths.CombatShrine": r"9|18|6|Complete the Mouldwood Combat Shrine to gain\n"
        }

        flags = f"Flags: AP, {logic_difficulty[options.difficulty]}"
        if "trees" in options.goal:
            flags += ", All Trees"
        if "quests" in options.goal:
            flags += ", All Quests"
        if "wisps" in options.goal:
            flags += ", All Wisps"
        if options.glitches:
            tricks = ("\"SwordSentryJump\",\"GlideHammerJump\",\"SentryRedirect\",\"HammerJump\",\"BlazeSwap\","
                      "\"LaunchSwap\",\"SpearBreak\",\"ShurikenBreak\",\"GlideJump\",\"GrenadeRedirect\","
                      "\"GrenadeJump\",\"FlashSwap\",\"RemoveKillPlane\",\"HammerBreak\",\"HammerSentryJump\","
                      "\"SpearJump\",\"PauseHover\",\"SwordJump\",\"WaveDash\",\"SentrySwap\","
                      "\"SentryBurn\",\"SentryBreak\"")
        else:
            tricks = ""
        if options.hard_mode:
            hard = "true"
        else:
            hard = "false"
        head = (r"// Format Version: 1.0.0" + "\n"
                r"// Config: {" + f"\"seed\":\"{world.seed_name}\",\"worldSettings\":["
                "{\"spawn\":\"Random\",\"difficulty\":" + f"\"{logic_difficulty[options.difficulty]}\""
                f",\"tricks\":[{tricks}],\"hard\":{hard},\"goals\":[],\"headers\":[]"
                ",\"headerConfig\":[],\"inlineHeaders\":[]}],\"disableLogicFilter\":false,"
                "\"online\":false,\"createGame\":\"None\"}\n\n")
        connect = ("APAddress:archipelago.gg\n"
                   "APPort:38281\n"
                   "APPassword:\n"
                   f"APSlot:{world.player_name[player]}\n"
                   f"APSeed:{world.seed_name}\n\n\n")

        output = r"Spawn: " + coord[options.spawn] + "\n\n"
        output += h_core

        def get_location_item(location_name, player):
            item = world.get_location(location_name, player).item
            if item is None:
                item = Item("Nothing", ItemClassification.filler, None, player)
            return item

        output += r"// Shops" + "\n"
        for loc, states in shops.items():
            item = get_location_item(loc, player)
            text = f"{item.name} ({item.game})"
            output += f"3|1|8|{states[1]}|int|200\n"  # Fix the price
            output += f"3|1|17|1|{states[0]}|{text}\n"  # Add the item name

            # Sometimes apworld use ints, since 0.6.0 that needs to be converted explicitly
            classification = ItemClassification(item.classification)
            target_player_name = self.multiworld.get_player_name(item.player) if item.player != player else "you"
            if ItemClassification.trap in classification and ItemClassification.progression in classification:
                description = f"This item might be important but you might want to avoid buying this for now. Ask {target_player_name} about it."
            elif ItemClassification.trap in classification:
                fakeclassification = self.random.choice(["important", "useful", "unimportant"])
                description = f"This item might be {fakeclassification} for {target_player_name}?"
            elif ItemClassification.progression in classification:
                description = f"This item might be important for {target_player_name}."
            elif ItemClassification.useful in classification:
                description = f"This item might be useful for {target_player_name}."
            else:
                description = f"This item might be unimportant for {target_player_name}."

            output += f"3|1|17|2|{states[0]}|{description}\n"  # Add the item description

            icon_path = get_item_iconpath(self, item, bool(options.shop_keywords))
            if icon_path:
                output += f"3|1|17|0|{states[0]}|{icon_path}\n"

        output += "\n\n"

        if options.hints:
            output += r"// Shrine and Trial hints"
            output += h_hints
            for loc, state in shrines.items():
                item = get_location_item(loc, player)
                target_player_name = self.multiworld.get_player_name(item.player) if item.player != player else "you"
                text = f"{item.name} for {target_player_name}\n"
                output += state + text
            if not options.no_trials:
                output += r"// Trial hints" + "\n"
                for loc, states in trials.items():
                    item = get_location_item(loc, player)
                    target_player_name = self.multiworld.get_player_name(item.player) if item.player != player else "you"
                    text = f"{item.name} for {target_player_name}\n"
                    output += states[0] + text
                    output += states[1] + text
            output += "\n\n"

        if options.glitches:
            flags += ", Glitches"
        if options.tp:
            flags += ", Teleporters"
        if options.better_spawn:
            output += h_better_spawn
        if options.no_combat:
            output += r"//No Combat" + "\n"
            no_combat = "Everything" in options.no_combat
            if no_combat or "Shrines" in options.no_combat:
                output += h_no_combat_shrines
            if no_combat or "Arenas" in options.no_combat:
                output += h_no_combat_arenas
            if no_combat or "Demi Bosses" in options.no_combat:
                output += h_no_combat_demibosses
            if no_combat or "Bosses" in options.no_combat:
                output += h_no_combat_bosses
            flags += ", No Combat"

        if options.quests == Quests.option_no_hand:
            output += h_no_hand
            flags += ", No Quests"
        elif options.quests == Quests.option_none:
            output += h_no_hand
            output += h_no_quests
            flags += ", No Quests"

        if options.no_hearts:
            output += h_no_hearts
            flags += ", No Willow Hearts"
        if options.no_trials:
            output += h_no_trials
            flags += ", No Trials"
        if options.glades_done:
            output += h_glades_done
            flags += ", Glades Done"
        if options.better_wellspring:
            output += r"// Better Wellspring" + "\n" + r"3|0|8|37858|31962|bool|true" + "\n\n"
            flags += ", Better Wellspring"
        if options.qol:
            output += h_qol
        if options.no_ks:
            output += h_no_ks
            flags += ", No Keystone Doors"
        if options.open_mode:
            output += h_open_mode
            flags += ", Open Mode"
        if options.no_rain:
            output += h_no_rain
            flags += ", No Rain"
        if options.knowledge_hints:
            output += h_knowledge

        flags += "\n"
        file_name = f"/AP_{world.player_name[player]}_{world.seed_name[:4]}.wotwr"
        with open(output_directory + file_name, "w", encoding="utf-8") as f:
            f.write(connect + flags + output + head)


class WotWItem(Item):
    game: str = "Ori and the Will of the Wisps"


class WotWLocation(Location):
    game: str = "Ori and the Will of the Wisps"

"""Initialisation file."""

from typing import List, TextIO, Dict
from collections import Counter

from .Rules import (set_moki_rules, set_gorlek_rules, set_gorlek_glitched_rules, set_kii_rules,
                    set_kii_glitched_rules, set_unsafe_rules, set_unsafe_glitched_rules)
from .Items import item_table, group_table
from .Locations import loc_table
from .Quests import quest_table
from .Options import WotWOptions  # TODO add options_presets
from .Events import event_table
from .Regions import region_table
from .Entrances import entrance_table
from .Refills import refill_events
from .Additional_Rules import combat_rules, glitch_rules, unreachable_rules
from .Spawn_items import spawn_items, spawn_names
from .Presets import options_presets

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, forbid_item, forbid_items_for_player
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification


class WotWWeb(WebWorld):
    theme = "ocean"  # TODO documentation, presets (create them in Options)
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Ori and the Will of the Wisps randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        [""]
    )]
    options_presets = options_presets


class WotWWorld(World):
    game = "Ori and the Will of the Wisps"
    web = WotWWeb()

    item_name_to_id = {name: data[2] for name, data in item_table.items()}
    location_name_to_id = loc_table

    item_name_groups = group_table

    options_dataclass = WotWOptions
    options: WotWOptions

    ref_resource: Dict[str, List] = {region: [0, 0, 30, 3] for region in region_table}

    required_client_version = (0, 5, 0)

    def __init__(self, multiworld, player):
        super(WotWWorld, self).__init__(multiworld, player)

    def generate_early(self):  # TODO costs
        pass

    def create_regions(self):
        world = self.multiworld
        player = self.player
        options = self.options

        for region_name in region_table:
            region = Region(region_name, player, world)
            world.regions.append(region)

        menu_region = Region("Menu", player, world)
        world.regions.append(menu_region)

        spawn_name = spawn_names[options.spawn]
        spawn_region = world.get_region(spawn_name, player)  # Links menu with spawn point
        menu_region.connect(spawn_region)
        WotWWorld.ref_resource[spawn_name] = [30, 3, 30, 3]

        menu_region.connect(world.get_region("HeaderStates", player))

        for loc_name in loc_table.keys():  # Create regions on locations and attach locations
            region = Region(loc_name, player, world)
            world.regions.append(region)
            region.locations.append(WotWLocation(player, loc_name, self.location_name_to_id[loc_name], region))
            if loc_name in quest_table:  # Quests also have to be tracked like events
                quest_name = loc_name + ".quest"
                quest_loc = WotWLocation(player, quest_name, None, region)
                quest_loc.show_in_spoiler = False
                quest_loc.place_locked_item(WotWItem(loc_name, ItemClassification.progression_skip_balancing,
                                                     None, player))
                region.locations.append(quest_loc)

        for event in event_table:  # Create events, their item, and a region to attach them
            region = Region(event, player, world)
            ev = WotWLocation(player, event, None, region)
            ev.place_locked_item(WotWItem(event, ItemClassification.progression_skip_balancing, None, player))
            world.regions.append(region)
            region.locations.append(ev)
        for event in refill_events:  # Create refill events, their item, and attach to their region
            region = Region(event, player, world)
            ev = WotWLocation(player, event, None, region)
            ev.show_in_spoiler = False
            ev.place_locked_item(WotWItem(event, ItemClassification.progression_skip_balancing, None, player))
            world.regions.append(region)
            region.locations.append(ev)

        for entrance_name in entrance_table:  # Creates and connects the entrances
            (parent, connected) = entrance_name.split("_to_")
            parent_region = world.get_region(parent, player)
            connected_region = world.get_region(connected, player)
            entrance = parent_region.create_exit(entrance_name)
            entrance.access_rule = lambda state: False
            entrance.connect(connected_region)

        world.completion_condition[player] = lambda state: state.has("Victory", player)

    def create_item(self, name: str) -> "WotWItem":
        return WotWItem(name, item_table[name][1], item_table[name][2], player=self.player)

    def create_items(self):
        world = self.multiworld
        player = self.player
        options = self.options

        skipped_items = []  # Remove one instance of the item
        removed_items = []  # Remove all instances of the item
        junk: int = 0

        for item in spawn_items(world, options.spawn, options.difficulty):  # Staring items
            world.push_precollected(self.create_item(item))
            skipped_items.append(item)
            junk += 1

        for item, count in world.start_inventory[player].value.items():
            for _ in range(count):
                skipped_items.append(item)
                junk += 1

        if options.sword:
            world.push_precollected(self.create_item("Sword"))
            removed_items.append("Sword")

        if not options.tp:
            for item in group_table["teleporters"]:
                removed_items.append(item)

        if not options.extratp:
            for item in group_table["extratp"]:
                removed_items.append(item)

        if not options.bonus:
            for item in group_table["bonus"]:
                removed_items.append(item)

        if not options.extra_bonus:
            for item in group_table["bonus+"]:
                removed_items.append(item)

        if not options.skill_upgrade:
            for item in group_table["skillup"]:
                removed_items.append(item)

        if options.vanilla_shop_upgrades:
            shop_items = {"OpherShop.ExplodingSpike": "ExplodingSpear",
                          "OpherShop.ShockSmash": "HammerShockwave",
                          "OpherShop.StaticStar": "StaticShuriken",
                          "OpherShop.ChargeBlaze": "ChargeBlaze",
                          "OpherShop.RapidSentry": "RapidSentry",
                          "OpherShop.WaterBreath": "WaterBreath",
                          "TwillenShop.Overcharge": "Overcharge",
                          "TwillenShop.TripleJump": "TripleJump",
                          "TwillenShop.Wingclip": "Wingclip",
                          "TwillenShop.Swap": "Swap",
                          "TwillenShop.LightHarvest": "LightHarvest",
                          "TwillenShop.Vitality": "Vitality",
                          "TwillenShop.Energy": "EnergyShard",
                          "TwillenShop.Finesse": "Finesse"}
            for location, item in shop_items.items():
                loc = world.get_location(location, player)
                loc.place_locked_item(self.create_item(item))
                removed_items.append(item)
        if options.skip_trials:
            for loc in ("MarshPastOpher.SpiritTrial",
                        "WestHollow.SpiritTrial",
                        "OuterWellspring.SpiritTrial",
                        "EastPools.SpiritTrial",
                        "WoodsMain.SpiritTrial",
                        "LowerReach.SpiritTrial",
                        "LowerDepths.SpiritTrial",
                        "LowerWastes.SpiritTrial"):
                world.get_location(loc, player).progress_type = 3

        counter = Counter(skipped_items)
        pool: List[WotWItem] = []

        for item, data in item_table.items():
            if item in removed_items:
                junk += data[0]
                count = -counter[item]
            else:
                count = data[0] - counter[item]
            if count <= 0:  # This can happen with starting inventory
                junk += count
                count = 0

            for _ in range(count):
                pool.append(self.create_item(item))

        for _ in range(junk):
            pool.append(self.create_item("50 SpiritLight"))

        world.itempool += pool

        if options.difficulty == 0:  # Exclude a location that is inaccessible in the lowest difficulty.
            skipped_loc = world.get_location("WestPools.BurrowOre", player)
            skipped_loc.progress_type = 3

    def set_rules(self):
        world = self.multiworld
        player = self.player
        options = self.options
        ref_resource = WotWWorld.ref_resource
        menu = world.get_region("Menu", player)
        difficulty = options.difficulty
        goal = options.goal

        # Add the basic rules.
        set_moki_rules(world, player, options, ref_resource)
        combat_rules(world, player, options)
        glitch_rules(world, player, options)
        unreachable_rules(world, player, options)

        # Add rules depending on the logic difficulty.
        if difficulty == 0:  # Extra rule for a location that is inaccessible in the lowest difficulty.
            add_rule(world.get_entrance("WestPools.Teleporter_to_WestPools.BurrowOre", player),
                     lambda state: state.has_all(("Burrow", "Water", "WaterDash"), player), "or")
        if difficulty >= 1:
            set_gorlek_rules(world, player, options, ref_resource)
            if options.glitches:
                set_gorlek_glitched_rules(world, player, options, ref_resource)
        if difficulty >= 2:
            set_kii_rules(world, player, options, ref_resource)
            if options.glitches:
                set_kii_glitched_rules(world, player, options, ref_resource)
        if difficulty == 3:
            set_unsafe_rules(world, player, options, ref_resource)
            if options.glitches:
                set_unsafe_glitched_rules(world, player, options, ref_resource)

        # Add victory condition
        if goal == 0:
            menu.connect(world.get_region("Victory", player),
                         rule=lambda s: s.can_reach_region("WillowsEnd.Upper", player)
                                and s.has_any(("Sword", "Hammer"), player)
                                and s.has_all(("DoubleJump", "Dash", "Bash", "Grapple", "Glide", "Burrow", "Launch"), player)
                                and all([s.can_reach_region(tree, player) for tree in ["MarshSpawn.RegenTree",
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
                                                                                       ]])
                         )
        elif goal == 1:
            menu.connect(world.get_region("Victory", player),
                         rule=lambda s: s.can_reach_region("WillowsEnd.Upper", player)
                                        and s.has_any(("Sword", "Hammer"), player)
                                        and s.has_all(
                             ("DoubleJump", "Dash", "Bash", "Grapple", "Glide", "Burrow", "Launch"), player)
                                        and s.has_all(("EastHollow.ForestsVoice", "LowerReach.ForestsMemory",
                                                       "UpperDepths.ForestsEyes", "WestPools.ForestsStrength",
                                                       "WindtornRuins.Seir"), player)
                         )
        elif goal == 2:
            menu.connect(world.get_region("Victory", player),
                         rule=lambda s: s.can_reach_region("WillowsEnd.Upper", player)
                                        and s.has_any(("Sword", "Hammer"), player)
                                        and s.has_all(
                             ("DoubleJump", "Dash", "Bash", "Grapple", "Glide", "Burrow", "Launch"), player)
                                        and s.has_all((quest + ".quest" for quest in quest_table), player)
                         )
        else:
            menu.connect(world.get_region("Victory", player),
                         rule=lambda s: s.can_reach_region("WillowsEnd.Upper", player)
                                        and s.has_any(("Sword", "Hammer"), player)
                                        and s.has_all(
                             ("DoubleJump", "Dash", "Bash", "Grapple", "Glide", "Burrow", "Launch"), player))

        # Exclude Gorlek Ore from locations locked behind rebuilding Glades.
        ore_loc = ("GladesTown.FamilyReunionKey",
                   "GladesTown.KeyMokiHutEX",
                   "GladesTown.MotayHutEX",
                   "GladesTown.HoleHutEX",
                   "GladesTown.HoleHutEC",
                   "GladesTown.BraveMokiHutEX",
                   "GladesTown.ArcingShard",
                   "GladesTown.LupoSwimLeftEX",
                   "GladesTown.AboveCaveEX",
                   "GladesTown.AcornQI",
                   "GladesTown.MokiAcornQuest",
                   "GladesTown.CaveBurrowEX",
                   "GladesTown.RebuildTheGlades",
                   "WoodsEntry.DollQI")
        for location in ore_loc:
            forbid_item(world.get_location(location, player), "Ore", player)

        # Exclude Spirit Light from shops (except 1 Spirit Light).
        shop_loc = ("TwillenShop.Overcharge",
                    "TwillenShop.TripleJump",
                    "TwillenShop.Wingclip",
                    "TwillenShop.Swap",
                    "TwillenShop.LightHarvest",
                    "TwillenShop.Vitality",
                    "TwillenShop.Energy",
                    "TwillenShop.Finesse",
                    "OpherShop.WaterBreath",
                    "OpherShop.Spike",
                    "OpherShop.SpiritSmash",
                    "OpherShop.Teleport",
                    "OpherShop.SpiritStar",
                    "OpherShop.Blaze",
                    "OpherShop.Sentry",
                    "OpherShop.ExplodingSpike",
                    "OpherShop.ShockSmash",
                    "OpherShop.StaticStar",
                    "OpherShop.ChargeBlaze",
                    "OpherShop.RapidSentry",
                    "LupoShop.HCMapIcon",
                    "LupoShop.ECMapIcon",
                    "LupoShop.ShardMapIcon")
        for location in shop_loc:
            forbid_items_for_player(world.get_location(location, player),
                                    {"50 SpiritLight", "100 SpiritLight", "200 SpiritLight"}, player)

        # Exclude Keystones from small areas locked behind doors
        ks_loc = ("UpperReach.SpringSeed",
                  "UpperReach.LightBurstTree",
                  "UpperReach.WellEX",
                  "UpperReach.HiddenEX",
                  "UpperReach.TreeOre",
                  "LowerReach.SpiritTrial",
                  "MidnightBurrows.TabletQI",
                  "MarshSpawn.TokkTabletQuest",
                  "UpperPools.SwimDashTree",
                  "UpperPools.SwimDashCurrentEX",
                  "UpperPools.RoofEX",
                  "UpperPools.WaterfallEC",
                  "EastPools.PurpleWallHC",)
        for location in ks_loc:
            forbid_item(world.get_location(location, player), "Keystone", player)

        # Rules for specific options
        if options.better_spawn:
            menu.connect(world.get_region("MarshSpawn.HowlBurnt", player))
            menu.connect(world.get_region("HowlsDen.BoneBarrier", player))
            menu.connect(world.get_region("EastPools.EntryLever", player))
            menu.connect(world.get_region("UpperWastes.LeverDoor", player))
        if options.skip_combat:
            add_rule(world.get_entrance("HeaderStates_to_SkipKwolok", player),
                     lambda s: True, "or")
            add_rule(world.get_entrance("HeaderStates_to_SkipMora1", player), lambda s: True, "or")
            add_rule(world.get_entrance("HeaderStates_to_SkipMora2", player), lambda s: True, "or")
        else:  # Connect these events when the seed is completed, to make them reachable.
            add_rule(world.get_entrance("HeaderStates_to_SkipKwolok", player),
                     lambda s: s.has("Victory", player), "or")
            add_rule(world.get_entrance("HeaderStates_to_SkipMora1", player),
                     lambda s: s.has("Victory", player), "or")
            add_rule(world.get_entrance("HeaderStates_to_SkipMora2", player),
                     lambda s: s.has("Victory", player), "or")
        if options.better_wellspring:
            menu.connect(world.get_region("InnerWellspring.TopDoorOpen", player))

    # TODO probably better to do that automatically with the client, and get the settings from fill_slot_data
    def generate_output(self, output_directory: str):
        pass

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        pass
    # TODO: config tutorial, infos with fill_slot_data


class WotWItem(Item):
    game: str = "Ori and the Will of the Wisps"


class WotWLocation(Location):
    game: str = "Ori and the Will of the Wisps"

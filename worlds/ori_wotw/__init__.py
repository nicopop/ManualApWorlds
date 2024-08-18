"""Initialisation file."""

from collections import Counter

from .Rules import (set_moki_rules, set_gorlek_rules, set_gorlek_glitched_rules, set_kii_rules,
                    set_kii_glitched_rules, set_unsafe_rules, set_unsafe_glitched_rules)
from .Items import item_table, group_table, base_id
from .Locations import location_table, quest_table
from .Options import WotWOptions  # TODO add options_presets
from .Events import event_table
from .Regions import region_table
from .Entrances import entrance_table
from .Refills import refill_events

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification

spawn_names = {0: "MarshSpawn.Main",
               1: "MidnightBurrows.Teleporter",
               2: "HowlsDen.Teleporter",
               3: "EastHollow.Teleporter",
               4: "GladesTown.Teleporter",
               5: "InnerWellspring.Teleporter",
               6: "WoodsEntry.Teleporter",
               7: "WoodsMain.Teleporter",
               8: "LowerReach.Teleporter",
               9: "UpperDepths.Teleporter",
               10: "EastPools.Teleporter",
               11: "WestPools.Teleporter",
               12: "LowerWastes.WestTP",
               13: "LowerWastes.EastTP",
               14: "UpperWastes.NorthTP",
               15: "WindtornRuins.RuinsTP",
               16: "WillowsEnd.InnerTP"}


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
    # options_presets = options_presets


class WotWWorld(World):
    game = "Ori and the Will of the Wisps"
    web = WotWWeb()

    item_name_to_id = {item["name"]: (base_id + index) for index, item in enumerate(item_table)}
    location_name_to_id = {loc: (base_id + index) for index, loc in enumerate(location_table)}

    item_name_groups = group_table

    options_dataclass = WotWOptions
    options: WotWOptions

    required_client_version = (0, 4, 2)  # TODO check it

    def __init__(self, multiworld, player):
        super(WotWWorld, self).__init__(multiworld, player)

    def generate_early(self):  # TODO costs, items on spawn
        pass

    def set_rules(self):
        world = self.multiworld
        player = self.player
        options = self.options

        set_moki_rules(world, player, options)

        if options.difficulty == 0:  # Extra rule for a location that is inaccessible in the lowest difficulty.
            add_rule(world.get_location("WestPools.BurrowOre", player),
                     lambda state: state.can_reach_region("WestPools.Teleporter", player)
                     and state.has_all(("Burrow", "Water", "WaterDash"), player))

        if options.difficulty >= 1:
            set_gorlek_rules(world, player, options)
            if options.glitches:
                set_gorlek_glitched_rules(world, player, options)
        if options.difficulty >= 2:
            set_kii_rules(world, player, options)
            if options.glitches:
                set_kii_glitched_rules(world, player, options)
        if options.difficulty == 3:
            set_unsafe_rules(world, player, options)
            if options.glitches:
                set_unsafe_glitched_rules(world, player, options)

    def create_regions(self):
        world = self.multiworld
        player = self.player
        options = self.options

        for region_name in region_table:
            region = Region(region_name, player, world)
            world.regions.append(region)

        menu_region = Region("Menu", player, world)
        world.regions.append(menu_region)

        spawn_region = world.get_region(spawn_names[options.spawn], player)  # Links menu with spawn point
        menu_region.connect(spawn_region)

        menu_region.connect(world.get_region("HeaderStates", player))

        for loc_name in location_table:  # Create regions on locations and attach locations
            region = Region(loc_name, player, world)
            world.regions.append(region)
            region.locations.append(WotWLocation(player, loc_name, self.location_name_to_id[loc_name], region))
            if loc_name in quest_table:  # Quests also have to be tracked like events
                quest_name = loc_name + ".quest"
                quest_loc = WotWLocation(player, quest_name, None)
                quest_loc.place_locked_item(WotWItem(loc_name, ItemClassification.progression, None, player))
                region.locations.append(quest_loc)

        for event in event_table:  # Create events, their item, and a region to attach them
            ev = WotWLocation(player, event, None)
            ev.place_locked_item(WotWItem(event, ItemClassification.progression, None, player))
            region = Region(event, player, world)
            world.regions.append(region)
            region.locations.append(ev)
        for event in refill_events:  # Create refill events, their item, and attach to their region
            ev = WotWLocation(player, event, None)
            ev.place_locked_item(WotWItem(event, ItemClassification.progression, None, player))
            region = Region(event, player, world)
            world.regions.append(region)
            region.locations.append(ev)

        for entrance_name in entrance_table:  # Creates and connects the entrances
            (parent, connected) = entrance_name.split("_to_")
            parent_region = world.get_region(parent, player)
            entrance = parent_region.create_exit(entrance_name)
            entrance.connect(world.get_region(connected, player))

        world.completion_condition[player] = lambda state: state.has("Victory", player)

    def create_item(self, name):
        item_id = self.item_name_to_id[name]
        i = item_id - base_id
        return WotWItem(name, item_table[i]["classification"], item_id, player=self.player)

    def create_items(self):
        world = self.multiworld
        player = self.player
        options = self.options

        skipped_items = []
        junk: int = 0

        for item, count in world.start_inventory[player].value.items():
            for _ in range(count):
                skipped_items.append(item)
                junk += 1

        if options.sword:
            skipped_items.append("Sword")
            junk += 1

        if not options.tp:
            for item in group_table["teleporters"]:
                skipped_items.append(item)
            junk += 14

        if not options.extratp:
            for item in group_table["extratp"]:
                skipped_items.append(item)
            junk += 2

        if not options.bonus:
            for item in group_table["bonus"]:
                skipped_items.append(item)
            junk += 15

        if not options.extra_bonus:
            for item in group_table["bonus+"]:
                skipped_items.append(item)
            junk += 25

        if not options.skill_upgrade:
            for item in group_table["skillup"]:
                skipped_items.append(item)
            junk += 6

        counter = Counter(skipped_items)
        pool = []

        for item in item_table:
            count = item["count"] - counter[item["name"]]

            if count <= 0:
                continue
            for _ in range(count):
                pool.append(self.create_item(item["name"]))

        for _ in range(junk):
            pool.append(self.create_item("SpiritLight"))

        world.itempool += pool

        if options.difficulty == 0:  # Exclude a location that is inaccessible in the lowest difficulty.
            skipped_loc = world.get_location("WestPools.BurrowOre", player)
            skipped_loc.progress_type = 3

    # TODO: config tutorial, header file, infos with fill_slot_data, spoiler


class WotWItem(Item):
    game: str = "Ori and the Will of the Wisps"


class WotWLocation(Location):
    game: str = "Ori and the Will of the Wisps"

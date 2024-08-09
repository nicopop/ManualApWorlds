"""Initialisation file."""

from collections import Counter
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule
from BaseClasses import Region, Location, Entrance, Item, Tutorial, ItemClassification
from .Rules import set_moki_rules
# from .Rules import (set_moki_rules, set_gorlek_rules, set_gorlek_glitched_rules, set_kii_rules, set_kii_glitched_rules,
#                     set_unsafe_rules, set_unsafe_glitched_rules)
from .Items import item_table, group_table, base_id
from .Locations import location_table
from .Options import WotWOptions  # add options_presets
from .Events import event_table
from .Regions import add_regions
from .Entrances import entrance_table

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
    location_name_to_id = {loc["name"]: (base_id + index) for index, loc in enumerate(location_table)}
    location_name_to_game_id = {loc["name"]: loc["game_id"] for loc in location_table}

    item_name_groups = group_table

    options_dataclass = WotWOptions
    options: WotWOptions

    required_client_version = (0, 4, 2)  # TODO check it

    def __init__(self, multiworld, player):
        super(WotWWorld, self).__init__(multiworld, player)

    def generate_early(self):  # TODO costs, items on spawn
        pass

    def set_rules(self):  # TODO add other difficulties
        world = self.multiworld
        player = self.player
        options = self.options

        set_moki_rules(world, player)

        if options.difficulty == 0:  # Extra rule for a location that is inaccessible in the lowest difficulty.
            add_rule(world.get_location("WestPools.BurrowOre", player),
                     lambda state: state.can_reach_region("WestPools.Teleporter", player)
                     and state.has_all(("Burrow", "Water", "WaterDash"), player))

#        if options.difficulty >= 1:
#            set_gorlek_rules(world, player)
#            if world.glitches:
#                set_gorlek_glitched_rules(world, player)
#        if options.difficulty >= 2:
#            set_kii_rules(world, player)
#            if world.glitches:
#                set_kii_glitched_rules(world, player)
#        if options.difficulty == 3:
#            set_unsafe_rules(world, player)
#            if world.glitches:
#                set_unsafe_glitched_rules(world, player)
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
        # TODO remove debug comment

    def create_regions(self):
        world = self.multiworld
        player = self.player
        options = self.options

        add_regions(player, world)  # Adds the anchors
        menu_region = menu_region = Region("Menu", player, world)
        world.regions += menu_region

        spawn_region = spawn_names[options.spawn]  # Links menu with spawn point
        menu_region.connect(spawn_region)

        for entrance in entrance_table:  # Creates and connects the entrances
            (parent, connected) = entrance.split("_to_")
            ent = Entrance(player, entrance, world.get_region(parent, player))
            ent.connect(world.get_region(connected, player))

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

        if options.difficulty == 0:  # Exclude a location that is inaccessible in the lowest difficulty.
            skipped_loc = world.get_location("WestPools.BurrowOre", player)
            skipped_loc.progress_type = 3

        if options.sword[player]:
            skipped_items.append("Sword")
            junk += 1

        if not options.tp[player]:
            skipped_items.append(group_table["teleporters"])
            junk += 14

        if not options.extratp[player]:
            skipped_items.append(group_table["extratp"])
            junk += 2

        if not options.bonus[player]:
            skipped_items.append(group_table["bonus"])
            junk += 15

        if not options.extra_bonus[player]:
            skipped_items.append(group_table["bonus+"])
            junk += 25

        if not options.skill_upgrade[player]:
            skipped_items.append(group_table["skillup"])
            junk += 6

        counter = Counter(skipped_items)

        pool = []

        for item in item_table:
            count = item["count"] - counter[item["name"]]

            if count <= 0:
                continue
            else:
                for i in range(count):
                    pool.append(self.create_item(item["name"]))

        for _ in range(junk):
            pool.append(self.create_item("SpiritLight"))

        world.itempool += pool

        for event in event_table:  # Create events and their item
            ev = WotWLocation(player, event, None)
            ev.place_locked_item(WotWItem(event, ItemClassification.progression, None, player))
    # TODO: Config, spoiler, victory event


class WotWItem(Item):
    game: str = "Ori and the Will of the Wisps"


class WotWLocation(Location):
    game: str = "Ori and the Will of the Wisps"

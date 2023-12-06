# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, forbid_item, set_rule
from ..Data import load_data_file
from copy import copy

from BaseClasses import MultiWorld
import logging

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table
#from .Options import

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

logger = logging.getLogger()
PPMiscData = {}
"""Miscellaneous shared data"""
PPMiscData["KnownPlayers"] = []
PPOptions = {}
"""
Player options:
To access option value: PPOptions[player]["optionName"]
"""
PPWorkingData = {}
"""
Copy of any changed world item/locations
"""
########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. set_rules - Creates rules for accessing regions and locations
##    3. generate_basic - Creates the item pool and runs any place_item options
##    4. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    extra_data = load_data_file("extra.json")
    # Set version in yaml and log
    if not PPMiscData.get('version'):
        apworldversion = "Unknown"
        if 'version' in game_table:
            apworldversion = game_table['version']
        multiworld.game_version[player].value = apworldversion
        PPMiscData["version"] = apworldversion
        logger.info(f"player(s) uses {world.game} version: {apworldversion}")
    else:
        multiworld.game_version[player].value = PPMiscData["version"]
#Init Options
#region
    PPMiscData["KnownPlayers"].append(player)
    PPOptions[player] = {}
    PPMiscData[player] = {}
    PPOptions[player]['host_level'] = get_option_value(multiworld, player, "host_level") or 0
    PPOptions[player]['win_percent'] = get_option_value(multiworld, player, "win_percent") or 0
    PPOptions[player]['do_overtime'] = get_option_value(multiworld, player, "do_overtime") or 0
    PPOptions[player]['recipe_steak'] = get_option_value(multiworld, player, "recipe_steak") or 0
    PPOptions[player]["recipe_salad"] = get_option_value(multiworld, player, "recipe_salad") or 0
    PPOptions[player]["recipe_pizza"] = get_option_value(multiworld, player, "recipe_pizza") or 0
    PPOptions[player]["recipe_dumplings"] = get_option_value(multiworld, player, "recipe_dumplings") or 0
    PPOptions[player]["recipe_coffee"] = get_option_value(multiworld, player, "recipe_coffee") or 0
    PPOptions[player]["recipe_burger"] = get_option_value(multiworld, player, "recipe_burger") or 0
    PPOptions[player]["recipe_turkey"] = get_option_value(multiworld, player, "recipe_turkey") or 0
    PPOptions[player]["recipe_pie"] = get_option_value(multiworld, player, "recipe_pie") or 0
    PPOptions[player]["recipe_fish"] = get_option_value(multiworld, player, "recipe_fish") or 0
    PPOptions[player]["recipe_hotdog"] = get_option_value(multiworld, player, "recipe_hotdog") or 0
    PPOptions[player]["recipe_breakfast"] = get_option_value(multiworld, player, "recipe_breakfast") or 0
    PPOptions[player]["recipe_stirfry"] = get_option_value(multiworld, player, "recipe_stirfry") or 0
    #Options Check for imposibities
    for i in range(PPOptions[player]['host_level'] + 1, 16):
        recipes = extra_data.get(f"level_{i}", {}).get(f"region", [])
        for recipe in recipes:
            logger.debug(f"removed player {player} recipe_{recipe.lower().replace(' ', '')}")
            PPOptions[player][f"recipe_{recipe.lower().replace(' ', '')}"] = 0
    PPMiscData[player]["RecipeCount"] = 0
    for option, count in PPOptions[player].items():
        if option.startswith('recipe_'):
            PPMiscData[player]["RecipeCount"] += count
    #Is it safe to skip some code
    PPMiscData[player]['SafeGen'] = False #value for first run
    index = PPMiscData['KnownPlayers'].index(player)
    if index > 0:
        last_player = PPMiscData['KnownPlayers'][index - 1]
        PPMiscData[player]['SafeGen'] = True
        if PPOptions[player]['host_level'] != PPOptions[last_player]["host_level"]:
            PPMiscData[player]['SafeGen'] = False
        if PPOptions[player]["do_overtime"] != PPOptions[last_player]["do_overtime"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_steak"] != PPOptions[last_player]["recipe_steak"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_salad"] != PPOptions[last_player]["recipe_salad"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_pizza"] != PPOptions[last_player]["recipe_pizza"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_dumplings"] != PPOptions[last_player]["recipe_dumplings"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_coffee"] != PPOptions[last_player]["recipe_coffee"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_burger"] != PPOptions[last_player]["recipe_burger"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_turkey"] != PPOptions[last_player]["recipe_turkey"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_pie"] != PPOptions[last_player]["recipe_pie"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_fish"] != PPOptions[last_player]["recipe_fish"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_hotdog"] != PPOptions[last_player]["recipe_hotdog"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_breakfast"] != PPOptions[last_player]["recipe_breakfast"]:
            PPMiscData[player]["SafeGen"] = False
        elif PPOptions[player]["recipe_stirfry"] != PPOptions[last_player]["recipe_stirfry"]:
            PPMiscData[player]["SafeGen"] = False
        logger.debug(f'SafeGen for player {player} set to {PPMiscData[player]["SafeGen"]}')
#endregion
# Called after regions and locations are created, in case you want to see or modify that information.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    host_level = PPOptions[player]["host_level"]
    extra_data = load_data_file("extra.json")

    minWin = max(round(PPMiscData[player]["RecipeCount"]*(PPOptions[player]['win_percent']/100)), 2)
    PPMiscData[player]["MinWin"] = minWin

    fcount = 0
    for location in multiworld.get_unfilled_locations(player):
        if location.name == "All done":
            set_rule(location,
                     lambda state: state.has("Victory Token", player, minWin))
            fcount += 1
        elif location.name == "Get in a game for the first time":
            forbid_item(location, "Research Table", player)
            fcount +=1
        elif fcount >= 2:
            break

# Removing disabled Items
#region
    items_to_be_removed = []
    local = copy(world.item_name_to_item)
    localid = copy(world.item_id_to_name)
    localname = copy(world.item_name_to_id)
# First we get what items to remove

    for option, count in PPOptions[player].items():
        if option.startswith('recipe_') and not count:
            items_to_be_removed += extra_data[option]["items"]
    for i in range(PPOptions[player]['host_level'] + 1, 16):
        items_to_be_removed += extra_data.get(f"level_{i}", {}).get(f"items", [])

# Then we remove items in items_to_be_removed

    for name in items_to_be_removed:
        if name in local:
            localid.pop(local[name]['id'])
            localname.pop(name)
            local.pop(name, "")
    logger.debug(f"Done removing {len(world.item_name_to_item) - len(local)} items from player {player}.")
    world.item_name_to_item = local
    world.item_id_to_name = localid
    world.item_name_to_id = localname
#endregion
    pass
# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def before_generate_basic(item_pool: list, world: World, multiworld: MultiWorld, player: int):
    host_level = PPOptions[player]["host_level"]
    extra_data = load_data_file("extra.json")
    locations_to_be_removed = []
    items_to_be_removed = []
#Restore location placed items
#region
    if PPMiscData["KnownPlayers"][0] != player and PPMiscData[player]["SafeGen"] == False:
        RemovedPlacedItems = PPWorkingData.get("place_items", {})
        RemovedPlacedItemsCategory = PPWorkingData.get('place_items_cat', {})
        if len(RemovedPlacedItems) > 0 or len(RemovedPlacedItemsCategory) > 0:
            readded_place_item_Count = 0
            locationstoCheck = {}
            locationstoCheck.update(RemovedPlacedItems)
            locationstoCheck.update(RemovedPlacedItemsCategory)
            for location in locationstoCheck:
                if location in world.location_names:
                    worldlocation = world.location_name_to_location[location]
                    if location in RemovedPlacedItemsCategory:
                        worldlocation["place_item_category"] = RemovedPlacedItemsCategory[location]
                        RemovedPlacedItemsCategory.pop(location)
                    if location in RemovedPlacedItems:
                        worldlocation["place_item"] = RemovedPlacedItems[location]
                        RemovedPlacedItems.pop(location)
                    if "place_item" in worldlocation or "place_item_category" in worldlocation:
                        readded_place_item_Count += 1
            if readded_place_item_Count > 0:
                multiworld.clear_location_cache()
                logger.debug(f"ReAdded placed item info to {readded_place_item_Count} locations of player {player}.")
        pass
#endregion
# Personnal Item counts adjustment
#region
    #maxWin = round(PPMiscData[player]["RecipeCount"]*(PPOptions[player]['win_percent']/100))

    item_counts= {}

    item_counts["Victory Token"] = PPMiscData[player]["RecipeCount"]

    for name, count in item_counts.items():
        checkedname = copy(name)
        # future change item name here
        items = []
        for item in item_pool:
            if item.player != player:
                continue
            if item.name == checkedname:
                items.append(item)
        if len(items) > count:
            for x in range(len(items) - count):
                item_pool.remove(items[x])
#endregion
# Removing disabled locations
    for option, count in PPOptions[player].items():
        if option.startswith('recipe_') and not count:
            locations_to_be_removed += extra_data[option]["locations"]
    for i in range(PPOptions[player]['host_level'] + 1, 16):
        locations_to_be_removed += extra_data.get(f"level_{i}", {}).get(f"locations", [])
    if PPOptions[player]['do_overtime'] == False:
        locations_to_be_removed += extra_data.get('overtime', {}).get('locations', [])
# Removing locations in locations_to_be_removed
#region
    local_valid_locations = copy(world.location_name_to_location)
    removedlocCount = 1 #victory included
    if len(locations_to_be_removed) > 0:
        for region in multiworld.regions:
            if region.player != player:
                continue
            for location in list(region.locations):
                if location.name in locations_to_be_removed:
                    if PPMiscData[player]["SafeGen"] == False:
                        worldlocation = world.location_name_to_location[location.name]
                        if 'place_item' in worldlocation:
                            if not PPWorkingData.get("place_items"):
                                PPWorkingData["place_items"] = {}
                            PPWorkingData["place_items"][location.name] = copy(worldlocation["place_item"])
                            worldlocation.pop("place_item", "")
                        if'place_item_category' in worldlocation:
                            if not PPWorkingData.get("place_items_cat"):
                                PPWorkingData["place_items_cat"] = {}
                            PPWorkingData["place_items_cat"][location.name] = copy(worldlocation["place_item_category"])
                            worldlocation.pop("place_item_category", "")
                    region.locations.remove(location)
                    local_valid_locations.pop(location.name, "")
                    removedlocCount += 1
        multiworld.clear_location_cache()
    logger.info(f"{world.game}:{player}:(lvl {host_level}) {len(item_pool)} items | {len(world.location_names) - removedlocCount} locations")
#endregion
    return item_pool

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is called before the victory location has the victory event placed and locked
def before_pre_fill(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is called after the victory location has the victory event placed and locked
def after_pre_fill(world: World, multiworld: MultiWorld, player: int):
    pass

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data
# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation
from ..Data import load_data_file

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

import logging
from copy import copy

logger = logging.getLogger()
APMiscData = {}
"""Miscellaneous shared data"""
APMiscData["KnownPlayers"] = []
APOptions = {}
"""
Player options:
To access option value: PPOptions[player]["optionName"]
"""
APWorkingData = {}
"""
Copy of any changed world item/locations
"""
########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    extra_data = load_data_file("extra.json")
    if hasattr(world, 'options'):
        world.hasOptionsManager = True
    else:
        world.hasOptionsManager = False
    # Set version in yaml and log
    if not APMiscData.get('version'):
        APMiscData['version'] = "Unknown"
        APMiscData['043Compatible'] = False

        if 'version' in game_table:
            APMiscData['version'] = game_table['version']

        if hasattr(multiworld, 'clear_location_cache') and callable(multiworld.clear_location_cache):
            APMiscData['043Compatible'] = True

        logger.info(f"player(s) uses {world.game} version: {APMiscData['version']}")
    if world.hasOptionsManager:
        world.options.game_version.value = APMiscData["version"]
    else:
        multiworld.game_version[player].value = APMiscData["version"]
#Init Options
#region
    APMiscData["KnownPlayers"].append(player)
    # APOptions[player] = {}
    APMiscData[player] = {}
    APMiscData[player]['name'] = multiworld.get_player_name(player)

    if world.hasOptionsManager:
        #Options Check for imposibities
        for i in range(world.options.host_level.value + 1, 16):
            recipes = extra_data.get("Options").get(f"level_{i}", [])
            for recipe in recipes:
                logger.debug(f"removed player {player} recipe_{recipe.lower().replace(' ', '')}")
                option_name = f"recipe_{recipe.lower().replace(' ', '')}"
                if world.options.__dict__.get(option_name, {}):
                    world.options.__dict__[option_name].value = 0
        APMiscData[player]["EnabledRecipeCount"] = len([name for name, option in world.options.__dict__.items() if name.startswith('recipe_') and option.value])
        APMiscData[player]["EnabledRecipeCount"] += world.options.more_recipes.value
        #Is it safe to skip some code
        # APMiscData[player]["SafeGen"] = False #value for first run
        # index = APMiscData["KnownPlayers"].index(player)
        # if index > 0:
        #     index = APMiscData["KnownPlayers"][index - 1]
        #     LastOptions = multiworld.worlds[index].options
        #     CurOptions = world.options
        #     APMiscData[player]["SafeGen"] = True
        #     logger.debug(f'SafeGen for player {player} set to {APMiscData[player]["SafeGen"]}')
        # APOptions.pop(player)

#endregion

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    extra_data = load_data_file("extra.json")
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names
    if not APWorkingData.get('items_to_be_removed'):
        APWorkingData["items_to_be_removed"] = {}
    APWorkingData['items_to_be_removed'][player] = []

    # First we get what items and locations to remove
    def FindRecipeLoc(recipe: str):
        found = extra_data.get(recipe, {}).get("locations", [])
        if not found:
            recipe = recipe.split('_')[-1]

            for location in world.location_name_to_location.keys():
                if location.lower().replace(' ', '').startswith(recipe):
                    found.append(location)
                if len(found) >= 6:
                    break

        return found

    def FindRecipeItems(recipe: str):
        found = extra_data.get(recipe, {}).get("items", [])
        if not found:
            recipe = recipe.split('_')[-1].capitalize()
            recipeName = f'{recipe} Recipe'
            if recipeName in world.item_name_to_item.keys():
                found.append(recipeName)
            else:
                for item in world.item_name_to_item.keys():
                    if item.lower().replace(' ', '').startswith(recipe.lower()):
                        found.append(item)
                        break
        return found

    if world.hasOptionsManager:
        DisabledRecipe = [name for name, option in world.options.__dict__.items() if name.startswith('recipe_') and not option.value]
        for option in DisabledRecipe:
            APWorkingData['items_to_be_removed'][player].extend(FindRecipeItems(option))
            locationNamesToRemove += FindRecipeLoc(option)

    if len(locationNamesToRemove) > 0:
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in locationNamesToRemove:
                        region.locations.remove(location)
        if hasattr(multiworld, "clear_location_cache"):
            multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names
    item_counts= {}
    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.
    for item in APWorkingData["items_to_be_removed"].get(player, []):
        item_counts[item] = 0

    item_counts["Victory Token"] = APMiscData[player]["EnabledRecipeCount"]

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


    # for itemName in itemNamesToRemove:
    #     item = next(i for i in item_pool if i.name == itemName)
    #     item_pool.remove(item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    from BaseClasses import ItemClassification
    location_count = len(multiworld.get_unfilled_locations(player))
    filler = 0
    if world.hasOptionsManager:
        host_level = world.options.host_level.value
    for item in item_pool:
        if item.classification == ItemClassification.filler or item.classification == ItemClassification.trap:
            filler += 1
    if world.options.more_recipes.value:
        logger.info(f"{world.game}:{APMiscData[player]['name']}({player}):(lvl {host_level})(extra: {world.options.more_recipes.value}) {len(item_pool) - filler} items | {location_count} locations")
    else:
        logger.info(f"{world.game}:{APMiscData[player]['name']}({player}):(lvl {host_level}) {len(item_pool) - filler} items | {location_count} locations")
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location
    if world.hasOptionsManager:
        minWin = max(round(APMiscData[player]["EnabledRecipeCount"]*(world.options.win_percent.value /100)), 2)
    APMiscData[player]["MinWin"] = minWin

    for location in multiworld.get_unfilled_locations(player):
        if location.name == "All done":
            set_rule(location,
                     lambda state: state.has("Victory Token", player, minWin))
            break
    pass
    # def Example_Rule(state: CollectionState) -> bool:
    #     # Calculated rules take a CollectionState object and return a boolean
    #     # True if the player can access the location
    #     # CollectionState is defined in BaseClasses
    #     return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data
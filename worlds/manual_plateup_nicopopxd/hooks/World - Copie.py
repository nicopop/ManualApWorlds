# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule
from ..Data import load_data_file
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation
from BaseClasses import ItemClassification

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

import logging
from copy import copy

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
        PPMiscData['version'] = "Unknown"
        PPMiscData['043Compatible'] = False

        if 'version' in game_table:
            PPMiscData['version'] = game_table['version']

        if hasattr(multiworld, 'clear_location_cache') and callable(multiworld.clear_location_cache):
            PPMiscData['043Compatible'] = True

        logger.info(f"player(s) uses {world.game} version: {PPMiscData['version']}")

    multiworld.game_version[player].value = PPMiscData["version"]
#Init Options
#region
    PPMiscData["KnownPlayers"].append(player)
    PPOptions[player] = {}
    PPMiscData[player] = {}
    PPMiscData[player]['name'] = multiworld.get_player_name(player)
    PPOptions[player]['host_level'] = get_option_value(multiworld, player, "host_level") or 0
    PPOptions[player]['win_percent'] = get_option_value(multiworld, player, "win_percent") or 0
    PPOptions[player]['do_overtime'] = get_option_value(multiworld, player, "do_overtime") or 0
    PPOptions[player]['recipe_steak'] = get_option_value(multiworld, player, 'recipe_steak') or 0
    PPOptions[player]['recipe_salad'] = get_option_value(multiworld, player, 'recipe_salad') or 0
    PPOptions[player]['recipe_pizza'] = get_option_value(multiworld, player, 'recipe_pizza') or 0
    PPOptions[player]['recipe_dumplings'] = get_option_value(multiworld, player, 'recipe_dumplings') or 0
    PPOptions[player]['recipe_coffee'] = get_option_value(multiworld, player, 'recipe_coffee') or 0
    PPOptions[player]['recipe_burger'] = get_option_value(multiworld, player, 'recipe_burger') or 0
    PPOptions[player]['recipe_turkey'] = get_option_value(multiworld, player, 'recipe_turkey') or 0
    PPOptions[player]['recipe_pie'] = get_option_value(multiworld, player, 'recipe_pie') or 0
    PPOptions[player]['recipe_cakes'] = get_option_value(multiworld, player, 'recipe_cakes') or 0
    PPOptions[player]['recipe_fish'] = get_option_value(multiworld, player, 'recipe_fish') or 0
    PPOptions[player]['recipe_hotdog'] = get_option_value(multiworld, player, 'recipe_hotdog') or 0
    PPOptions[player]['recipe_breakfast'] = get_option_value(multiworld, player, 'recipe_breakfast') or 0
    PPOptions[player]['recipe_stirfry'] = get_option_value(multiworld, player, 'recipe_stirfry') or 0
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
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_steak'] != PPOptions[last_player]['recipe_steak']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_salad'] != PPOptions[last_player]['recipe_salad']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_pizza'] != PPOptions[last_player]['recipe_pizza']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_dumplings'] != PPOptions[last_player]['recipe_dumplings']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_coffee'] != PPOptions[last_player]['recipe_coffee']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_burger'] != PPOptions[last_player]['recipe_burger']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_turkey'] != PPOptions[last_player]['recipe_turkey']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_pie'] != PPOptions[last_player]['recipe_pie']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_cakes'] != PPOptions[last_player]['recipe_cakes']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_fish'] != PPOptions[last_player]['recipe_fish']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_hotdog'] != PPOptions[last_player]['recipe_hotdog']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_breakfast'] != PPOptions[last_player]['recipe_breakfast']:
            PPMiscData[player]['SafeGen'] = False
        elif PPOptions[player]['recipe_stirfry'] != PPOptions[last_player]['recipe_stirfry']:
            PPMiscData[player]['SafeGen'] = False
        logger.debug(f"SafeGen for player {PPMiscData[player]['name']} set to {PPMiscData[player]['SafeGen']}")
#endregion
# Called after regions and locations are created, in case you want to see or modify that information.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    #print(f"after_create_regions {player}")
    extra_data = load_data_file("extra.json")
# Removing disabled Items/locations
#region

    items_to_be_removed = []
    locations_to_be_removed = []
    local = copy(world.item_name_to_item)
    localid = copy(world.item_id_to_name)
    localname = copy(world.item_name_to_id)
# First we get what items and locations to remove
    def FindRecipeLoc(recipe: str) -> []:
        found = extra_data.get(recipe, {}).get("locations", [])
        if not found:
            recipe = recipe.split('_')[-1]

            for location in world.location_name_to_location.keys():
                if location.lower().replace(' ', '').startswith(recipe):
                    found.append(location)
                if len(found) >= 6:
                    break

        return found

    def FindRecipeItems(recipe: str) -> []:
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

    for option, enabled in PPOptions[player].items():
        if option.startswith('recipe_') and not enabled:
            items_to_be_removed += FindRecipeItems(option)
            locations_to_be_removed += FindRecipeLoc(option)

    for i in range(PPOptions[player]['host_level'] + 1, 16):
        items_to_be_removed += extra_data.get(f"level_{i}", {}).get(f"items", [])
        locations_to_be_removed += extra_data.get(f"level_{i}", {}).get(f"locations", [])

    if PPOptions[player]['do_overtime'] == False:
        for location in world.location_name_to_location.keys():
            if '- Overtime' in location:
                locations_to_be_removed.append(location)
        items_to_be_removed += extra_data.get('overtime', {}).get(f"items", [])
        #locations_to_be_removed += extra_data.get('overtime', {}).get('locations', [])

# Then we remove items in items_to_be_removed
#region
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

# Removing disabled Locations
#region
    if len(locations_to_be_removed) > 0:
        for region in multiworld.regions:
            if region.player != player:
                continue
            for location in list(region.locations):
                if location.name in locations_to_be_removed:
                    region.locations.remove(location)
        if PPMiscData['043Compatible']:
            multiworld.clear_location_cache()
#endregion
    pass

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    #print(f"before_set_rules {player}")
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    #print(f"after_set_rules {player}")

    minWin = max(round(PPMiscData[player]["RecipeCount"]*(PPOptions[player]['win_percent']/100)), 2)
    PPMiscData[player]["MinWin"] = minWin

    for location in multiworld.get_unfilled_locations(player):
        if location.name == "All done":
            set_rule(location,
                     lambda state: state.has("Victory Token", player, minWin))
            break
    pass
# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def before_generate_basic(item_pool: list, world: World, multiworld: MultiWorld, player: int):
    host_level = PPOptions[player]["host_level"]
# Personnal Item counts adjustment
#region
    #maxWin = round(PPMiscData[player]["RecipeCount"]*(PPOptions[player]['win_percent']/100))

    item_counts= {}
    location_count = len(multiworld.get_unfilled_locations(player)) - 1
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
                if len(item_pool) < location_count:
                    filler = ManualItem(game_table["filler_item_name"], ItemClassification.filler, #needed since filter are added before this.
                                        world.item_name_to_id[game_table["filler_item_name"]], player)
                    item_pool.append(filler)

#endregion
# Displaying item/location info
#region
    filler = 0
    for item in item_pool:
        if item.classification == ItemClassification.filler or item.classification == ItemClassification.trap:
            filler += 1
    logger.info(f"{world.game}:{PPMiscData[player]['name']}({player}):(lvl {host_level}) {len(item_pool) - filler} items | {location_count - 1} locations")
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
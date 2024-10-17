# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation
from ..Game import game_name
from ..Helpers import clamp, load_data_file

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table, category_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, get_items_with_value

from .Options import Goal

import logging
import math

logger = logging.getLogger()
APMiscData = {}
"""Miscellaneous shared data"""
APMiscData["KnownPlayers"] = []
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



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    if not hasattr(world, 'options'):
        raise Exception("Sorry I no longer support AP before the Options Manager")
    # Set version in yaml and log
    if not APMiscData.get('version'):
        APMiscData['version'] = "Unknown"

        if 'version' in game_table:
            APMiscData['version'] = game_table['version']

        logger.info(f"player(s) uses {world.game} version: {APMiscData['version']}")

    APMiscData['is_regen'] = hasattr(multiworld, "re_gen_passthrough")
    APMiscData['is_fake'] = hasattr(multiworld, "generation_is_fake")

    world.options.game_version.value = APMiscData["version"]
#Init Options
#region
    APMiscData["KnownPlayers"].append(player)
    APMiscData[player] = {}
    APMiscData[player]['name'] = multiworld.get_player_name(player)

    #Options Check for impossibilities
    for i in range(world.options.host_level.value + 1, 16):
        recipes = world.item_name_groups.get(f"level_{i:02d}", [])
        #recipes = extra_data.get("Options").get(f"level_{i}", [])
        for recipe in recipes:
            if not recipe.lower().endswith("recipe"):
                continue
            recipe = "recipe_" + recipe.lower().rstrip("recipe").replace(' ', '')
            # option_name = f"recipe_{recipe}"
            if world.options.__dict__.get(recipe, {}):
                world.options.__dict__[recipe].value = 0
                logger.debug(f"Set player {player}'s {recipe} option's value to 0 because its for a higher lvl than host_level({world.options.host_level.value})")

    if not hasattr(world, "valid_recipes"):
        world.valid_recipes = {}
        world.required_tokens = -1
    if APMiscData['is_regen']:
        data = multiworld.re_gen_passthrough.get(game_name,{}).get(player, {"valid_recipes": {}, "required_tokens": -1})
        world.valid_recipes = data["valid_recipes"]
        world.required_tokens = data["required_tokens"]

    if not world.valid_recipes:
        world.valid_recipes = {r.replace("recipe_", "").replace(' ', '').lower(): value.value for r, value in world.options.__dict__.items() if r.startswith("recipe_")}
        for i in range(1, 11):
            if i <= world.options.more_recipes.value:
                world.valid_recipes[f"extra{i:02d}"] = 1
            else:
                world.valid_recipes[f"extra{i:02d}"] = 0

        world.enabled_recipes = [r for r, value in world.valid_recipes.items() if value]

        if world.required_tokens == -1:
            world.required_tokens = int(len(world.enabled_recipes))
            if world.options.goal == Goal.option_random_recipes_quota:
                world.required_tokens = max(math.ceil(len(world.enabled_recipes)*(world.options.win_percent.value * 0.01)), 2)
                if not APMiscData['is_fake']:
                    toRoll = len(world.enabled_recipes) - world.required_tokens
                    shuffle = list(world.enabled_recipes)
                    world.random.shuffle(shuffle)
                    for _ in range(toRoll):
                        world.valid_recipes[shuffle.pop()] = False


    # if world.options.goal == Goal.option_randomly_placed_tokens or world.options.goal == Goal.option_chaos_mcguffin:
    #     APMiscData[player]["win_tokens"] = max(math.ceil(APMiscData[player]["win_tokens"]*(world.options.win_percent.value * 0.01)), 2)

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

    # if world.hasOptionsManager:
    #     DisabledRecipe = [name for name, option in world.options.__dict__.items() if name.startswith('recipe_') and not option.value]
    #     for option in DisabledRecipe:
    #         APWorkingData['items_to_be_removed'][player].extend(FindRecipeItems(option))
    #         # locationNamesToRemove += FindRecipeLoc(option)
    #         pass

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
    item_counts= {}
    location_count = len(multiworld.get_unfilled_locations(player))
    totalRecipes = world.required_tokens
    host_level = world.options.host_level.value
    goal = world.options.goal
    if goal == Goal.option_random_recipes_quota:
        pass
    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.
    for item in APWorkingData["items_to_be_removed"].get(player, []):
        item_counts[item] = 0

    tokenType = "Chaos Token" if goal == Goal.option_chaos_mcguffin else "Victory Token"
    non_Token_items_count = len(item_pool) - next(iter(filter(lambda c: c["name"] == tokenType, item_table)))["count"]
    loc_left = len(multiworld.get_unfilled_locations(player)) - non_Token_items_count

    if tokenType == "Chaos Token":
        item_counts["Chaos Token"] = min(loc_left, clamp(totalRecipes * 2, 4 , 60))
        item_counts["Victory Token"] = 0
    else:
        item_counts["Chaos Token"] = 0
        item_counts["Victory Token"] = clamp(totalRecipes, 2, 30)
    if loc_left < item_counts[tokenType]:
        raise Exception(f"Before even creating filler items there's is not enough locations left for the Victory tokens. {item_counts['Victory Token'] - loc_left} location(s) missing \nTry enabling more recipes")
    world.required_tokens = item_counts[tokenType]

    counts = {}
    removeMe = []
    for item in item_pool:
        if item.name in item_counts.keys():
            if not item.name in counts.keys():
                counts[item.name] = 0
            counts[item.name] += 1
            if counts[item.name] > item_counts[item.name]:
                removeMe.append(item)

    for item in removeMe:
        item_pool.remove(item)
    removeMe.clear()

    # for itemName in itemNamesToRemove:
    #     item = next(i for i in item_pool if i.name == itemName)
    #     item_pool.remove(item)

    logger.info(f"{world.game}:{APMiscData[player]['name']}({player}):(lvl {host_level})(Goal: {goal.current_option_name})(Recipes: {len(world.enabled_recipes)}) {len(item_pool)} items | {location_count} locations")

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location
    token_required = world.required_tokens
    goal = world.options.goal
    if goal == Goal.option_quota or goal == Goal.option_randomly_placed_tokens or goal == Goal.option_chaos_mcguffin:
        token_name = "Victory Token"
        token_required = max(math.ceil(token_required*(world.options.win_percent.value * 0.01)), 2)
        if goal == Goal.option_chaos_mcguffin:
            token_name = "Chaos Token"
            token_required = min(token_required * 2, 60)
        Goals = [x['name'] for x in location_table if x.get('victory',False)]
        for location in multiworld.get_locations(player):
            if location.name in Goals:
                set_rule(location,
                        lambda state: state.has(token_name, player, token_required))
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
    # if not hasattr(world, "item_counts"):
    #     world.item_counts = {}
    # world.item_counts[player] = slot_data.get("item_counts", {})
    # slot_data["item_counts"] = world.item_counts[player]
    slot_data["valid_recipes"] = world.valid_recipes
    slot_data["required_tokens"] = world.required_tokens
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass

# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from ..Data import load_data_file
from copy import copy

from BaseClasses import MultiWorld, CollectionState
import logging

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation
from .Helpers import InitCategories

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table
from .Options import EarlyLaunchCode, RandomContent, Goal

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, is_item_enabled, get_option_value

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



# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    if hasattr(world, 'options'):
        world.hasOptionsManager = True
    else:
        raise Exception("Sorry I no longer support AP before the Options Manager")
    # Set version in yaml and log
    if not APMiscData.get('version'):
        APMiscData['version'] = "Unknown"
        APMiscData['043Compatible'] = False

        if 'version' in game_table:
            APMiscData['version'] = game_table['version']

        if hasattr(multiworld, 'clear_location_cache') and callable(multiworld.clear_location_cache):
            APMiscData['043Compatible'] = True

        logger.info(f"player(s) uses {world.game} version: {APMiscData['version']}")

    world.options.game_version.value = APMiscData["version"]
#Init Options
#region
    APMiscData["KnownPlayers"].append(player)
    APMiscData[player] = {}

    #Options Check for impossibilities
    if world.options.randomized_content.value == RandomContent.option_base_game:
        world.options.require_prisoner.value = 0
        goal = world.options.goal
        if goal == Goal.option_prisoner: goal.value = Goal.default #impossible option
        elif goal == Goal.option_visit_all_archive: goal.value = Goal.default #impossible option
        elif goal == Goal.option_stuck_in_stranger: goal.value = Goal.default #impossible option
        elif goal == Goal.option_stuck_in_dream: goal.value = Goal.default #impossible option
        world.options.enable_spooks.value = 1 #Set to True to skip some code later
        world.options.dlc_access_items.value = 0

    # #Is it safe to skip some code
    # APMiscData[player]["SafeGen"] = False #value for first run
    # index = APMiscData["KnownPlayers"].index(player)
    # if index > 0:
    #     index = APMiscData["KnownPlayers"][index - 1]
    #     LastOptions = multiworld.worlds[index].options
    #     CurOptions = world.options
    #     APMiscData[player]["SafeGen"] = True
    #     if CurOptions.randomized_content.value != LastOptions.randomized_content.value:
    #         APMiscData[player]["SafeGen"] = False
    #     elif CurOptions.do_place_item_category.value != LastOptions.do_place_item_category:
    #         APMiscData[player]["SafeGen"] = False
    #     elif CurOptions.goal.value != LastOptions.goal.value:
    #         APMiscData[player]["SafeGen"] = False
    #     logger.debug(f'SafeGen for player {player} set to {APMiscData[player]["SafeGen"]}')

    InitCategories(multiworld, player)
#endregion

# Called after regions and locations are created, in case you want to see or modify that information.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    solanum = world.options.require_solanum.value
    owlguy = world.options.require_prisoner.value
    randomContent = world.options.randomized_content.value
    goal = world.options.goal.value

# Removing items/locations
#region
    locations_to_be_removed = []

    # Selecting what content to remove
    #region
    if not APWorkingData.get('items_to_be_removed'):
        APWorkingData["items_to_be_removed"] = {}
    APWorkingData['items_to_be_removed'][player] = []
    if randomContent != RandomContent.option_both:
        if randomContent == RandomContent.option_base_game:
            message = "Base game"
        elif randomContent == RandomContent.option_dlc:
            message = "DLC"
            if goal == Goal.option_eye:
                message += " + Eye"
            elif goal == Goal.option_ash_twin_project_break_spacetime:
                message += " + Ash Twin project"
            elif goal == Goal.option_high_energy_lab_break_spacetime:
                message += " + High Energy Lab"
            elif goal == Goal.option_stuck_in_stranger or goal == Goal.option_stuck_in_dream:
                message += " + Adv. warp core"
            elif goal == Goal.option_stuck_with_solanum:
                message += " + Adv. warp core + Solanum"
            if solanum and goal != Goal.option_stuck_with_solanum:
                message += " + Solanum"

            # for item in list(world.item_name_to_item):
            #     if item not in valid_items:
            #         APWorkingData['items_to_be_removed'][player].append(item)

            # for location in list(world.location_name_to_location):
            #     if location not in valid_locations:
            #         locations_to_be_removed.append(location)

    else:
        message = "Both"
    #logger.info(message)
    APMiscData[player]['contentmsg'] = message
    if goal != Goal.option_stuck_with_solanum:
        locations_to_be_removed.append("FINAL > Get the Adv. warp core and get stuck with Solanum on the Quantum Moon")
    if goal != Goal.option_stuck_in_stranger:
        locations_to_be_removed.append("FINAL > Get the Adv. warp core to the Stranger and wait until Credits")
    if goal != Goal.option_stuck_in_dream:
        locations_to_be_removed.append("FINAL > Get the Adv. warp core to the Stranger and die to get in the dreamworld")
    if (goal != Goal.option_eye and not (goal == Goal.option_standard and randomContent != RandomContent.option_dlc)):
        locations_to_be_removed.append("FINAL > Get the Adv. warp core to the vessel and Warp to the Eye")
    if goal != Goal.option_ash_twin_project_break_spacetime:
        locations_to_be_removed.append('FINAL > Break Space-Time in the Ash Twin Project')
    if goal == Goal.option_ash_twin_project_break_spacetime:
        locations_to_be_removed.append('1 - Break Space-Time in the Ash Twin Project')
    if goal != Goal.option_high_energy_lab_break_spacetime:
        locations_to_be_removed.append('FINAL > Break space time in the lab')
    if goal == Goal.option_ash_twin_project_break_spacetime:
        locations_to_be_removed.append('1 - Break space time in the lab')
    if goal != Goal.option_visit_all_archive:
        locations_to_be_removed.append('FINAL > In a loop visit all 3 archive without getting caught')
    if goal == Goal.option_visit_all_archive:
        locations_to_be_removed.append('9 - In a loop visit all 3 archive without getting caught')
    #endregion

    #Removing Locations
    #region

    if len(locations_to_be_removed) > 0:
        for region in multiworld.regions:
            if region.player != player:
                continue
            for location in list(region.locations):
                if location.name in locations_to_be_removed:
                    region.locations.remove(location)
        if APMiscData['043Compatible']:
            multiworld.clear_location_cache()

    #endregion
#endregion
    pass

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    solanum = world.options.require_solanum
    owlguy = world.options.require_prisoner
    do_place_item_category = world.options.do_place_item_category
    randomContent = world.options.randomized_content
    goal = world.options.goal
    do_spooks = world.options.enable_spooks
    DlcMainItemsRequired = world.options.dlc_access_items

# Early Launch Codes
#region
    early_launch = world.options.early_launch_codes.value
    if early_launch == EarlyLaunchCode.option_anywhere:
        world.options.local_items.value.discard("Launch Codes")
        multiworld.early_items[player].pop("Launch Codes", "")
    elif early_launch == EarlyLaunchCode.option_startswith:
        world.options.local_items.value.discard("Launch Codes")
        multiworld.early_items[player].pop("Launch Codes", "")
        world.options.start_inventory["Launch Codes"] = 1
    elif early_launch == EarlyLaunchCode.option_global:
        world.options.local_items.value.discard("Launch Codes")
#endregion
# Personal Item counts adjustment
#region
    location_count = len(multiworld.get_unfilled_locations(player)) - 1
    item_counts= {}
    if randomContent == RandomContent.option_base_game:
        item_counts["Forced Meditation"] = 2
        item_counts["Musical Instrument"] = 6
        item_counts["Ticket for (1) free death"] = 4

    elif randomContent == RandomContent.option_dlc:
        item_counts["Forced Meditation"] = 3
        item_counts["Ticket for (1) free death"] = 5

    else:
        pass
    #if randomContent == RandomContent.option_base_game or randomContent == RandomContent.option_dlc:
        #if either only base game or only dlc
        #world.item_name_to_item["Ticket for (1) free death"]["count"] = 10

    if not do_spooks:
        item_counts['Visited Starlit Cove Archive'] = 1
        item_counts['Visited Endless Canyon Archive'] = 1

    for item in APWorkingData['items_to_be_removed'][player]:
        item_counts[item] = 0

    for name, count in item_counts.items():
        items = []
        for item in item_pool:
            if item.player != player:
                continue
            if item.name == name:
                items.append(item)
        if len(items) > count:
            for x in range(len(items) - count):
                item_pool.remove(items[x])
#endregion
#Placing Victory item in location
#region
    VictoryInfoToAdd = ""
    if solanum: VictoryInfoToAdd += " + 'Seen Solanum'"
    if owlguy: VictoryInfoToAdd += " + 'Seen Prisoner'"

    if goal == Goal.option_eye or (goal == Goal.option_standard and ( randomContent == RandomContent.option_both or randomContent == RandomContent.option_base_game)):
        victory_name = "FINAL > Get the Adv. warp core to the vessel and Warp to the Eye"
        victory_base_message = "Eye"
    elif goal == Goal.option_prisoner or (goal == Goal.option_standard and randomContent == RandomContent.option_dlc):
        victory_name = "94 - Communicate with the prisoner in the Subterranean Lake Dream"
        victory_base_message = "Prisoner"
    elif goal == Goal.option_visit_all_archive:
        victory_name = "FINAL > In a loop visit all 3 archive without getting caught"
        victory_base_message = "Visit all archive"
    elif goal == Goal.option_ash_twin_project_break_spacetime:
        victory_name = "FINAL > Break Space-Time in the Ash Twin Project"
        victory_base_message = "Ash Twin Project"
    elif goal == Goal.option_high_energy_lab_break_spacetime:
        victory_name = "FINAL > Break space time in the lab"
        victory_base_message = "High Energy Lab"
    elif goal == Goal.option_stuck_with_solanum:
        victory_name = "FINAL > Get the Adv. warp core and get stuck with Solanum on the Quantum Moon"
        victory_base_message = "Stuck with Solanum"
    elif goal == Goal.option_stuck_in_stranger:
        victory_name = "FINAL > Get the Adv. warp core to the Stranger and wait until Credits"
        victory_base_message = "Stuck in Stranger"
    elif goal == Goal.option_stuck_in_dream:
        victory_name = "FINAL > Get the Adv. warp core to the Stranger and die to get in the dreamworld"
        victory_base_message = "Stuck in Dreamworld"
    victory_message = victory_base_message + VictoryInfoToAdd

    for item in item_pool:
        if item.player != player:
            continue
        if item.name == "Victory Token":
            victory_item = item
            break
    for location in multiworld.get_unfilled_locations(player):
        if location.name == victory_name:
            location.place_locked_item(victory_item)
    item_pool.remove(victory_item)

    contentmsg = APMiscData[player]['contentmsg']
    logger.info(f"{world.game}:{multiworld.get_player_name(player)} ({player}):({contentmsg}) {len(item_pool)} items | {location_count} locations")
    logger.info(f'Set Victory rules to {victory_message}')
#endregion

    if len(APWorkingData.get('RM_place_item_cat', ["tomato"])) == 0:
        APWorkingData.pop("RM_place_item_cat", "")
    if len(APWorkingData.get('RM_place_item', ["tomato"])) == 0:
        APWorkingData.pop("RM_place_item", "")
    return item_pool

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    #extra_data = load_data_file("extra.json")
    solanum = world.options.require_solanum.value
    owlguy = world.options.require_prisoner.value
    randomContent = world.options.randomized_content.value
    goal = world.options.goal.value

#Victory Location access rules mod
#region

    if goal == Goal.option_eye or (goal == Goal.option_standard and ( randomContent == RandomContent.option_both or randomContent == RandomContent.option_base_game)):
        victory_name = "FINAL > Get the Adv. warp core to the vessel and Warp to the Eye"
    elif goal == Goal.option_prisoner or (goal == Goal.option_standard and randomContent == RandomContent.option_dlc):
        victory_name = "94 - Communicate with the prisoner in the Subterranean Lake Dream"
    elif goal == Goal.option_visit_all_archive:
        victory_name = "FINAL > In a loop visit all 3 archive without getting caught"
    elif goal == Goal.option_ash_twin_project_break_spacetime:
        victory_name = "FINAL > Break Space-Time in the Ash Twin Project"
    elif goal == Goal.option_high_energy_lab_break_spacetime:
        victory_name = "FINAL > Break space time in the lab"
    elif goal == Goal.option_stuck_with_solanum:
        victory_name = "FINAL > Get the Adv. warp core and get stuck with Solanum on the Quantum Moon"
    elif goal == Goal.option_stuck_in_stranger:
        victory_name = "FINAL > Get the Adv. warp core to the Stranger and wait until Credits"
    elif goal == Goal.option_stuck_in_dream:
        victory_name = "FINAL > Get the Adv. warp core to the Stranger and die to get in the dreamworld"

    for location in multiworld.get_unfilled_locations(player):
        if location.name == victory_name:
            if solanum:
                add_rule(location,
                         lambda state: state.has("Seen Solanum", player))
            if owlguy:
                add_rule(location,
                         lambda state: state.has("Seen Prisoner", player))
#endregion
# Add Stranger if required
#region
    # def _add_region_rule(region, item: str):
    #     for entrance in region.entrances:
    #         add_rule(entrance,
    #             lambda state: state.has(item, player))
    # if world.options.dlc_access_items.value:
    #     for region in multiworld.regions:
    #         if region.name == "The Stranger":
    #             _add_region_rule(region, "Stranger Access")
    #         elif (region.name == "DreamWorld General" or region.name == "Shrouded Woodlands" or region.name == "Starlit Cove"
    #               or region.name == "Endless Canyon" or region.name == "Subterranean Lake"):
    #             _add_region_rule(region, "DreamWorld Access")
#endregion
# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it


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

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
# #Restore location placed items
# #region
#     if APMiscData["KnownPlayers"][0] != player and APMiscData[player]["SafeGen"] == False:
#         RemovedPlacedItems = APWorkingData.get('RM_place_item', {})
#         RemovedPlacedItemsCategory = APWorkingData.get('RM_place_item_cat', {})
#         if RemovedPlacedItems or RemovedPlacedItemsCategory:
#             reAdded_place_item_Count = 0
#             locations_to_check = {}
#             locations_to_check.update(RemovedPlacedItems)
#             locations_to_check.update(RemovedPlacedItemsCategory)
#             for location in locations_to_check:
#                 if location in world.location_names:
#                     worldlocation = world.location_name_to_location[location]
#                     if location in RemovedPlacedItemsCategory:
#                         worldlocation["place_item_category"] = RemovedPlacedItemsCategory[location]
#                         APWorkingData['RM_place_item_cat'].pop(location)
#                     if location in RemovedPlacedItems:
#                         worldlocation["place_item"] = RemovedPlacedItems[location]
#                         APWorkingData['RM_place_item'].pop(location)
#                     if "place_item" in worldlocation or "place_item_category" in worldlocation:
#                         reAdded_place_item_Count += 1
#             if reAdded_place_item_Count > 0:
#                 if APMiscData["043Compatible"]:
#                     multiworld.clear_location_cache()
#                 logger.debug(f"ReAdded placed item info to {reAdded_place_item_Count} locations.")
# #endregion
#     randomContent = world.options.randomized_content
#     if randomContent == RandomContent.option_dlc:
#         if not APMiscData[player]["SafeGen"]:
#             if not APWorkingData.get('RM_place_item_cat', {}):
#                 APWorkingData['RM_place_item_cat'] = {}
#             worldlocation = world.location_name_to_location["Get in the ship for the first time"]
#             APWorkingData['RM_place_item_cat'][worldlocation['name']] = copy(worldlocation["place_item_category"])
#             worldlocation.pop("place_item_category", "")

# # Remove place category if required
# #region
#     do_place_item_category = world.options.do_place_item_category.value
#     if not APMiscData[player]["SafeGen"]:
#         if not do_place_item_category:
#             extra_data = load_data_file("extra.json")
#             if 'RM_place_item_cat' not in APWorkingData:
#                 APWorkingData["RM_place_item_cat"] = {}
#             if 'RM_place_item' not in APWorkingData:
#                 APWorkingData["RM_place_item"] = {}
#             for location in list(extra_data["no_place_item_category"]["locations"]):
#                 if location in world.location_name_to_location:
#                     worldlocation = world.location_name_to_location[location]
#                     if "place_item_category" in worldlocation:
#                         APWorkingData['RM_place_item_cat'][location] = copy(worldlocation["place_item_category"])
#                         worldlocation.pop("place_item_category", "")
#             if APMiscData["043Compatible"]:
#                 multiworld.clear_location_cache()

# #endregion
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

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

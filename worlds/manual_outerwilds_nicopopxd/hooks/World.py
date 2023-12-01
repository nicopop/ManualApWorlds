# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from copy import copy
from difflib import SequenceMatcher

from BaseClasses import MultiWorld
import json
import os
import pkgutil
import logging

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation
from ..Regions import regionMap

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table
from .Options import RandomContent, Goal, GameLanguage, SpoilerFreeNames

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

logger = logging.getLogger()
OWMiscData = {}
"""Miscellaneous shared data"""
OWMiscData["KnownPlayers"] = []
OWOptions = {}
"""
Player options:
To access option value: OWOptions[player]["optionName"]
"""

OWWorkingData = {}
"""Contains Tracking of 'permanently' changed values to be restored as needed"""

RemovedPlacedItems = {}
RemovedPlacedItemsCategory = {}
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

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Called before regions and locations are created. Not clear why you'd want this, but it's here.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
# Set version in yaml and log
#region
    if 'version' in game_table:
        apworldversion = game_table['version']
        if apworldversion != "":
            multiworld.game_version[player].value = apworldversion
            if "version" not in OWMiscData:
                logger.info(f"player(s) uses {world.game} version: {apworldversion}")
                OWMiscData["version"] = apworldversion
        else:
            multiworld.game_version[player].value = "Unknown"
    else:
        multiworld.game_version[player].value = "Unknown"
#endregion
# init player personnal data
#region
    OWMiscData["KnownPlayers"].append(player)
    OWOptions[player] = {}
    OWOptions[player]["name"] = multiworld.get_player_name(player)
#endregion
# Add Current Options to OWOptions
#region
    OWOptions[player]["solanum"] = get_option_value(multiworld, player, "require_solanum") or 0
    OWOptions[player]["owlguy"] = get_option_value(multiworld, player, "require_prisoner") or 0
    OWOptions[player]["reducedSpooks"] = get_option_value(multiworld, player, "reduced_spooks") or 0
    OWOptions[player]["do_place_item_category"] = get_option_value(multiworld, player, "do_place_item_category") or 0
    OWOptions[player]["no_spoilers"] = get_option_value(multiworld, player, "no_spoilers") or SpoilerFreeNames.default
    OWOptions[player]["language"] = get_option_value(multiworld, player, "game_language") or GameLanguage.default
    OWOptions[player]["randomContent"] = get_option_value(multiworld, player, "randomized_content") or RandomContent.default
    OWOptions[player]["goal"] = get_option_value(multiworld, player, "goal") or Goal.default
    #Options Check for imposibities
    if OWOptions[player]["randomContent"] == RandomContent.option_base_game:
        OWOptions[player]["owlguy"] = 0
        OWOptions[player]["reducedSpooks"] = 0
        goal = OWOptions[player]["goal"]
        if goal == Goal.option_prisoner: goal = Goal.default #imposible option
        elif goal == Goal.option_visit_all_archive: goal = Goal.default #imposible option
        elif goal == Goal.option_stuck_in_stranger: goal = Goal.default #imposible option
        elif goal == Goal.option_stuck_in_dream: goal = Goal.default #imposible option
        OWOptions[player]["goal"] = goal
#endregion
# Spoiler Detection
#region
    if OWOptions[player]["no_spoilers"] == SpoilerFreeNames.option_detection:
        if 'SpoilersSafe' in OWMiscData:
            if OWMiscData["SpoilersSafe"]:
                OWOptions[player]["no_spoilers"] = SpoilerFreeNames.option_disabled
            else:
                OWOptions[player]["no_spoilers"] = SpoilerFreeNames.option_enabled
        elif 'SpoilersSafe' not in OWMiscData and multiworld.players > 1:    #Only run once
            similarities = {}
            PlayersToCheck = set([])
            players = multiworld.player_name
            for pid, name in players.items():
                if pid not in similarities:
                    similarities[pid] = {}
                    similarities[pid]["name"] = multiworld.get_player_name(pid)
                for _pid, _name in players.items():
                    if pid == _pid:
                        continue
                    elif _pid in similarities[pid]:
                        continue
                    test = similar(name, _name)
                    if test >= 0.60:
                        if _pid not in similarities:
                            similarities[_pid] = {}
                            similarities[_pid]["name"] = multiworld.get_player_name(pid)
                        similarities[pid][_pid] = multiworld.get_player_name(_pid)
                        similarities[_pid][pid] = multiworld.get_player_name(pid)
                    else:
                        PlayersToCheck.add(_pid)
            else:
                logger.info(f"Spoiler Protection: Got {len(PlayersToCheck)} players to check")
                result = False
                for _player in PlayersToCheck:
                    result = False
                    if len(similarities[_player]) == 1 and multiworld.game[_player] != multiworld.game[player]:
                        break
                    elif len(similarities[_player]) > 1:
                        for test in similarities[_player]:
                            if test.key == "name":
                                continue
                            if multiworld.game[test] == multiworld.game[player]:
                                result = True
                                if test in PlayersToCheck:
                                    PlayersToCheck.remove(test)
                                break
                        else:
                            break
                        continue
                similarities.clear()
                PlayersToCheck.clear()
                OWMiscData['SpoilersSafe'] = result
                if result:
                    OWOptions[player]["no_spoilers"] = SpoilerFreeNames.option_disabled
                else:
                    OWOptions[player]["no_spoilers"] = SpoilerFreeNames.option_enabled
#endregion
# Creating personnal Misc data
#region
    OWMiscData[player] = {}
    OWMiscData[player]["name"] = multiworld.get_player_name(player)
    OWMiscData[player]["languageKey"] = GameLanguage(OWOptions[player]["language"]).current_key.upper()
#endregion
# Compare Current option with last options
#region
    #Is it safe to skip some code
    OWMiscData[player]["SafeGen"] = False #value for first run
    index = OWMiscData["KnownPlayers"].index(player)
    if index > 0:
        index = OWMiscData["KnownPlayers"][index - 1]
        OWMiscData[player]["SafeGen"] = True
        if OWOptions[player]["randomContent"] != OWOptions[index]["randomContent"]:
            OWMiscData[player]["SafeGen"] = False
        elif OWOptions[player]["do_place_item_category"] != OWOptions[index]["do_place_item_category"]:
            OWMiscData[player]["SafeGen"] = False
        elif OWOptions[player]["goal"] != OWOptions[index]["goal"]:
            OWMiscData[player]["SafeGen"] = False
        elif OWOptions[player]["no_spoilers"] != OWOptions[index]["no_spoilers"]:
            OWMiscData[player]["SafeGen"] = False
        elif OWOptions[player]["language"] != OWOptions[index]["language"]:
            OWMiscData[player]["SafeGen"] = False
        logger.debug(f'SafeGen for player {player} set to {OWMiscData[player]["SafeGen"]}')
#endregion
# Called after regions and locations are created, in case you want to see or modify that information.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    language = str(OWMiscData[player]["languageKey"])
    removeSpoilers = SpoilerFreeNames(OWOptions[player]["no_spoilers"])
    if not OWMiscData[player]["SafeGen"]:
        #Restore first
        if "Requires" in OWWorkingData:
            if "Regions" in OWWorkingData["Requires"]:
                for name, requirement in OWWorkingData["Requires"]["Regions"].items():
                    regionMap[name]["requires"] =  requirement
                OWWorkingData["Requires"].pop("Regions")
            if "Locations" in OWWorkingData["Requires"]:
                for name, requirement in OWWorkingData["Requires"]["Locations"].items():
                    world.location_name_to_location[name]["requires"] =  requirement
                OWWorkingData["Requires"].pop("Regions")
            OWWorkingData.pop("Requires")
        if language != "EN" or removeSpoilers == SpoilerFreeNames.option_enabled:
            fname = os.path.join("..", "data", "extra.json")
            extra_data = json.loads(pkgutil.get_data(__name__, fname).decode())
            OWWorkingData["Requires"] = {}
        # Temporarily Renaming items
        #region
            itemchanged = {}
            for item in item_table:
                old_item_name = ""
                if removeSpoilers:
                    if item['name'] in extra_data["NameMapping"][language]["SpoilerFree"]["items"]:
                        old_item_name = copy(item['name'])
                        new_item_name = extra_data["NameMapping"][language]["SpoilerFree"]["items"][old_item_name]
                    elif language != "EN" and item['name'] in extra_data["NameMapping"][language]["Normal"]["items"]:
                        old_item_name = copy(item['name'])
                        new_item_name = extra_data["NameMapping"][language]["Normal"]["items"][old_item_name]
                elif item['name'] in extra_data["NameMapping"][language]["Normal"]["items"]:
                        old_item_name = copy(item['name'])
                        new_item_name = extra_data["NameMapping"][language]["Normal"]["items"][old_item_name]
                if old_item_name != "":
                    itemchanged[old_item_name] = new_item_name
            logger.debug(f"Done renaming {len(itemchanged)} items")
        #endregion
            extra_data.clear()
        #Replacing items in region requirements
        #region
            OWWorkingData['Requires']['Regions'] = {}
            for name, region in regionMap.items():
                if 'requires' in region:
                    requirement = region['requires']
                    if len(requirement) > 0:
                        if isinstance(requirement, str):
                            for old_item, new_item in itemchanged.items():
                                if requirement.find(f"|{old_item}|") != -1:
                                    logger.debug(f"replaced:|{old_item}| with |{new_item}| in region: {name}:{requirement}")
                                    if name not in OWWorkingData['Requires']['Regions']:
                                        OWWorkingData['Requires']['Regions'][name] = copy(requirement)
                                    region['requires'] = region['requires'].replace(f"|{old_item}|", f"|{new_item}|")
                        elif isinstance(requirement, list):
                            for old_item, new_item in itemchanged.items():
                                if old_item in requirement:
                                    logger.debug(f"replaced:|{old_item}| with |{new_item}| in region: {name}:{requirement}")
                                    if name not in OWWorkingData['Requires']['Regions']:
                                        OWWorkingData['Requires']['Regions'][name] = copy(requirement)
                                    listindex = region['requires'].index(old_item)
                                    region['requires'].remove(old_item)
                                    region['requires'].insert(listindex, new_item)
            logger.debug(f"Done replacing requirements of {len(OWWorkingData['Requires']['Regions'])} Regions")
            if len(OWWorkingData['Requires']['Regions']) == 0:
                OWWorkingData['Requires'].pop('Regions')
        #endregion
        # Replaceing items in location requirements
        #region
            OWWorkingData['Requires']['Locations'] = {}
            for location in world.location_name_to_location.values():
                if 'requires' in location and location['name'] != "__Manual Game Complete__":
                    requirement = location['requires']
                    if len(requirement) > 0:
                        if isinstance(requirement, str):
                            for new_item, old_item in itemchanged.items():
                                if requirement.find(f"|{old_item}|") != -1:
                                    logger.debug(f"replaced:|{old_item}| with |{new_item}| in : {location['name']}:{requirement}")
                                    if location['name'] not in OWWorkingData['Requires']['Locations']:
                                        OWWorkingData['Requires']['Locations'][location['name']] = copy(requirement)
                                    location['requires'] = location['requires'].replace(f"|{old_item}|", f"|{new_item}|")
                        elif isinstance(requirement, list):
                            for new_item, old_item in itemchanged.items():
                                if old_item in requirement:
                                    logger.debug(f"replaced:|{old_item}| with |{new_item}| in : {location['name']}:{requirement}")
                                    if location['name'] not in OWWorkingData['Requires']['Locations']:
                                        OWWorkingData['Requires']['Locations'][location['name']] = copy(requirement)
                                    listindex = location['requires'].index(old_item)
                                    location['requires'].remove(old_item)
                                    location['requires'].insert(listindex, new_item)
            logger.debug(f"Done replacing requirements of {len(OWWorkingData['Requires']['Locations'])} locations")
            if len(OWWorkingData['Requires']['Locations']) == 0:
                OWWorkingData['Requires'].pop('Locations')
        #endregion
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    solanum = OWOptions[player]["solanum"]
    owlguy = OWOptions[player]["owlguy"]
    randomContent = OWOptions[player]["randomContent"]
    goal = OWOptions[player]["goal"]
    language = OWMiscData[player]["languageKey"]
    removeSpoilers = OWOptions[player]["no_spoilers"]

    fname = os.path.join("..", "data", "extra.json")
    extra_data = json.loads(pkgutil.get_data(__name__, fname).decode())
#Victory Location access rules mod
#region

    if goal == Goal.option_eye or (goal == Goal.option_standard and ( randomContent == RandomContent.option_both or randomContent == RandomContent.option_base_game)):
        victory_name = "FINAL > Get the Adv. warp core to the vessel and Warp to the Eye"
    elif goal == Goal.option_prisoner or (goal == Goal.option_standard and randomContent == RandomContent.option_dlc):
        victory_name = "94 - Communicate with the prisoner in the Subterranean Lake Dream"
    elif goal == Goal.option_visit_all_archive:
        victory_name = "9 - In a loop visit all 3 archive without getting caught"
    elif goal == Goal.option_ash_twin_project_break_spacetime:
        victory_name = "1 - Break Space-Time in the Ash Twin Project"
    elif goal == Goal.option_high_energy_lab_break_spacetime:
        victory_name = "1 - Break space time in the lab"
    elif goal == Goal.option_stuck_with_solanum:
        victory_name = "FINAL > Get the Adv. warp core and get stuck with Solanum on the Quantum Moon"
    elif goal == Goal.option_stuck_in_stranger:
        victory_name = "FINAL > Get the Adv. warp core to the Stranger and wait until Credits"
    elif goal == Goal.option_stuck_in_dream:
        victory_name = "FINAL > Get the Adv. warp core to the Stranger and die to get in the dreamworld"

    for location in multiworld.get_unfilled_locations(player):
        if location.name == victory_name:
            if solanum:
                name = "Seen Solanum"
                if removeSpoilers and name in extra_data["NameMapping"][language]["SpoilerFree"]["items"]:
                    name = extra_data["NameMapping"][language]["SpoilerFree"]["items"][name]
                elif name in extra_data["NameMapping"][language]["Normal"]["items"]:
                    name = extra_data["NameMapping"][language]["Normal"]["items"][name]
                add_rule(location,
                            lambda state: state.has(name, player))
            if owlguy:
                name = "Seen Prisoner"
                if removeSpoilers and name in extra_data["NameMapping"][language]["SpoilerFree"]["items"]:
                    name = extra_data["NameMapping"][language]["SpoilerFree"]["items"][name]
                elif name in extra_data["NameMapping"][language]["Normal"]["items"]:
                    name = extra_data["NameMapping"][language]["Normal"]["items"][name]
                add_rule(location,
                            lambda state: state.has(name, player))
            break
#endregion

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def before_generate_basic(item_pool: list, world: World, multiworld: MultiWorld, player: int):
    solanum = OWOptions[player]["solanum"]
    owlguy = OWOptions[player]["owlguy"]
    reducedSpooks = OWOptions[player]["reducedSpooks"]
    do_place_item_category = OWOptions[player]["do_place_item_category"]
    randomContent = OWOptions[player]["randomContent"]
    goal = OWOptions[player]["goal"]

#Restore location placed items
#region
    if OWMiscData["KnownPlayers"][0] != player and OWMiscData[player]["SafeGen"] == False:
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
                logger.debug(f"ReAdded placed item info to {readded_place_item_Count} locations.")
#endregion

# Personnal Item counts adjustment
#region
    item_counts= {}
    if randomContent == RandomContent.option_base_game:
        item_counts["forced Meditation"] = 2
        item_counts["Musical Instrument"] = 6
        item_counts["Ticket for (1) free death"] = 4

    elif randomContent == RandomContent.option_dlc:
        worldlocation = world.location_name_to_location["Get in ship for the first time"]
        RemovedPlacedItemsCategory[worldlocation.name] = copy(worldlocation["place_item_category"])
        worldlocation.pop("place_item_category", "")

        item_counts["forced Meditation"] = 3
        item_counts["Ticket for (1) free death"] = 5
    #if randomContent == RandomContent.option_base_game or randomContent == RandomContent.option_dlc:
        #if either only base game or only dlc
        #world.item_name_to_item["Ticket for (1) free death"]["count"] = 10

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

    locations_to_be_removed = []

    if randomContent != RandomContent.option_both or reducedSpooks or not do_place_item_category :
        fname = os.path.join("..", "data", "extra.json")
        extra_data = json.loads(pkgutil.get_data(__name__, fname).decode())
        # THX Axxroy

    if not do_place_item_category:
        for location in list(extra_data["no_place_item_category"]["locations"]):
            if location in world.location_name_to_location:
                worldlocation = world.location_name_to_location[location]
                if "place_item_category" in worldlocation:
                    RemovedPlacedItemsCategory[location] = copy(worldlocation["place_item_category"])
                    worldlocation.pop("place_item_category", "")
        multiworld.clear_location_cache()


    if randomContent != RandomContent.option_both:
        if randomContent == RandomContent.option_base_game:
            message = "Base game"
            for item in list(item_pool):
                if item.name in extra_data["echoes"]["items"]:
                    item_pool.remove(item)
            locations_to_be_removed += extra_data["echoes"]["locations"]
        elif randomContent == RandomContent.option_dlc:
            message = "DLC"
            valid_items = extra_data["echoes"]["items"] + extra_data["both"]["items"]
            valid_locations = extra_data["echoes"]["locations"] + extra_data["both"]["locations"]
            if goal == Goal.option_eye:
                valid_items += extra_data["victory_eye"]["items"]
                valid_locations += extra_data["victory_eye"]["locations"]
                message += " + Eye"
            elif goal == Goal.option_ash_twin_project_break_spacetime:
                valid_items += extra_data["victory_ash_twin_project_break_spacetime"]["items"]
                valid_locations += extra_data["victory_ash_twin_project_break_spacetime"]["locations"]
                message += " + Ash Twin project"
            elif goal == Goal.option_high_energy_lab_break_spacetime:
                valid_items += extra_data["victory_high_energy_lab_break_spacetime"]["items"]
                valid_locations += extra_data["victory_high_energy_lab_break_spacetime"]["locations"]
                message += " + High Energy Lab"
            elif goal == Goal.option_stuck_in_stranger or goal == Goal.option_stuck_in_dream:
                valid_items +=  extra_data["need_warpdrive"]["items"]
                valid_locations += extra_data["need_warpdrive"]["locations"]
                message += " + Adv. warp core"
            elif goal == Goal.option_stuck_with_solanum:
                valid_items +=  extra_data["need_warpdrive"]["items"] + extra_data["require_solanum"]["items"]
                valid_locations += extra_data["need_warpdrive"]["locations"] + extra_data["require_solanum"]["locations"]
                message += " + Adv. warp core + Solanum"
            if solanum and goal != Goal.option_stuck_with_solanum:
                valid_items += extra_data["require_solanum"]["items"]
                valid_locations += extra_data["require_solanum"]["locations"]
                message += " + Solanum"

            for item in list(item_pool):
                if item.name not in valid_items:
                    item_pool.remove(item)

            for location in list(world.location_name_to_location):
                if location not in valid_locations:
                    locations_to_be_removed.append(location)

    else:
        message = "Both"
    #logger.info(message)

    if goal != Goal.option_stuck_with_solanum:
        locations_to_be_removed.append("FINAL > Get the Adv. warp core and get stuck with Solanum on the Quantum Moon")
    if goal != Goal.option_stuck_in_stranger:
        locations_to_be_removed.append("FINAL > Get the Adv. warp core to the Stranger and wait until Credits")
    if goal != Goal.option_stuck_in_dream:
        locations_to_be_removed.append("FINAL > Get the Adv. warp core to the Stranger and die to get in the dreamworld")

    if reducedSpooks:
        locations_to_be_removed += extra_data["reduce_spooks"]["locations"]
        #do stuff to reduce spook like change requires of some locations

    if (goal != Goal.option_eye and not (goal == Goal.option_standard and (randomContent != RandomContent.option_dlc))):
        locations_to_be_removed.append("FINAL > Get the Adv. warp core to the vessel and Warp to the Eye")

    local_valid_locations = copy(world.location_name_to_location)
    removedlocCount = 1 #victory included
    if len(locations_to_be_removed) > 0:
        for region in multiworld.regions:
            if region.player != player:
                continue
            for location in list(region.locations):
                if location.name in locations_to_be_removed:
                    if OWMiscData[player]["SafeGen"] == False:
                        worldlocation = world.location_name_to_location[location.name]
                        if 'place_item' in worldlocation:
                            RemovedPlacedItems[location.name] = copy(worldlocation["place_item"])
                            worldlocation.pop("place_item", "")
                        if'place_item_category' in worldlocation:
                            RemovedPlacedItemsCategory[location.name] = copy(worldlocation["place_item_category"])
                            worldlocation.pop("place_item_category", "")
                    region.locations.remove(location)
                    local_valid_locations.pop(location.name, "")
                    removedlocCount += 1
        multiworld.clear_location_cache()

    logger.info(f"{world.game}:{player}:({message}) {len(item_pool)} items | {len(world.location_names) - removedlocCount} locations")

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
        victory_name = "9 - In a loop visit all 3 archive without getting caught"
        victory_base_message = "Visit all archive"
    elif goal == Goal.option_ash_twin_project_break_spacetime:
        victory_name = "1 - Break Space-Time in the Ash Twin Project"
        victory_base_message = "Ash Twin Project"
    elif goal == Goal.option_high_energy_lab_break_spacetime:
        victory_name = "1 - Break space time in the lab"
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

    logger.info(f'Set the player {multiworld.get_player_name(player)} Victory rules to {victory_message}')
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
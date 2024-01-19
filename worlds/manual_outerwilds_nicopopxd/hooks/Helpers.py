from typing import Optional
from BaseClasses import MultiWorld
from ..Locations import ManualLocation
from ..Items import ManualItem
from ..Data import load_data_file
#from .Options import EarlyLaunchCode, RandomContent, Goal
extraData = {}

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(world: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(world: MultiWorld, player: int, item: ManualItem) -> Optional[bool]:
    return checkobject(world, player, item, 'items')

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(world: MultiWorld, player: int, location: ManualLocation) -> Optional[bool]:
    return checkobject(world, player, location, 'locations')

def checkobject(world, player, obj, objtype) -> Optional[bool]:
    if not hasattr(world, 'worlds'):
        base = world
    else:
        base = world.worlds.get(player)
    content = base.ppoptions['randomContent']
    if content == 0:
        return None
    #cant import options because of circular import soooo
    #display_name = "Randomized content"
    #option_both = 0
    #alias_everything = 0
    #option_base_game = 1
    #option_dlc = 2
    #default = 0
    # display_name = "Goal"
    # option_standard = 0
    # option_eye = 1
    # option_prisoner = 2
    # option_visit_all_archive = 3
    # option_ash_twin_project_break_spacetime = 4
    # option_high_energy_lab_break_spacetime = 5
    # option_stuck_with_solanum = 6
    # option_stuck_in_stranger = 7
    # option_stuck_in_dream = 8
    categories = obj.get('category', [])
    if categories:
        goal = base.ppoptions['goal']
        solanum = base.ppoptions['solanum']
        if content == 1 and "DLC - Eye" in categories:
            return False
        elif content == 2 and "Base Game" in categories:
            global extraData
            if not extraData:
                extraData = load_data_file("extra.json")
            if goal == 1 and obj.get('name') in extraData["victory_eye"][objtype]:
                return True
            elif goal == 4 and obj.get('name') in extraData["victory_ash_twin_project_break_spacetime"][objtype]:
                return True
            elif goal == 5 and obj.get('name') in extraData["victory_high_energy_lab_break_spacetime"][objtype]:
                return True
            elif goal == 6 and (obj.get('name') in extraData["need_warpdrive"][objtype] + extraData["require_solanum"][objtype]):
                return True
            elif (goal == 7 or goal == 8) and obj.get('name') in extraData["need_warpdrive"][objtype]:
                return True
            elif (goal != 6 and solanum)  and obj.get('name') in extraData["require_solanum"][objtype]:
                return True
            else:
                return False
    return None
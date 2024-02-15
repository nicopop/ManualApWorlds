from typing import Optional
from BaseClasses import MultiWorld
from ..Locations import ManualLocation
from ..Items import ManualItem
from ..Data import load_data_file, category_table
#from .Options import EarlyLaunchCode, RandomContent, Goal
extraData = {}
# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(world: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    if not hasattr(world, 'worlds'):
        base = world
    else:
        base = world.worlds.get(player)
    if not hasattr(base, 'categoryInit'):
        InitCategories(base, player)

    return is_category_manual_enabled(base, player, category_name)

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_any_category_enabled(world: MultiWorld, player: int, category_name: str) -> Optional[bool]:
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
    if not hasattr(base, 'categoryInit'):
        InitCategories(base, player)

    resultYes = False
    resultNo = False
    categories = obj.get('category', [])
    for category in categories:
        result = is_category_manual_enabled(base, player, category)
        if result is not None:
            if result:
                resultYes = True
                break
            else:
                resultNo = True
    if resultYes:
        return True
    elif resultNo:
        return False
    else:
        return None
    # from .Options import RandomContent, Goal #imported here because otherwise cause circular import

    # if base.hasOptionsManager:
    #     content = base.options.randomized_content.value
    # else:
    #     content = base.ppoptions['randomContent']
    # if content == RandomContent.option_both:
    #     return None
    # categories = obj.get('category', [])
    # if categories:
    #     if base.hasOptionsManager:
    #         goal = base.options.goal
    #         solanum = base.options.require_solanum
    #     else:
    #         goal = base.ppoptions['goal']
    #         solanum = base.ppoptions['solanum']
    #     if content == RandomContent.option_base_game and "DLC - Eye" in categories:
    #         return False
    #     elif content == RandomContent.option_dlc and "Base Game" in categories:
    #         global extraData
    #         if not extraData:
    #             extraData = load_data_file("extra.json")
    #         if goal == Goal.option_eye and obj.get('name') in extraData["victory_eye"][objtype]:
    #             return True
    #         elif (goal == Goal.option_ash_twin_project_break_spacetime and obj.get('name')
    #               in extraData["victory_ash_twin_project_break_spacetime"][objtype]):
    #             return True
    #         elif (goal == Goal.option_high_energy_lab_break_spacetime and obj.get('name')
    #               in extraData["victory_high_energy_lab_break_spacetime"][objtype]):
    #             return True
    #         elif ((goal == Goal.option_stuck_with_solanum or solanum)
    #               and (obj.get('name') in extraData["require_solanum"][objtype])):
    #             return True
    #         elif ((goal == Goal.option_stuck_in_stranger or goal == Goal.option_stuck_in_dream or Goal.option_stuck_with_solanum)
    #               and obj.get('name') in extraData["need_warpdrive"][objtype]):
    #             return True
    #         else:
    #             return False
    return None
def InitCategories(world: MultiWorld, player: int):
    from .Options import RandomContent, Goal #imported here because otherwise cause circular import
    if not hasattr(world, 'worlds'):
        base = world
    else:
        base = world.worlds.get(player)

    if base.hasOptionsManager:
        goal = base.options.goal.value
        solanum = base.options.require_solanum.value
        content = base.options.randomized_content.value
    else:
        goal = base.ppoptions['goal']
        solanum = base.ppoptions['solanum']
        content = base.ppoptions['randomContent']

    if content == RandomContent.option_both:
        set_category_status(base, player, 'Base Game', True)
        set_category_status(base, player, 'DLC - Eye', True)
    elif content == RandomContent.option_base_game:
        set_category_status(base, player, 'Base Game', True)
        set_category_status(base, player, 'DLC - Eye', False)
    elif content == RandomContent.option_dlc:
        set_category_status(base, player, 'Base Game', False)
        set_category_status(base, player, 'DLC - Eye', True)
        if solanum:
            set_category_status(base, player, 'require_solanum', True)

        if goal == Goal.option_eye:
            set_category_status(base, player, 'Win_Eye', True)
            set_category_status(base, player, 'need_warpdrive', True)
        elif goal == Goal.option_ash_twin_project_break_spacetime:
            set_category_status(base, player, 'need_warpdrive', True)
            set_category_status(base, player, 'Win_ATP_break_spacetime', True)
        elif goal == Goal.option_high_energy_lab_break_spacetime:
            set_category_status(base, player, 'need_warpdrive', True)
            set_category_status(base, player, 'Win_HEL_break_spacetime', True)
        elif goal == Goal.option_stuck_with_solanum:
            set_category_status(base, player, 'need_warpdrive', True)
            set_category_status(base, player, 'require_solanum', True)
            set_category_status(base, player, 'Win_solanum', True)
        elif (goal == Goal.option_stuck_in_stranger or goal == Goal.option_stuck_in_dream):
            set_category_status(base, player, 'need_warpdrive', True)
    base.categoryInit = True

def _is_manualobject_enabled(world: MultiWorld, player: int, object: any) -> bool:
    """Internal method: Check if a Manual Object has any category disabled by a yaml option.
    \nPlease use the proper is_'item/location'_enabled or is_'item/location'_name_enabled methods instead.
    """
    #from ..Helpers import is_any_category_enabled
    enabled = True
    for category in object.get("category", []):
        if not is_category_manual_enabled(world, player, category):
            enabled = False
            break

    return enabled

def is_category_manual_enabled(world, player: int, category_name: str) -> Optional[bool]:
    """Check if a category has been disabled Manually."""
    category_data = world.category_table.get(category_name, {})

    return category_data.get('enabled', {}).get(player, None)

def set_category_status(world, player: int, category_name: str, status: bool):
    if world.category_table.get(category_name, {}):
        if not world.category_table[category_name].get('enabled', {}):
            world.category_table[category_name]['enabled'] = {}
        world.category_table[category_name]['enabled'][player] = status

from typing import Optional
from BaseClasses import MultiWorld
from ..Locations import ManualLocation
from ..Items import ManualItem


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(world: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    if hasattr(world, 'worlds'):
        world = world.worlds.get(player)
    if not hasattr(world, 'categoryInit'):
        InitCategories(world, player)
    category_data = world.category_table.get(category_name, {})

    return category_data.get('enabled', {}).get(player, None)

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_any_category_enabled(world: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(world: MultiWorld, player: int, item: ManualItem) -> Optional[bool]:
    if item.get('name','').endswith('Access') and 'DLC - Eye' in item.get('category', []):
        return bool(world.worlds[player].options.dlc_access_items.value)
    return checkobject(world, player, item)

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(world: MultiWorld, player: int, location: ManualLocation) -> Optional[bool]:
    return checkobject(world, player, location)

def checkobject(world: MultiWorld, player: int, obj: object) -> Optional[bool]:
    """Check if a Manual object as any category enabled/disabled

    Args:
        world (MultiWorld): Multiworld or World it doesn't matter
        player (int): Player id
        obj (object): Manual Object to test

    Returns:
        Optional[bool]: enabled or not,
        return None if no category are enable or disabled
    """
    if hasattr(world, 'worlds'):
        world = world.worlds.get(player)
    if not hasattr(world, 'categoryInit'):
        InitCategories(world, player)

    resultYes = False
    resultNo = False
    categories = obj.get('category', [])
    for category in categories:
        result = before_is_category_enabled(world, player, category)
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
    return None

def InitCategories(world: MultiWorld, player: int):
    """Mark categories as Enabled or Disabled based on options"""
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

def set_category_status(world, player: int, category_name: str, status: bool):
    if world.category_table.get(category_name, {}):
        if not world.category_table[category_name].get('enabled', {}):
            world.category_table[category_name]['enabled'] = {}
        world.category_table[category_name]['enabled'][player] = status

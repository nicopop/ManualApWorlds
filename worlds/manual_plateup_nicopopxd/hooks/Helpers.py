from typing import Optional
from BaseClasses import MultiWorld
from ..Locations import ManualLocation
from ..Items import ManualItem


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    from .Options import Goal
    base = multiworld.worlds[player]
    if category_name.startswith('level_'):
        number = int(category_name[-2:])
        if number <= base.options.host_level.value:
            return True
        return False
    elif category_name.endswith("_tokens"):
        if base.options.goal.value == Goal.option_chaos_mcguffin:
            return category_name == "chaos_tokens"
        else:
            return category_name != "chaos_tokens"
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item: ManualItem) -> Optional[bool]:
    check = checkobject(multiworld, player, item)
    if check is None:
        base = multiworld.worlds[player]
        name = item.get('name', "")
        if name.endswith(' Recipe'):
            recipe = name.replace(' Recipe', '').replace(' ', '').lower()
            return _check_recipe(base, recipe)
    return check

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: ManualLocation) -> Optional[bool]:
    from .Options import Goal
    check = checkobject(multiworld, player, location)
    if check is None:
        name = location.get('name', "")
        if "inGame" not in location.get('category', []):
            return check
        recipe = name.split('-')[0].replace(" ", "").lower()
        world = multiworld.worlds[player]

        if recipe not in world.valid_recipes.keys():
            raise Exception(f"{recipe} is not a known recipe. Probably missing its '{recipe} recipe' item in item.json")
        #if its a recipe location
        if world.options.goal.value == Goal.option_random_recipes_quota:
            result = _check_recipe(world, recipe)
            if result is None:
                if "no_token" in location.get('category', []) or "has_token" in location.get('category', []):
                    has_token = "has_token" in location.get('category', [])
                    if world.valid_recipes.get(recipe, False):
                        return has_token
                    else:
                        return not has_token
        elif world.options.goal == Goal.option_randomly_placed_tokens:
            if "has_token" in location.get('category', []):
                return False
        else:
            if "no_token" in location.get('category', []):
                return False
        return _check_recipe(world, recipe)
    return check

def _check_recipe(base, recipe: str) -> Optional[bool]:
    if recipe.startswith('extra'):
        more_recipes = base.options.more_recipes.value
        if not more_recipes:
            return False
        number = int(recipe[-2:])
        if number > more_recipes:
            return False
        return None
    Object = lambda **kwargs: type("Object", (), kwargs)
    option = base.options.__dict__.get(f"recipe_{recipe}", Object(value = None))
    if option.value == 0:
        return False
    return None

def set_category_status(world, player: int, category_name: str, status: bool):
    if not hasattr(world, "has_category_status"):
        world.has_category_status = True
    if world.category_table.get(category_name, {}):
        if not world.category_table[category_name].get('enabled', {}):
            world.category_table[category_name]['enabled'] = {}
        world.category_table[category_name]['enabled'][player] = status

def set_object_status(player: int, obj: object, status: bool):
    if not obj.get("enabled"):
        obj["enabled"] = {}
    obj["enabled"][player] = status

def get_category_status(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    category_data = multiworld.worlds.get(player).category_table.get(category_name, {})

    return category_data.get('enabled', {}).get(player, None)

def checkobject(multiworld: MultiWorld, player: int, obj: object) -> Optional[bool]:
    """Check if a Manual object as any category enabled/disabled

    Args:
        multiworld: Multiworld
        player (int): Player id
        obj (object): Manual Object to test

    Returns:
        Optional[bool]: enabled or not,
        return None if no category are enable or disabled
    """
    if obj.get("enabled", {}).get(player, None) is not None:
        return obj["enabled"][player]

    world = multiworld.worlds.get(player)
    # if not hasattr(world, 'categoryInit'):
    #     InitCategories(world, player)

    if hasattr(world, "has_category_status"):
        resultYes = False
        resultNo = False
        categories = obj.get('category', [])
        for category in categories:
            result = get_category_status(multiworld, player, category)
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
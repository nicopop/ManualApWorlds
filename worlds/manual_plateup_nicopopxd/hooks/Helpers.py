from typing import Optional
from BaseClasses import MultiWorld
from ..Locations import ManualLocation
from ..Items import ManualItem


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    base = multiworld.worlds[player]

    if category_name.startswith('level_'):
        number = int(category_name[-2:])
        if number <= base.options.host_level.value:
            return True
        return False

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item: ManualItem) -> Optional[bool]:
    base = multiworld.worlds[player]
    name = item.get('name', "")
    if name.endswith(' Recipe'):
        recipe = name.replace(' Recipe', '').replace(' ', '').lower()
        return _check_recipe(base, recipe)
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: ManualLocation) -> Optional[bool]:
    name = location.get('name', "")
    base = multiworld.worlds[player]
    if ' - Beat ' in name:
        recipe = name.split('-')[0].replace(" ", "").lower()
        return _check_recipe(base, recipe)
    return None

def _check_recipe(base, recipe: str) -> Optional[bool]:
    Object = lambda **kwargs: type("Object", (), kwargs)
    if recipe.startswith('extra'):
        more_recipes = base.options.more_recipes.value
        if not more_recipes:
            return False
        number = int(recipe[-2:])
        if number > more_recipes:
            return False
        return None

    option = base.options.__dict__.get(f"recipe_{recipe}", Object(value = None))
    if option.value == 0:
        return False
    return None
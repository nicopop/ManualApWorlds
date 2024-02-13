from typing import Optional
from BaseClasses import MultiWorld
from ..Locations import ManualLocation
from ..Items import ManualItem


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(world: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    base = world.worlds[player]
    # if category_name.startswith('99 - Extra Recipe '):
    #     if not base.options.more_recipes.value:
    #         return False
    #     number = int(category_name[-2:])
    #     if number <= base.options.more_recipes.value:
    #         return True
    #     return False

    if category_name.startswith('level_'):
        number = int(category_name[-2:])
        if number <= base.options.host_level.value:
            return True
        return False

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(world: MultiWorld, player: int, item: ManualItem) -> Optional[bool]:
    if item.get('name', "").startswith('Extra '):
        base = world.worlds[player]
        if not base.options.more_recipes.value:
            return False
        number = int(item.get('name', "").split()[1])
        if number > base.options.more_recipes.value:
            return False
        return True

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(world: MultiWorld, player: int, location: ManualLocation) -> Optional[bool]:
    name = location.get('name', "")
    Object = lambda **kwargs: type("Object", (), kwargs)
    base = world.worlds[player]
    if ' - Beat ' in name:
        recipe = name.split('-')[0].replace(" ", "").lower()

        if recipe.startswith('extra'):
            if not base.options.more_recipes.value:
                return False
            number = int(recipe[-2:])
            if number > base.options.more_recipes.value:
                return False

        option = base.options.__dict__.get(f"recipe_{recipe}", Object(value = None))
        if option.value == 0:
            return False
    return None

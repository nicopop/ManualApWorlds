# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, SpecialRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
#class TotalCharactersToWinWith(Range):
#    """Instead of having to beat the game with all characters, you can limit locations to a subset of character victory locations."""
#    display_name = "Number of characters to beat the game with before victory"
#    range_start = 10
#    range_end = 50
#    default = 50

class ApWorldVersion(FreeText):
    """Do not change this, it will get set to the apworld version"""
    display_name = "Game Version (Detected)"

class HostLevel(Range):
    """What level is your host player?"""
    display_name = "Host Level:"
    range_start = 1
    range_end = 15
    default = 10
class TotalTokenForWin(Range):
    """Percentage of available Recipe needed to win?(rounded up)"""
    display_name = "Recipe % needed to Win"
    range_start = 1
    range_end = 100
    default = 75
class EnableSteak(DefaultOnToggle):
    """Enable the Steak Main recipe"""
    display_name = "Enable Steak"
class EnableSalad(DefaultOnToggle):
    """Enable the Salad Main recipe"""
    display_name = "Enable Salad"
class EnablePizza(DefaultOnToggle):
    """Enable the Pizza Main recipe"""
    display_name = "Enable Pizza"
class EnableDumplings(DefaultOnToggle):
    """Enable the Dumplings Main recipe"""
    display_name = "Enable Dumplings"
class EnableCoffee(DefaultOnToggle):
    """Enable the Coffee Main recipe"""
    display_name = "Enable Coffee"
class EnableBurger(DefaultOnToggle):
    """Enable the Burger Main recipe"""
    display_name = "Enable Burger"
class EnableTurkey(DefaultOnToggle):
    """Enable the Turkey Main recipe"""
    display_name = "Enable Turkey"
class EnablePie(DefaultOnToggle):
    """Enable the Pie Main recipe"""
    display_name = "Enable Pie"
class EnableFish(DefaultOnToggle):
    """Enable the Fish Main recipe"""
    display_name = "Enable Fish"
class EnableHotDog(DefaultOnToggle):
    """Enable the Hot Dog Main recipe"""
    display_name = "Enable Hot Dog"
class EnableBreakfast(DefaultOnToggle):
    """Enable the Breakfast Main recipe"""
    display_name = "Enable Breakfast"
class EnableStirFry(DefaultOnToggle):
    """Enable the Stir Fry Main recipe"""
    display_name = "Enable Stir Fry"
# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
#    options["total_characters_to_win_with"] = TotalCharactersToWinWith
    options["game_version"] = ApWorldVersion
    options["host_level"] = HostLevel
    options["win_percent"] = TotalTokenForWin
    options["recipe_steak"] = EnableSteak
    options["recipe_salad"] = EnableSalad
    options["recipe_pizza"] = EnablePizza
    options["recipe_dumplings"] = EnableDumplings
    options["recipe_coffee"] = EnableCoffee
    options["recipe_burger"] = EnableBurger
    options["recipe_turkey"] = EnableTurkey
    options["recipe_pie"] = EnablePie
    options["recipe_fish"] = EnableFish
    options["recipe_hotdog"] = EnableHotDog
    options["recipe_breakfast"] = EnableBreakfast
    options["recipe_stirfry"] = EnableStirFry

    #options["reduced_spooks"] = ReducedSpooks #we'll need to talk on what need to be disabled/modified when this is enabled
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options
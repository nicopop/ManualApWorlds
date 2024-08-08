# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange

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

class HostLevel(Range):
    """What level is your host player?"""
    display_name = "Host Level"
    range_start = 2
    range_end = 15
    default = 10
class AdditionalRecipe(NamedRange):
    """Add extra X number of unnamed recipe for modded recipe support?"""
    display_name = "Modded Recipes"
    range_start = 0
    range_end = 10
    default = 0
    special_range_names = {
        "none": 0
    }

class TotalTokenForWin(Range):
    """Percentage of available Recipe needed to win?(rounded up)"""
    display_name = "Recipe % needed to Win"
    range_start = 1
    range_end = 100
    default = 75

class Goal(Choice):
    """What is your goal?
    Hit your Quota: Beat day 15 of >= number of recipes than what you chose in 'Recipe % needed to Win'\n
    Get Every Enabled Tokens: Beat every enabled recipes's day 15\n
    Randomly chosen Recipes: Out of every Enabled recipes, 'Recipe % needed to Win'% will have a Victory Token\n
    Randomly placed tokens: a token for every enabled recipes can be found anywhere local. Aka McGuffin mode.\n
    Chaos McGuffin Mode: like Randomly placed tokens but double the amount and can be non local only 'Recipe % needed to Win'% is required
    """
    default = 2
    option_quota = 0
    option_enabled_tokens = 1
    option_random_recipes_quota = 2
    option_randomly_placed_tokens = 3
    option_chaos_mcguffin = 4
    alias_mcguffin_mode = option_randomly_placed_tokens

class OverTimeEnabled(DefaultOnToggle):
    """Do you want to enable the 'overtime - X' locations"""
    display_name = "Overtime"

class ApWorldVersion(FreeText):
    """Do not change this, it will get set to the apworld version"""
    display_name = "Game Version (Detected)"
    default = "Should Be Detected"

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    from ..Data import item_table

    options["game_version"] = ApWorldVersion
    options["host_level"] = HostLevel
    options["win_percent"] = TotalTokenForWin
    options["do_overtime"] = OverTimeEnabled

    for item in [i for i in item_table if "2 Recipes" in i.get("category", []) and not i["name"].lower().startswith("extra")]:
        recipe = item["name"].lower().rstrip("recipe").replace(' ', '')
        level = next(iter(filter(lambda c: c.lower().startswith("level_"), item["category"]))).lstrip("level_")
        options[f"recipe_{recipe}"] = type(f"recipe_{recipe}", (DefaultOnToggle,), {'display_name': f"Enable {item['name']} (lvl{level})"})
        options[f"recipe_{recipe}"].__doc__ = f"Enable the {item['name']} Main recipe"

    options["more_recipes"] = AdditionalRecipe

    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    # the generated goal option will not keep your defined values or documentation string you'll need to add them here:
    # To automatically convert your own goal to alias of the generated goal uncomment this below and replace 'Goal' with your own option of type Choice
    your_goal_class = Goal #Your Goal class here
    generated_goal = options.get('goal', {})
    if generated_goal and issubclass(your_goal_class, Choice) and not issubclass(generated_goal, your_goal_class):
        goals = {'option_' + i: v for i, v in generated_goal.options.items() if i != 'default'}
        for option, value in your_goal_class.options.items():
            if option == 'default':
                continue
            goals[f"alias_{option}"] = value
        options['goal'] = type('goal', (Choice,), goals)
        options['goal'].default = your_goal_class.options.get('default', generated_goal.default)
        options['goal'].__doc__ = your_goal_class.__doc__ or options['goal'].__doc__
    return options
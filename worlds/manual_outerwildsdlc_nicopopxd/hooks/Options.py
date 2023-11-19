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

class RequireSolanum(Toggle):
    """Do you want to require Talking to Solanum before you can win?"""
    display_name = "Require Talking to Solanum"

class RequirePrisoner(Toggle):
    """Do you want to require Talking to the Prisoner before you can win?"""
    display_name = "Require Talking to the Prisoner"

class RandomContent(Choice):
    """What part of the game do you want to play + minimum content for your goal,
    Base Game: disable the dlc and set require_prisoner to false
    DLC: disable every optionnal location but allows require_solanum
    both(default): everything's allowed
    """
    display_name = "Randomized content"
    option_both = 0
    option_base_game = 1
    option_dlc = 2
    default = 0

class Goal(Choice):
    """Where do you want to end,
    Standard(default): for dlc only will end on prisoner, for base and base+dlc will end at the eye.
    Eye: Will require going to the eye.
    Prisoner: Will end after talking to the prisonner
    ash_twin_project_break_spacetime: Require going to the ash twin project and break spacetime there.
    high_energy_lab_break_spacetime: Require going to the high energy lab and break spacetime there.
    """
    display_name = "Goal"
    option_standard = 0
    option_eye = 1
    option_prisoner = 2
    option_ash_twin_project_break_spacetime = 3
    option_high_energy_lab_break_spacetime = 4
    default = 0

class ApWorldVersion(FreeText):
    """Do not change this, it will get set to the apworld version"""
    display_name = "Game Version (Detected)"

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
#    options["total_characters_to_win_with"] = TotalCharactersToWinWith
    options["require_solanum"] = RequireSolanum
    options["require_prisoner"] = RequirePrisoner
    options["game_version"] = ApWorldVersion
    options["randomized_content"] = RandomContent
    options["goal"] = Goal
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options
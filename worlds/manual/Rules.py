from ..generic.Rules import set_rule
from ..AutoWorld import World
from BaseClasses import MultiWorld

def set_rules(base: World, world: MultiWorld, player: int):
    # Location access rules
    for location in base.location_table:
        locFromWorld = world.get_location(location["name"], player)
        if "requires" in location: # Specific item access required
            def fullLocationCheck(state, location=location):
                canAccess = True
                for item in location["requires"]:
                    if not state.has(item, player):
                        canAccess = False
                        break
                return canAccess
            set_rule(locFromWorld, fullLocationCheck)
        else: # Only region access required
            def allRegionsAccessible(state, location=location):
                return True
            set_rule(locFromWorld, allRegionsAccessible) # everything is in the same region in manual

    # Victory requirement
    world.completion_condition[player] = lambda state: state.has("__Victory__", player)
from math import floor, ceil
from .Regions import region_table


ref_resource = {region: [0, 0] for region in region_table}
maxH = 30
maxE = 30
regen = False

def update_ref(state, player):
    """Updates the values in ref_resource and the cached values."""
    pass  # TODO


def update_maxH(state, player):
    """Updates the current max health."""
    wisps = state.count_from_list("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir")
    maxH = 30 + state.count("Health", player)*5 + 10*wisps


def update_maxE(state, player):
    """Updates the max energy."""
    wisps = state.count_from_list("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir")
    maxE = 30 + state.count("Energy", player)*5 + 10*wisps


def update_regen(state, player):
    """Updates if regenerate is collected."""
    if state.has("Regenerate", player):
        regen = True


def total_keystones(state, player):
    """Returns the total amount of Keystones on accessible doors."""
    count = 0
    if (state.can_reach_region("MarshSpawn.CaveEntrance", player)
            or state.can_reach_region("MarshSpawn.RegenDoor", player)):
        count += 2
    if (state.can_reach_region("HowlsDen.BoneBridge", player)
            or state.can_reach_region("HowlsDen.BoneBridgeDoor", player)):
        count += 2
    if (state.can_reach_region("MarshPastOpher.BowArea", player)
            or state.can_reach_region("WestHollow.Entrance", player)):
        count += 2
    if state.can_reach_region("MidnightBurrows.TabletRoom", player):
        count += 4
    if (state.can_reach_region("WoodsEntry.TwoKeystoneRoom", player)
            or state.can_reach_region("WoodsMain.AfterKuMeet", player)):
        count += 2
    if (state.can_reach_region("WoodsMain.FourKeystoneRoom", player)
            or state.can_reach_region("WoodsMain.GiantSkull", player)):
        count += 4
    if state.can_reach_region("LowerReach.TrialStart", player):
        count += 4
    if (state.can_reach_region("UpperReach.OutsideTreeRoom", player)
            or state.can_reach_region("UpperReach.TreeRoomLedge", player)):
        count += 4
    if (state.can_reach_region("UpperDepths.KeydoorLedge", player)
            or state.can_reach_region("UpperDepths.BelowHive", player)):
        count += 2
    if (state.can_reach_region("UpperDepths.Central", player)
            or state.can_reach_region("UpperDepths.LowerConnection", player)):
        count += 2
    if (state.can_reach_region("UpperPools.BeforeKeystoneDoor", player)
            or state.can_reach_region("UpperPools.TreeRoomEntrance", player)):
        count += 4
    if (state.can_reach_region("UpperWastes.KeystoneRoom", player)
            or state.can_reach_region("UpperWastes.MissilePuzzleLeft", player)):
        count += 2
    return count


def has_resources_loc(cost, region):
    """Checks if the player has enough health and energy to reach the location."""
    available = ref_resource[region]
    health, energy = available[0] - cost[0], available[1] - cost[1]
    if energy >= 0:
        if health > 0:
            return True
        if regen and -health < maxH and health + 3*floor(energy) > 0:
            return True
    return False
# TODO case damage=x, damage=x. Maybe execute the function twice ?


def has_resources_conn(cost, region, arrival):
    """Checks if the player has enough health and energy to reach the arrival region, and updates its values."""
    available = ref_resource[region]
    health, energy = available[0] - cost[0], available[1] - cost[1]
    if energy >= 0:
        if health > 0:
            change_ref([health, energy], arrival)
            return True
        if regen and -health < maxH:
            n_regen = ceil((-health + 1)//3)
            if n_regen <= energy:
                change_ref([min(maxH, health + 3*n_regen), energy - n_regen], arrival)
                return True
    return False


def change_ref(resource, arrival):
    """Change the resource amount of the arrival region if a better path is found."""
    if resource > ref_resource[arrival]:  # Lexical order, so greater health, then greater energy.
        ref_resource[arrival] = resource  # TODO: refills, and change comparison if regen

from math import floor, ceil
from .Regions import region_table
from .Refills import refills
import numpy as np


# Damage of each weapon  TODO: remove numpy ?
d_grenade = 8
d_shuriken = 5
d_bow = 4
d_flash = 1
d_sentry = 10
d_spear = 20
d_blaze = 8
d = np.array([d_grenade, d_shuriken, d_bow, d_flash, d_sentry, d_spear, d_blaze])

# Energy cost of each weapon TODO use integers
e_grenade = 1
e_shuriken = 0.5
e_bow = 0.25
e_flash = 0.25
e_sentry = 1
e_spear = 2
e_blaze = 1
e = np.array([e_grenade, e_shuriken, e_bow, e_flash, e_sentry, e_spear, e_blaze])

ref_resource = {region: [0, 0] for region in region_table}
maxH = 30
maxE = 30
refillH = 40
refillE = 10
regen = False


def update_ref(state, player):
    """Updates the values in ref_resource and the cached values."""
    # TODO
    update_maxH(state, player)
    update_maxE(state, player)
    update_refill()
    update_regen(state, player)


def get_maxH(state, player):
    """Returns the current max health."""
    wisps = state.count_from_list("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir")
    return 30 + state.count("Health", player)*5 + 10*wisps


def get_maxE(state, player):
    """Returns the max energy."""
    wisps = state.count_from_list("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir")
    return 30 + state.count("Energy", player)*5 + 10*wisps


def update_refill():
    """Updates the refill values."""
    global refillH, refillE, maxH, maxE
    refillH = max(40, 40)  # TODO: get formulas. Also, do not go above max H/E
    refillE = max(10, 10)


def update_regen(state, player):
    """Updates if regenerate is collected."""
    global regen
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


def cost_all(state, player, region, arrival="", damages=[], en_and=[], en_or=[]):
    """
    Returns a bool stating if the path can be taken, and updates ref_resource if a connection.

    damages (list) contains the dboost values (if several elements, Regenerate can be used inbetween).
    en_and (list of list) contains as elements the skill name, and the amount used. All must be satisfied.
    en_or (list of list) is the same, but anty is required (the lowest cost will be applied).
    """
    health, energy = ref_resource[region]
    maxH, maxE = get_maxH(state, player), get_maxE(state, player)

    for damage in damages:  # This part deals with the damage boosts
        health -= damage
        if health <= 0:
            if state.has("Regenerate", player) and -health < maxH:
                n_regen = ceil((-health + 1)/3)
                if n_regen > energy:
                    return False
                health = min(maxH, health + 3*n_regen)
                energy -= n_regen
            else:
                return False

    cost_and = 0
    for source in en_and:
        if not state.has(source[0], player):
            return False
        cost_and += E_cost[source[0]]*source[1]

    cost_or = 10000  # Arbitrary value, must be high
    invalid = True
    for source in en_or:  # TODO: create E_cost, deal with empty requirements
        if not state.has(source[0], player):
            continue
        invalid = False
        cost_or = min(cost_or, E_cost[source[0]]*source[1])

    energy -= cost_and + cost_or

    if energy < 0 or invalid:
        return False
    if arrival:
        apply_refill(arrival, state, player, [health, energy], [maxH, maxE])
        return True
    return True


def change_ref(resource, arrival):
    """Change the resource amount of the arrival region if a better path is found."""
    if resource > ref_resource[arrival]:  # Lexical order, so greater health, then greater energy.
        ref_resource[arrival] = resource  # TODO: refills, and change comparison if regen


def cost_boss(hp, state, player, diff_g=1):
    """Energy cost for the boss with current state."""
    # TODO: implement game difficulty as option, and get diff_g from there
    # TODO: merge this with cost_damage
    if state.has("Sword", player) or state.has("Hammer", player):
        return 0

    if diff_g == 0:
        mod = 0.5
    elif diff_g == 2:
        mod = 1.8
    else:
        mod = 1

    c = e*np.ceil(hp*mod/d)

    if not state.has("Grenade"):
        c[0] = np.inf
    if not state.has("Shuriken"):
        c[1] = np.inf
    if not state.has("Bow"):
        c[2] = np.inf
    if not state.has("Flash"):
        c[3] = np.inf
    if not state.has("Sentry"):
        c[4] = np.inf
    if not state.has("Spear"):
        c[5] = np.inf
    if not state.has("Blaze"):
        c[6] = np.inf

    return np.min(c)


def Damage(hp_list, state, player, region, arrival=None, diff_g=1):
    """Energy cost for the enemies/wall/boss with current state."""
    # TODO: implement game difficulty as option, and get diff_g from there
    global d, e  # TODO: rename
    if state.has("Sword", player) or state.has("Hammer", player):
        return True

    if diff_g == 0:  # TODO: verify the values
        mod = 0.5
    elif diff_g == 2:
        mod = 1.8
    else:
        mod = 1

    cost = np.zeros(7)
    for hp in hp_list:
        cost += e * np.ceil(hp * mod / d)

    if not state.has("Grenade"):
        cost[0] = np.inf
    if not state.has("Shuriken"):
        cost[1] = np.inf
    if not state.has("Bow"):
        cost[2] = np.inf
    if not state.has("Flash"):
        cost[3] = np.inf
    if not state.has("Sentry"):
        cost[4] = np.inf
    if not state.has("Spear"):
        cost[5] = np.inf
    if not state.has("Blaze"):
        cost[6] = np.inf

    cost = np.min(cost)
    remain = ref_resource[region] - cost
    if remain >= 0:
        if arrival:
            ref_resource[arrival][1] = remain
            return True
        return True
    return False
    # TODO: rework as returning a bool and updating the resource. Make separate function for trials (that use refills, and do not update)


def BreakCrystal(state, player, diff=0):  # TODO get difficulty from options
    """Returns a bool, stating if the player can break energy crystals."""
    if diff == 0:
        return state.has_any("Sword", "Hammer", "Bow", player)
    if diff == 1 or diff == 2:
        return state.has_any("Shuriken", "Grenade", player)
    return state.has("Spear", player)


def apply_refill(region, state, player, resource, max_res):
    """Updates the resource table for the arrival region, using the resource and the refills."""
    maxH, maxE = max_res
    global refillH, refillE
    en, hp, tr = refills[region]
    if tr == 2 and state.has("F." + region, player):
        ref_resource[region] = [maxH, maxE]
    else:
        if tr == 1 and state.has("C." + region, player):
            resource = [max(resource[0], refillH), max(resource[1], refillE)]
        if hp != 0 and state.has("H." + region, player):
            resource[0] = max(maxH, resource[0] + hp*10)
        if en != 0 and state.has("E." + region, player):
            resource[1] += max(maxE, resource[1] + en*10)
        ref_resource[region] = resource

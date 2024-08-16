from math import ceil, floor
from .Regions import region_table
from .Refills import refills

weapon_data = {  # The list contains the damage, and its energy cost
    "Grenade": [13, 10],  # Can be 17 damage if charged
    "Shuriken": [7, 5],
    "Bow": [4, 2.5],
    "Flash": [12, 10],
    "Sentry": [8, 10],  # 8.8, rounded down here
    "Spear": [20, 20],
    "Blaze": [13, 10],  # 13.8, rounded down here
    }

ref_resource = {region: [0, 0] for region in region_table}


def has_health(amount, state, player):
    """Returns if the player has enough max health to enter the area."""
    wisps = state.count_from_list("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir")
    return amount < 30 + state.count("Health", player)*5 + 10*wisps


def get_max(state, player):
    """Returns the current max health and energy."""
    wisps = state.count_from_list("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir")
    return 30 + state.count("Health", player)*5 + 10*wisps, 30 + state.count("Energy", player)*5 + 10*wisps


def get_refill(max_resource):
    """Returns the refill values."""
    maxH, maxE = max_resource
    refillH = max(40, floor(maxH/5/0.6685 + 1), maxH)
    refillE = 10*floor(maxE/50+1)
    return refillH, refillE


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


# TODO: multiply energy cost by 2 if not in unsafe. Also add combat_and, combat_or, damages_or
def cost_all(state, player, region, arrival="", damages=[], en_and=[], en_or=[]):
    """
    Returns a bool stating if the path can be taken, and updates ref_resource if it's a connection.

    damages (list) contains the dboost values (if several elements, Regenerate can be used inbetween).
    en_and (list of list) contains as elements the skill name, and the amount used. All must be satisfied.
    en_or (list of list) is the same, but anty is required (the lowest cost will be applied).
    """
    health, energy = ref_resource[region]
    maxH, maxE = get_max(state, player)

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

    cost_and = 0  # This computes the energy cost for weapons
    for source in en_and:
        if not state.has(source[0], player):
            return False
        cost_and += weapon_data[source[0]][1]*source[1]

    cost_or = 0
    if en_or:
        cost_or = 1000  # Arbitrary value, must be higher than 200
        for source in en_or:
            if not state.has(source[0], player):
                continue
            cost_or = min(cost_or, weapon_data[source[0]][1]*source[1])

    energy -= cost_and + cost_or

    if energy < 0:
        return False
    if arrival:
        update_ref(arrival, state, player, [health, energy], [maxH, maxE])
        return True
    return True


def Damage(hp_list, state, player, region, weapons, arrival="", diff_g=1):  # TODO: hard/easy: damage modifier
    """
    Energy cost for the enemies/wall/boss with current state.

    `weapons` indicates the list of energy weapons that can be used in the situation.
    """
    # TODO: implement game difficulty as option, and get diff_g from there
    if state.has("Sword", player) or state.has("Hammer", player):
        tot_cost = 0

    else:
        if not weapons:
            return False
        if diff_g == 2:
            mod = 1.8
        else:
            mod = 1

        tot_cost = 0
        for hp in hp_list:
            for weapon in weapons:
                cost = 1000  # Arbitrary value, higher than 200
                if state.has(weapon, player):
                    cost = min(cost, weapon_data[weapon][1] * ceil(hp*mod / weapon_data[weapon][0]))
            tot_cost += cost

    health, energy = ref_resource[region]
    energy -= tot_cost
    if energy < 0:
        return False
    if arrival:
        maxH, maxE = get_max(state, player)
        update_ref(arrival, state, player, [health, energy], [maxH, maxE])
        return True
    return True
    # TODO: implement trials (that use refills in middle, and do not update)


def BreakCrystal(state, player, diff=0):  # TODO get difficulty from options. Maybe merge with damage=1 ? Or get cost then use it to correct refills
    """Returns a bool, stating if the player can break energy crystals."""
    if diff == 0:
        return state.has_any("Sword", "Hammer", "Bow", player)
    if diff == 1 or diff == 2:
        return state.has_any("Shuriken", "Grenade", player)
    return state.has("Spear", player)


def update_ref(region, state, player, resource, max_res):
    """Updates the resource table for the arrival region, using the resource and the refills."""
    maxH, maxE = max_res
    refillH, refillE = get_refill(max_res)
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

        if resource > ref_resource[region]:  # Updates if bigger (lexical order, so health takes priority)
            ref_resource[region] = resource

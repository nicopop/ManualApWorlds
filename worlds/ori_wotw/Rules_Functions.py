from math import ceil, floor
from .Regions import region_table
from .Refills import refills

weapon_data = {  # The list contains the damage, and its energy cost
    "Sword": [4, 0],
    "Hammer": [12, 0],
    "Grenade": [13, 1],  # Can be 17 damage if charged
    "Shuriken": [7, 0.5],
    "Bow": [4, 0.25],
    "Flash": [12, 1],
    "Sentry": [8, 1],  # 8.8, rounded down here
    "Spear": [20, 2],
    "Blaze": [13, 1],  # 13.8, rounded down here
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
    return 30 + state.count("Health", player)*5 + 10*wisps, 3 + state.count("Energy", player)*0.5 + wisps


def get_refill(max_resource):
    """Returns the refill values."""
    maxH, maxE = max_resource
    refillH = max(40, floor(maxH/5/0.6685 + 1), maxH)
    refillE = floor(maxE/50+1)
    return refillH, refillE


def can_keystones(state, player):
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
    return state.count("Keystone", player) >= count


def cost_all(state, player, options, region, arrival, damage_and, en_and, combat_and, or_req):
    """
    Returns a bool stating if the path can be taken, and updates ref_resource if it's a connection.

    damage_and (list) contains the dboost values (if several elements, Regenerate can be used inbetween).
    combat_and (list of list) contains the combat damages needed and the type (enemy/wall).
    en_and (list of list) contains as elements the skill name, and the amount used. All must be satisfied.
    or_req (list of list) contains damages, combat, and energy in each sublist (the first element of the list is the
    type of requirement: 0 is combat, 1 is energy, 2 is damage boost). Any can be verified.
    """
    diff = options.difficulty
    health, energy = ref_resource[region]
    maxH, maxE = get_max(state, player)

    if diff != 3:  # Energy costs are doubled, except in unsafe
        energy /= 2

    for damage in damage_and:  # This part deals with the damage boosts
        health -= damage
        if health <= 0:
            if state.has("Regenerate", player) and -health < maxH:
                n_regen = ceil((-health + 1)/30)
                if n_regen > energy:
                    return False
                health = min(maxH, health + 30*n_regen)
                energy -= n_regen
            else:
                return False

    for source in en_and:  # This computes the energy cost for weapons
        if not state.has(source[0], player):
            return False
        energy -= weapon_data[source[0]][1] * source[1]
        if energy < 0:
            return False

    energy -= combat_cost(state, player, options, combat_and)
    if energy < 0:
        return False

    if or_req:
        min_cost = 1000  # Arbitrary value, higher than 200
        hp_cost = False
        for req in or_req:
            if req[0] == 0:
                if all([state.has(danger) for danger in req[2]]):
                    min_cost = min(min_cost, combat_cost(state, player, options, req[1]))
            if req[0] == 1:
                if state.has(req[1]):
                    min_cost = min(min_cost, weapon_data[req[1]][1] * req[2])
            if req[0] == 2:
                hp_cost = req[1]
        if min_cost > energy:
            if not hp_cost:
                return False
            else:
                health -= hp_cost
                if state.has("Regenerate", player) and -health < maxH:
                    n_regen = ceil((-health + 1)/30)
                    if n_regen > energy:
                        return False
                    health = min(maxH, health + 30*n_regen)
                    energy -= n_regen
        else:
            energy -= min_cost

    if arrival:
        if diff != 3:
            energy *= 2
        update_ref(arrival, state, player, [health, energy], [maxH, maxE])
        return True
    return True


def combat_cost(state, player, options, hp_list):
    """Returns the energy cost for the enemies/walls/boss with current state."""
    hard = options.hard_mode
    diff = options.difficulty

    tot_cost = 0
    for damage, category in hp_list:
        if category == "Combat":
            if diff == 3:
                weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"]
            else:
                weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]
        elif category == "Ranged":
            if diff == 0:
                weapons = ["Bow", "Spear"]
            elif diff == 3:
                weapons = ["Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"]
            else:
                weapons = ["Grenade", "Bow", "Shuriken", "Sentry", "Spear"]
        elif category == "Wall":
            weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]
        elif category == "Boss":
            if hard:
                damage *= 1.8
            if diff == 3:
                weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"]
            else:
                weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]
        else:  # ShurikenBreak or SentryBreak
            weapons = [category]

        cost = 1000  # Arbitrary value, higher than 200
        for weapon in weapons:
            if state.has(weapon, player):
                cost = min(cost, weapon_data[weapon][1] * ceil(damage / weapon_data[weapon][0]))
        tot_cost += cost

    return tot_cost


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
            resource[1] += max(maxE, resource[1] + en)

        if resource > ref_resource[region]:  # Updates if bigger (lexical order, so health takes priority)
            ref_resource[region] = resource

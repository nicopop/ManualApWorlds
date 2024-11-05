from typing import Dict, List
from math import ceil, floor
from .Refills import refills

weapon_data: Dict[str, List] = {  # The list contains the damage, and its energy cost
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


def has_health(amount: int, state, player) -> bool:
    """Returns if the player has enough max health to enter the area."""
    wisps = state.count_from_list(("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir"), player)
    return amount < 30 + state.count("Health", player)*5 + 10*wisps


def get_max(state, player) -> (int, float):
    """Returns the current max health and energy."""
    wisps = state.count_from_list(("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir"), player)
    return 30 + state.count("Health", player)*5 + 10*wisps, 3 + state.count("Energy", player)*0.5 + wisps


def get_refill(max_resource: (int, float)) -> (int, int):
    """Returns the refill values."""
    maxH, maxE = max_resource
    refillH = max(40, floor(maxH/5/0.6685 + 1), maxH)
    refillE = floor(maxE/5+1)
    return refillH, refillE


def can_buy_map(state, player) -> bool:
    """Returns if the total amount of Spirit Light can buy all accessible maps."""
    cost = 200  # Higher cost than necessary to make it less constrained for the player.
    if state.can_reach_region("MarshSpawn.BrokenBridge", player):
        cost += 200
    if state.can_reach_region("MidnightBurrows.Central", player):
        cost += 50
    if state.can_reach_region("WestHollow.HollowDrainLower", player):
        cost += 150
    if state.can_reach_region("InnerWellspring.WestDoor", player):
        cost += 150
    if (state.can_reach_region("LowerReach.Central", player)
            or state.can_reach_region("LowerReach.OutsideTPRoom", player)):
        cost += 150
    if state.can_reach_region("LowerDepths.East", player):
        cost += 150
    if state.can_reach_region("EastPools.LupoArea", player):
        cost += 150
    if state.can_reach_region("LowerWastes.ThirstyGorlek", player):
        cost += 150
    if state.can_reach_region("WillowsEnd.InnerTP", player):
        cost += 50
    return state.count("200 Spirit Light", player) >= ceil(cost/200)


def can_keystones(state, player) -> bool:
    """Returns if the total amount of Keystones can open all accessible doors."""
    count = 2  # Add more Keystones than necessary to make it less constrained for the player.
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


def cost_all(state, player, ref_resource, options, region: str, arrival: str, damage_and: List, en_and: List[List],
             combat_and: List[List], or_req: List[List], refill: str, update: bool) -> bool:
    """
    Returns a bool stating if the path can be taken, and updates ref_resource if it's a connection.

    damage_and: contains the dboost values (if several elements, Regenerate can be used inbetween).
    combat_and: contains the combat damages needed and the type (enemy/wall).
    en_and: contains as elements the skill name, and the amount used. All must be satisfied.
    or_req: contains damages, combat, and energy in each sublist (the first element of the list is the
        type of requirement: 0 is combat, 1 is energy, 2 is damage boost). Any can be verified.
    update: indicates if the resource table has to be updated
    refill: indicates if the path leads to a refill, and its type in that case
    """
    diff = options.difficulty
    hard = options.hard_mode
    health, energy, old_maxH, old_maxE = ref_resource[region].copy()
    maxH, maxE = get_max(state, player)

    # Note: this can yield to some inaccuracies, but it should be fine (except maybe in unsafe).
    # The alternative is to redo all rules each time an item is received, but that takes too long
    health += maxH - old_maxH
    energy += maxE - old_maxE

    if diff != 3:  # Energy costs are doubled, except in unsafe
        energy /= 2

    for damage in damage_and:  # This part deals with the damage boosts
        if hard:
            damage *= 2
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
        min_cost = 1000  # Arbitrary value, higher than 20
        hp_cost = False
        for req in or_req:
            if req[0] == 0:
                if all([state.has(danger, player) for danger in req[2]]):
                    min_cost = min(min_cost, combat_cost(state, player, options, req[1]))
            if req[0] == 1:
                if state.has(req[1], player):
                    min_cost = min(min_cost, weapon_data[req[1]][1] * req[2])
            if req[0] == 2:
                hp_cost = req[1]
        if min_cost > energy:
            if not hp_cost:  # The damage boost option is considered only if no other option is possible.
                return False
            else:
                if hard:
                    hp_cost *= 2
                health -= hp_cost
                if state.has("Regenerate", player) and -health < maxH:
                    n_regen = ceil((-health + 1)/30)
                    if n_regen > energy:
                        return False
                    health = min(maxH, health + 30*n_regen)
                    energy -= n_regen
        else:
            energy -= min_cost

    if update:
        if diff != 3:
            energy *= 2
        update_ref(arrival, state, player, ref_resource, [health, energy], [maxH, maxE], refill)
    return True


def no_cost(region: str, arrival: str, state, player, ref_resource, refill: str) -> bool:
    """Executed when the path does not consume resource to still update the resource table."""
    maxH, maxE = get_max(state, player)
    old_health, old_energy, old_maxH, old_maxE = ref_resource[region].copy()
    oldH = old_health + maxH - old_maxH
    oldE = old_energy + maxE - old_maxE
    update_ref(arrival, state, player, ref_resource, [oldH, oldE], get_max(state, player), refill)
    return True


def combat_cost(state, player, options, hp_list: List[List]) -> float:
    """Returns the energy cost for the enemies/walls/boss with current state."""
    hard = options.hard_mode
    diff = options.difficulty

    tot_cost = 0
    max_cost = 0  # Maximum amount used, in case there are refills during combat.
    for damage, category in hp_list:
        if category == "Combat":
            if diff == 3:
                weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"]
            else:
                weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]
        elif category == "Wall":
            weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]
        elif category == "Boss":
            if hard:
                damage *= 1.8
            if diff == 3:
                weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"]
            else:
                weapons = ["Sword", "Hammer", "Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]
        elif category == "Refill":
            max_cost = max(max_cost, tot_cost)
            tot_cost -= damage  # In that case, damage contains the amount of energy given back
            continue
        else:  # ShurikenBreak or SentryBreak
            weapons = [category]

        cost = 1000  # Arbitrary value, higher than 20
        for weapon in weapons:
            if state.has(weapon, player):
                cost = min(cost, weapon_data[weapon][1] * ceil(damage / weapon_data[weapon][0]))
        tot_cost += cost

    return max(tot_cost, max_cost)


def update_ref(region: str, state, player, ref_resource, resource: [int, float], max_res: [int, float], refill: str):
    """Updates the resource table for the arrival region, using the resource and the refills."""
    maxH, maxE = max_res
    old_health, old_energy, old_maxH, old_maxE = ref_resource[region].copy()
    oldH = old_health + maxH - old_maxH
    oldE = old_energy + maxE - old_maxE
    refillH, refillE = get_refill(max_res)
    en, hp, tr = refills[region]

    if tr == 2 and (refill == "F" or state.has("F." + region, player)):
        ref_resource[region] = [maxH, maxE, maxH, maxE]
    else:
        if tr == 1 and (refill == "C" or state.has("C." + region, player)):
            resource = [max(resource[0], refillH), max(resource[1], refillE)]
        if hp != 0 and (refill == "H" or state.has("H." + region, player)):
            resource[0] = min(maxH, resource[0] + hp*10)
        if en != 0 and (refill == "E" or state.has("E." + region, player)):
            resource[1] = min(maxE, resource[1] + en)

        if resource > [oldH, oldE]:  # Updates if bigger (lexical order, so health takes priority)
            ref_resource[region] = [resource[0], resource[1], maxH, maxE]
        elif old_health == 0:  # If this is the first time the region is accessible, update the resource table
            ref_resource[region] = [resource[0], resource[1], maxH, maxE]
        # Otherwise, the resource table is unchanged

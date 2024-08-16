"""
Converts an areas.wotw file into a set_rules function.

Run `parsing()` to extract the rules (the `areas.wotw` file must be in the same folder as this script).
"""

import os
import re
from math import ceil
from collections import Counter

# TODO : fix line 271 in areas.wotw and 10803 (TwoCrushersEX)
# TODO 4: Create syntax analysis for areas.wotw
# %% Data and global variables

# Enemy data
ref_en = {"Mantis": (32, ("Free")),
          "Slug": (13, ("Free")),
          "WeakSlug": (12, ("Free")),
          "BombSlug": (1, ("Ranged")),
          "CorruptSlug": (1, ("Ranged")),
          "SneezeSlug": (32, ("Dangerous")),
          "ShieldSlug": (24, ("Free")),
          "Lizard": (24, ("Free")),
          "Bat": (32, ("Bat", "Aerial", "Ranged")),
          "Hornbug": (40, ("Dangerous", "Shielded")),
          "Skeeto": (20, ("Aerial")),
          "SmallSkeeto": (8, ("Aerial")),
          "Bee": (24, ("Aerial")),
          "Nest": (25, ("Aerial")),
          "Fish": (10, ("Free")),
          "Waterworm": (20, ("Free")),
          "Crab": (32, ("Dangerous")),
          "SpinCrab": (32, ("Dangerous")),
          "Tentacle": (40, ("Ranged")),
          "Balloon": (1, ("Free")),
          "Miner": (40, ("Dangerous")),
          "MaceMiner": (60, ("Dangerous")),
          "ShieldMiner": (60, ("Dangerous", "Shielded")),
          "CrystalMiner": (80, ("Dangerous")),
          "ShieldCrystalMiner": (50, ("Dangerous", "Shielded")),
          "Sandworm": (20, ("Sand")),
          "Spiderling": (12, ("Free")),
          }

# Regular expressions used for parsing
com = re.compile(" *#")  # Detects comments
sp = re.compile("^ *")  # Used for indents
col = re.compile(" .*:")  # name between space and colon
tra = re.compile(" *$")  # Trailing space
sep = re.compile(" at ")
typ = re.compile("^  [a-z]+ ")  # Detects the type of the path
nam = re.compile(" [a-zA-Z.=0-9]+:")  # Name of the object
dif = re.compile("^[a-z]+, ")  # extracts the difficulty of the path
ref = re.compile("[a-zA-Z=0-9]+$")  # Extracts the refill type if it has no colon

en_skills = ("Bow", "Grenade", "Flash", "Sentry", "Shuriken", "Spear", "Blaze")  # Skills that require energy

# Things that require a specific treatment
combat_name = ("BreakWall", "Combat", "Boss")

# Skills that can be used infinitly (note: Regenerate is here because of how the logic is written)
inf_skills = ("Sword", "DoubleJump", "Regenerate", "Dash", "Bash", "Grapple", "Glide", "Flap", "WaterDash",
              "Burrow", "Launch", "Water", "WaterBreath", "Hammer", "free")

# Glitches that use resources
glitches = {"ShurikenBreak": ["Shuriken"],
            "SentryJump": ["Sentry"],
            "SwordSJump": ["Sword", "Sentry"],
            "HammerSJump": ["Hammer", "Sentry"],
            "SentryBurn": ["Sentry"],
            "SentryBreak": ["Sentry"],
            "SpearBreak": ["Spear"],
            "SentrySwap": ["Sentry"],
            "BlazeSwap": ["Blaze"],
            "GrenadeRedirect": ["Grenade"],
            "SentryRedirect": ["Sentry"],
            "SpearJump": ["Spear"]}

# Glitches that can be used infinitly (and only use one skill)
inf_glitches = {"RemoveKillPlane": "free",
                "HammerBreak": "Hammer",
                "LaunchSwap": "Launch",
                "FlashSwap": "Flash",
                "GrenadeJump": "Grenade",
                "GrenadeCancel": "Grenade",
                "BowCancel": "Bow",
                "PauseHover": "free",
                "GlideJump": "Glide"}

# Glitches that can be used infinitly, and use two skills
other_glitches = ("WaveDash", "HammerJump", "SwordJump", "GlideHammerJump")


# %% Text initialisations

header = ("\"\"\"\n"
          "File generated with `extract_rules.py` with an `areas.wotw` file.\n\n"
          "You can find such a file at https://github.com/ori-community/wotw-seedgen/tree/main/wotw_seedgen .\n\n"
          "Do not edit manually.\n"
          "\"\"\"\n\n"
          )

imports = "from .Rules_Functions import *\n\n"

lightM = "    add_rule(world.get_location(\"DepthsLight\", player), lambda state: state.has_any((\"UpperDepths.ForestsEyes\", \"Flash\"), player))\n"
lightG = "    add_rule(world.get_location(\"DepthsLight\", player), lambda state: state.has(\"Bow\", player))\n"
# TODO add rule for glitches, and their event

# %% Functions for extracting rules


def parsing(override=False):
    """Parse an areas.wotw file, and creates `Rules.py` containing the rules, and `Entrances.py` for the entrances."""
    if os.path.exists("./Rules.py"):
        if override:
            print("Warning: File `Rules.py` replaced")
        else:
            raise FileExistsError("The file `Rules.py` already exists. Use `override=True` to override it.")
    if os.path.exists("./Entrances.py"):
        if override:
            print("Warning: File `Entrances.py` replaced")
        else:
            raise FileExistsError("The file `Entrances.py` already exists. Use `override=True` to override it.")
    if os.path.exists("./Refills.py"):
        if override:
            print("Warning: File `Refills.py` replaced")
        else:
            raise FileExistsError("The file `Refills.py` already exists. Use `override=True` to override it.")

    with open("./areas.wotw", "r") as file:
        temp = file.readlines()

    # Moki, Gorlek, Kii and Unsafe rules respectively
    M = (header + imports + "from worlds.generic.Rules import add_rule\n\n\n"
         "def set_moki_rules(world, player, options):\n"
         "    \"\"\"Moki (or easy, default) rules.\"\"\"\n" + lightM)
    G = ("\n\ndef set_gorlek_rules(world, player, options):\n"
         "    \"\"\"Gorlek (or medium) rules.\"\"\"\n" + lightG)
    Gg = ("\n\ndef set_gorlek_glitched_rules(world, player, options):\n"
          "    \"\"\"Gorlek (or medium) rules with glitches\"\"\"\n")
    K = ("\n\ndef set_kii_rules(world, player, options):\n"
         "    \"\"\"Kii (or hard) rules\"\"\"\n")
    Kg = ("\n\ndef set_kii_glitched_rules(world, player, options):\n"
          "    \"\"\"Kii (or hard) rules with glitches.\"\"\"\n")
    U = ("\n\ndef set_unsafe_rules(world, player, options):\n"
         "    \"\"\"Unsafe rules.\"\"\"\n")
    Ug = ("\n\ndef set_unsafe_glitched_rules(world, player, options):\n"
          "    \"\"\"Unsafe rules with glitches.\"\"\"\n")

    L_rules = [M, G, Gg, K, Kg, U, Ug]
    entrances = []
    refills = {}  # Contains the refill info per region as a list: [health, energy, type]
    refill_events = []  # Stores all the names given to the refill events.

    # Variables
    anc = ""  # Name of the current anchor
    diff = 0  # Difficulty of the path
    req2 = ""  # Requirements from second indent
    req3 = ""  # Requirements from third indent
    req4 = ""  # Requirements from fourth indent
    ref_type = ""  # Refill type (energy, health, checkpoint or full)

    c_diff = {"moki": 0, "gorlek": 1, "kii": 3, "unsafe": 5}

    for i, p in enumerate(temp):  # line number is only used for debug
        m = com.search(p)  # Removes the comments
        if m:
            p = p[:m.start()]
        m = tra.search(p)  # Removes the trailing spaces
        if m:
            p = p[:m.start()]
        if p == "":
            continue

        m = sp.match(p)  # Counts the indents
        if m is None:
            ind = 0
        else:
            ind = (m.end()+1)//2

        if ind == 0:
            if "anchor" in p:
                name = col.search(p).group()[1:-1]
                s = sep.search(name)
                if s:
                    anc = name[:s.start()]
                else:
                    anc = name
                refills.setdefault(anc, [0, 0, 0])
            else:
                anc = ""

        elif ind == 1:
            if not anc:
                continue
            if "nospawn" in p or "tprestriction" in p:  # TODO: manage these
                continue
            p_type = typ.search(p).group()[2:-1]  # Connection type
            if p_type not in ("conn", "state", "pickup", "refill", "quest"):
                raise ValueError(f"{p_type} (line {i}) is not an appropriate path type.\n\"{p}\"")
            if p_type == "refill":
                if ":" in p:
                    p_name = nam.search(p).group()[1:-1]
                    ref_type, refills, refill_events = conv_refill(p_name, anc, refills, refill_events)
                else:
                    p_name = ref.search(p).group()
                    ref_type, refills, refill_events = conv_refill(p_name, anc, refills, refill_events)
                    convert(anc, p_type, p_name, L_rules, entrances, ref_type, 0, "free")
            else:
                p_name = nam.search(p).group()[1:-1]  # Name

            if "free" in p:
                L_rules, entrances = convert(anc, p_type, p_name, L_rules, entrances, ref_type, 0, "free")

        elif ind == 2:
            if not anc:
                continue
            if p[-1] == ":":
                if p[4:] in ("moki:", "gorlek:", "kii:", "unsafe:"):
                    diff = c_diff[p[4:-1]]
                    req2 = ""
                elif "moki" in p or "gorlek" in p or "kii" in p or "unsafe" in p:
                    s = dif.search(p[4:])
                    diff = c_diff[s.group()[:-2]]
                    req2 = p[s.end()+4:-1]
                else:
                    raise ValueError(f"Input on line {i} is invalid.\n\"{p}\"")

            elif ": " in p:
                if "moki:" in p or "gorlek:" in p or "kii:" in p or "unsafe:" in p:
                    start = p.find(": ")
                    diff = c_diff[p[4:start]]
                    req = p[start + 2:]
                    L_rules, entrances = convert(anc, p_type, p_name, L_rules, entrances, ref_type, diff, req)
                else:
                    s = dif.search(p[4:])
                    diff = c_diff[s.group()[:-2]]
                    req = p[s.end()+4:]
                    req = req.replace(":", ",")
                    L_rules, entrances = convert(anc, p_type, p_name, L_rules, entrances, ref_type, diff, req)
            else:
                raise ValueError(f"Input on line {i} is invalid.\n\"{p}\"")

        elif ind == 3:
            if not anc:
                continue
            if p[-1] == ":":
                req3 = p[6:-1]
            else:
                req3 = ""
                if req2:
                    req = req2 + ", " + p[6:]
                else:
                    req = p[6:]
                L_rules, entrances = convert(anc, p_type, p_name, L_rules, entrances, ref_type, diff, req)

        elif ind == 4:
            if not anc:
                continue
            if p[-1] == ":":
                req4 = p[8:-1]
            else:
                req4 = ""
                req = ""
                if req2:
                    req += req2 + ", "
                if req3:
                    req += req3 + ", "
                req += p[8:]
                L_rules, entrances = convert(anc, p_type, p_name, L_rules, entrances, ref_type, diff, req)

        elif ind == 5:
            if not anc:
                continue
            req = ""
            if req2:
                req += req2 + ", "
            if req3:
                req += req3 + ", "
            if req4:
                req += req4 + ", "
            req += p[10:]
            L_rules, entrances = convert(anc, p_type, p_name, L_rules, entrances, ref_type, diff, req)

        else:
            raise NotImplementedError(f"Too many indents ({ind}) on line {i}.\n{p}")

    ent_txt = header + "\n" + "entrance_table = [\n"
    for entrance in entrances:
        ent_txt += f"    \"{entrance}\",\n"
    ent_txt += "    ]\n"

    ref_txt = header + "\n" + "refills = {  # key: region name. List: [health restored, energy restored, refill type]\n"
    ref_txt += "    # For refill type: 0 is no refill, 1 is Checkpoint, 2 is Full refill.\n"
    for region, info in refills.items():
        ref_txt += f"    \"{region}\": {info},\n"
    ref_txt += ("    }\n\n"
                "refill_events = [\n")
    for name in refill_events:
        ref_txt += f"    \"{name}\",\n"
    ref_txt += "    ]\n"

    with open("Rules.py", "w") as file:
        for i in range(7):
            file.write(L_rules[i])
        print("The file `Rules.py` has been successfully created.")
    with open("Entrances.py", "w") as file:
        file.write(ent_txt)
        print("The file `Entrances.py` has been successfully created.")
    with open("Refills.py", "w") as file:
        file.write(ref_txt)
        print("The file `Refills.py` has been successfully created.")


def convert(anc, p_type, p_name, L_rules, entrances, ref_type, diff=0, req="free"):
    """
    Converts the data given by the arguments into an add_rule function, and adds it to the right difficulty.

    Returns the updated lists.
    anc: name of the starting anchor
    p_type: type of the element accessed by the rules (anchor, state, refill or item)
    p_name: name of the element accessed by the rules
    diff: difficulty of the path (str)
    req: requirements to access the element
    """
    glitched = False
    health_req = 0  # Requirement when entering a new area

    and_req = []
    or_req = []

    if "." in anc:  # Gets the requirements when entering a new area.
        s = anc.find(".")
        i_area = anc[:s]  # Extracts the name of the area
        if p_type == "anchor" and "." in p_name:
            s = p_name.find(".")
            f_area = p_name[:s]
            if i_area != f_area:
                regen, health_req = req_area(f_area, diff)
                if regen:
                    and_req.append("Regenerate")

    arrival = ""
    if p_type == "conn":
        arrival = p_name
        conn_name = f"{anc}_to_{p_name}"
        if conn_name not in entrances:
            entrances.append(conn_name)

    s_req = req.split(", ")
    for elem in s_req:
        if " OR " in elem:
            or_req.append(elem.split(" OR "))
        else:
            and_req.append(elem)

    if len(or_req) > 2:
        raise ValueError(f"{req}\n{or_req}")  # TODO debug, remove

    if len(or_req) == 2:
        or_skills0, or_glitch0, or_resource0 = order_or(or_req[0])
        or_skills1, or_glitch1, or_resource1 = order_or(or_req[1])

        # Swaps the two chains if it is more efficient to split the second resource chain
        if len(or_resource0) > len(or_resource1):
            (or_skills0, or_glitch0, or_resource0, or_skills1, or_glitch1,
             or_resource1) = (or_skills1, or_glitch1, or_resource1, or_skills0, or_glitch0, or_resource0)

        for req in or_glitch0:
            for req2 in or_glitch1:  # Case 0 glitched, 1 glitched
                and_req.append(req)
                and_req.append(req2)
                and_requirements, glitched = parse_and(and_req, diff)
                and_req.remove(req)
                and_req.remove(req2)
                L_rules = append_rule(and_requirements, "", "", "", health_req, diff, True, anc, p_name, arrival,
                                      L_rules)
            if or_skills1:   # Case 0 glitched, 1 skill
                and_req.append(req)
                and_requirements, glitched = parse_and(and_req, diff)
                and_req.remove(req)
                L_rules = append_rule(and_requirements, "", or_skills1, "", health_req, diff, True, anc, p_name,
                                      arrival, L_rules)
            if or_resource1:  # Case 0 glitched, 1 resource
                and_req.append(req)
                and_requirements, glitched = parse_and(and_req, diff)
                and_req.remove(req)
                L_rules = append_rule(and_requirements, "", "", or_resource1, health_req, diff, True, anc, p_name,
                                      arrival, L_rules)

        for req in or_resource0:
            for req2 in or_glitch1:  # Case 0 resource, 1 glitched
                and_req.append(req)
                and_req.append(req2)
                and_requirements, glitched = parse_and(and_req, diff)
                and_req.remove(req)
                and_req.remove(req2)
                L_rules = append_rule(and_requirements, "", "", "", health_req, diff, True, anc, p_name, arrival,
                                      L_rules)
            if or_skills1:  # Case 0 resource, 1 skill
                and_req.append(req)
                and_requirements, glitched = parse_and(and_req, diff)
                and_req.remove(req)
                L_rules = append_rule(and_requirements, "", or_skills1, "", health_req, diff, glitched, anc, p_name,
                                      arrival, L_rules)
            if or_resource1:  # Case 0 resource, 1 resource
                and_req.append(req)
                and_requirements, glitched = parse_and(and_req, diff)
                and_req.remove(req)
                L_rules = append_rule(and_requirements, "", "", or_resource1, health_req, diff, glitched, anc, p_name,
                                      arrival, L_rules)

        for req2 in or_glitch1:  # Case 0 skill, 1 glitched
            and_req.append(req2)
            and_requirements, glitched = parse_and(and_req, diff)
            and_req.remove(req2)
            L_rules = append_rule(and_requirements, or_skills0, "", "", health_req, diff, True, anc, p_name, arrival,
                                  L_rules)
        if or_skills1:  # Case 0 skill, 1 skill
            and_requirements, glitched = parse_and(and_req, diff)
            L_rules = append_rule(and_requirements, or_skills0, or_skills1, "", health_req, diff, glitched, anc,
                                  p_name, arrival, L_rules)
        if or_resource1:  # Case 0 skill, 1 resource
            and_requirements, glitched = parse_and(and_req, diff)
            L_rules = append_rule(and_requirements, or_skills0, "", or_resource1, health_req, diff, glitched, anc,
                                  p_name, arrival, L_rules)

    return L_rules, entrances


def combat_req(need, value):
    """Parse the combat requirement with the given enemies."""
    damage = []
    dangers = []

    if need == "Combat":
        enemies = value.split("+")

        for elem in enemies:
            amount = 1
            if "EnergyRefill" in elem:  # TODO: account for this, but does not affect logic at this point
                continue
            if elem[1] == "x":
                amount = int(elem[0])
                elem = elem[2:]
            danger = ref_en[elem][1]
            if "Ranged" in danger:
                damage_type = "Ranged"
            else:
                damage_type = "Combat"
            damage.append([[ref_en[elem][0]], damage_type] * amount)
            for dan in danger:
                if dan not in dangers and dan not in ("Free", "Ranged"):
                    dangers.append("Combat." + dan)

    elif need == "Boss":
        damage.append([int(value), "Combat"])

    elif need == "BreakWall":
        damage.append([int(value), "Wall"])

    return damage, dangers


def parse_and(and_req, diff):
    """Parse the list of requirements in the `and` chain, and returns the processed information."""
    and_skills = []  # Stores inf_skills
    and_other = []  # Stores other requirements (that often have their own event)
    damage_and = []  # Stores damage boosts
    combat_and = []  # Stores combat damage to inflict, as a list of each damage to do + the type of combat
    # The type of combat can be ranged, wall
    en_and = []  # Stores energy weapon used
    glitched = False

    for requirement in and_req:
        if "=" in requirement:
            elem, value = requirement.split("=")
        else:
            elem = requirement
            value = 0

        if elem in other_glitches:  # Handle the glitches
            glitched = True
            and_other.append(elem)
        elif elem in inf_glitches.keys():
            glitched = True
            req = inf_glitches[elem]
            if req not in and_skills and req != "free":
                and_skills.append(req)
        elif elem in glitches.keys():
            glitched = True
            value = int(value)
            req = glitches[elem]
            for i, skill in enumerate(req):
                if elem == "ShurikenBreak" and diff == 5:
                    combat_and.append((value*2, "Shuriken"))
                elif elem == "ShurikenBreak":
                    combat_and.append((value*3, "Shuriken"))
                elif elem == "SentryBreak":
                    combat_and.append((value*6.25, "Shuriken"))
                elif i == len(req)-1:
                    en_and += [skill] * value
                else:
                    if req not in and_skills and req != "free":
                        and_skills.append(req)

        elif elem in inf_skills:
            if elem not in and_skills and elem != "free":
                and_skills.append(elem)
        elif elem in en_skills:
            value = int(value)
            en_and += [elem] * value
        elif elem == "Damage":
            value = int(value)
            damage_and.append(value)
        elif elem in combat_name:
            deal_damage, danger = combat_req(elem, value)
            combat_and += deal_damage
            and_other += danger
        else:  # Case of an event, or keystone, or spirit light, or ore
            and_other.append(elem)
    return (and_skills, and_other, damage_and, combat_and, en_and), glitched


def order_or(or_chain):
    """Parse the list of requirements in the `or` chain, and categorize them."""
    or_skills = []  # Stores inf_skills
    or_glitch = []  # Stores the glitches
    or_resource = []  # Stores requirements that need resources

    for requirement in or_chain:
        if "=" in requirement:
            elem = requirement.split("=")[0]
        else:
            elem = requirement

        if elem in other_glitches or elem in inf_glitches.keys() or elem in glitches.keys():  # Handle the glitches
            or_glitch.append(requirement)

        elif elem in inf_skills:
            or_skills.append(requirement)
        elif elem in en_skills or elem in combat_name or elem == "Damage":
            or_resource.append(requirement)
        else:  # Case of an event
            or_skills.append(requirement)
    return or_skills, or_glitch, or_resource


def append_rule(and_requirements, or_skills0, or_skills1, or_resource, health, diff, glitched, anc, p_name, arrival,
                L_rules):
    """Adds the text to the rules list."""  # TODO: complete docstring
    and_skills, and_other, damage_and, combat_and, en_and = and_requirements

    if not arrival and not p_name:
        raise ValueError("p_name or arrival must be non empty.")

    if arrival:
        start_txt = f"    add_rule(world.get_entrance(\"{anc}_to_{arrival}\", player), lambda s: "
        req_txt = ""
    else:
        start_txt = f"    add_rule(world.get_location(\"{p_name}\", player), lambda s: "
        req_txt = "s.can_reach_region(\"{anc}\")"

    if and_skills:
        temp_txt = ""
        for elem in and_skills:
            if temp_txt:
                temp_txt += f", \"{elem}\""
            else:
                temp_txt += f"s.has_all((\"{elem}\""
        temp_txt += "), player)"
        if req_txt:
            req_txt += " and " + temp_txt
        else:
            req_txt += temp_txt

    if and_other:
        for elem in and_other:
            if "Keystone" in elem:
                temp_txt = "can_keystones(s, player)"
            elif "=" in elem:
                name, amount = elem.split("=")
                if name == "SpiritLight":
                    temp_txt = f"s.count(\"SpiritLight\", player) >= {ceil(amount/100)}"
                elif name == "Ore":
                    temp_txt = f"s.count(\"Ore\", player) >= {amount}"
                else:
                    raise ValueError(f"Invalid input: {elem}")
            else:
                temp_txt = f"s.has(\"{elem}\", player)"
            if req_txt:
                req_txt += "and" + temp_txt
            else:
                req_txt += temp_txt

    if or_skills0:
        temp_txt = ""
        for elem in or_skills0:
            if temp_txt:
                temp_txt += f", \"{elem}\""
            else:
                temp_txt += f"s.has_any((\"{elem}\""
        temp_txt += "), player)"
        if req_txt:
            req_txt += " and " + temp_txt
        else:
            req_txt += temp_txt

    if or_skills1:
        temp_txt = ""
        for elem in or_skills1:
            if temp_txt:
                temp_txt += f", \"{elem}\""
            else:
                temp_txt += f"s.has_any((\"{elem}\""
        temp_txt += "), player)"
        if req_txt:
            req_txt += " and " + temp_txt
        else:
            req_txt += temp_txt

    if health:
        if req_txt:
            req_txt += "and" + f"has_health(\"{health}\", s, player)"
        else:
            temp_txt += f"has_health(\"{health}\", s, player)"

    if en_and:
        counter = Counter(en_and)
        energy = []
        for weapon in en_skills:
            amount = counter[weapon]
            if amount != 0:
                energy.append([weapon, amount])

    or_costs = []  # List of list, each element is a possibility. The first element of the lists codes the type of cost.
    for requirement in or_resource:
        if "=" in requirement:
            elem, value = requirement.split("=")
        else:
            elem = requirement
            value = 0
        if elem == "Combat":
            deal_damage, danger = combat_req(elem, value)
            or_costs.append([0, deal_damage, danger])
        elif elem in en_skills:
            or_costs.append([1, elem, value])
        elif elem == "Damage":
            or_costs.append([2, value])

    if damage_and or combat_and or en_and or or_costs:
        temp_txt = (f"cost_all(s, player, options, \"{anc}\", \"{arrival}\", {damage_and}, {en_and}, {combat_and}, "
                    f"{or_costs}):")
        if req_txt:
            req_txt += "and" + temp_txt
        else:
            temp_txt += temp_txt

    if req_txt:
        tot_txt = start_txt + req_txt + ")\n"
    else:
        tot_txt = start_txt + "True)\n"
    if glitched:
        diff += 1

    L_rules[diff] += tot_txt

    return L_rules


def conv_refill(p_name, anc, refills, refill_events):
    """Returns the refill type (to add before the region name) and updates the data tables."""
    current = refills[anc]
    if "=" in p_name:
        value = int(p_name[-1])
        if p_name[:-2] == "Health":
            if current[0] == 0:
                refills.update({anc: [value, current[1], current[2]]})
                refill_events.append(f"H.{anc}")
            return "H.", refills, refill_events
        if p_name[:-2] == "Energy":
            if current[1] == 0:
                refills.update({anc: [current[0], value, current[2]]})
                refill_events.append(f"E.{anc}")
            return "E.", refills, refill_events
    if p_name == "Checkpoint":
        refills.update({anc: [current[0], current[1], 1]})
        refill_events.append(f"C.{anc}")
        return "C.", refills, refill_events
    if p_name == "Full":
        refills.update({anc: [current[0], current[1], 2]})
        refill_events.append(f"F.{anc}")
        return "F.", refills, refill_events
    raise ValueError(f"{p_name} is not a valid refill type (at anchor {anc}).")


def req_area(area, diff):
    """Requirements for entering an area."""
    M_dat = {"MidnightBurrows": (25, False), "EastHollow": (20, False), "WestHollow": (20, False),
             "WestGlades": (20, False), "OuterWellspring": (25, False), "InnerWellspring": (25, False),
             "WoodsEntry": (40, True), "WoodsMain": (40, True), "LowerReach": (40, True), "UpperReach": (40, True),
             "UpperDepths": (40, True), "LowerDepths": (40, True), "PoolsApproach": (25, True), "EastPools": (40, True),
             "UpperPools": (40, True), "WestPools": (40, True), "LowerWastes": (50, True), "UpperWastes": (50, True),
             "WindtornRuins": (50, True), "WeepingRidge": (60, True), "WillowsEnd": (60, True)}

    if area in (None, "MarshSpawn", "HowlsDen", "MarshPastOpher", "GladesTown"):
        return False, 0
    if diff >= 5:  # Unsafe
        return False, 0
    if diff >= 1:
        if M_dat[area][1]:  # Kii, Gorlek
            return True, 0
        return False, 0

    if M_dat[area][1]:  # Moki
        return True, M_dat[area][0]
    return False, M_dat[area][0]

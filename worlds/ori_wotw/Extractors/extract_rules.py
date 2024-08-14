"""
Converts an areas.wotw file into a set_rules function.

Run `parsing()` to extract the rules (the `areas.wotw` file must be in the same folder as this script).
"""

import os
import re
import numpy as np

# TODO : fix line 271 in areas.wotw and 10803 (TwoCrushersEX)
# TODO 1: group the indents: reduces redundancies, helps for ordering
# TODO 2: Order by increasing damage, then energy cost, so that the bool eval is nice (handle difficulties ?)
# TODO 3: Reevaluate when state evolves
# TODO 4: Create syntax analysis for areas.wotw
# %% Data and global variables

skills = ("Sword", "DoubleJump", "Regenerate", "Bow", "Dash", "Bash", "Grapple", "Glide", "Flap", "Grenade",
          "Flash", "WaterDash", "Burrow", "Launch", "Water", "WaterBreath", "Hammer", "Sentry", "Shuriken",
          "Spear", "Blaze")

# Damage of each weapon
# TODO: get exact values
d_grenade = 10
d_shuriken = 5
d_bow = 4
d_flash = 1
d_sentry = 10
d_spear = 20
d_blaze = 10
d = np.array([d_grenade, d_shuriken, d_bow, d_flash, d_sentry, d_spear, d_blaze])

# TODO: get exact values
# Energy cost of each weapon
e_grenade = 1
e_shuriken = 0.5
e_bow = 0.25
e_flash = 0.25
e_sentry = 1
e_spear = 2
e_blaze = 1
e = np.array([e_grenade, e_shuriken, e_bow, e_flash, e_sentry, e_spear, e_blaze])

# Enemy data
ref_en = {"Mantis": (32, "Free"),
          "Slug": (13, "Free"),
          "WeakSlug": (12, "Free"),
          "BombSlug": (1, "Ranged"),
          "CorruptSlug": (1, "Ranged"),
          "SneezeSlug": (32, "Dangerous"),
          "ShieldSlug": (24, "Free"),
          "Lizard": (24, "Free"),
          "Bat": (32, ("Bat", "Aerial", "Ranged")),
          "Hornbug": (40, ("Dangerous", "Shielded")),
          "Skeeto": (20, "Aerial"),
          "SmallSkeeto": (8, "Aerial"),
          "Bee": (24, "Aerial"),
          "Nest": (25, "Aerial"),
          "Fish": (10, "Free"),
          "Waterworm": (20, "Free"),
          "Crab": (32, "Dangerous"),
          "SpinCrab": (32, "Dangerous"),
          "Tentacle": (40, "Ranged"),
          "Balloon": (1, "Free"),
          "Miner": (40, "Dangerous"),
          "MaceMiner": (60, "Dangerous"),
          "ShieldMiner": (60, ("Dangerous", "Shielded")),
          "CrystalMiner": (80, "Dangerous"),
          "ShieldCrystalMiner": (50, ("Dangerous", "Shielded")),
          "Sandworm": (20, "Sand"),
          "Spiderling": (12, "Free"),
          "EnergyRefill": (1, "Free")}  # TODO : remove EnergyRefill and Boss

# Requirements for enemies
ref_rule = {"Aerial": ("state.has_any((\"DoubleJump\", \"Launch\"), player)",
                       "state.has(\"Bash\", player)",
                       "free",
                       "free"),
            "Dangerous": ("state.has_any((\"DoubleJump\", \"Dash\", \"Bash\", \"Launch\"), player)",
                          "state.has_any((\"DoubleJump\", \"Dash\", \"Bash\", \"Launch\"), player)",
                          "free",
                          "free"),
            "Ranged": ("state.has_any((\"Bow\", \"Spear\"), player)",
                       "state.has_any((\"Grenade\", \"Shuriken\", \"Sentry\"), player)",
                       "state.has_any((\"Grenade\", \"Shuriken\", \"Sentry\"), player)",
                       "state.has_any((\"Flash\", \"Blaze\"), player)"),
            "Shielded": ("state.has_any((\"Hammer\", \"Launch\", \"Grenade\", \"Spear\"), player)",
                         "state.has_any((\"Hammer\", \"Launch\", \"Grenade\", \"Spear\"), player)",
                         "state.has_any((\"Hammer\", \"Launch\", \"Grenade\", \"Spear\"), player)",
                         "state.has_any((\"Hammer\", \"Launch\", \"Grenade\", \"Spear\"), player)"),
            "Bat": ("state.has(\"Bash\", player)",
                    "state.has(\"Bash\", player)",
                    "free",
                    "free"),
            "Sand": ("state.has(\"Burrow\", player)",
                     "state.has(\"Burrow\", player)",
                     "state.has(\"Burrow\", player)",
                     "state.has(\"Burrow\", player)"),
            "Free": ("free",
                     "free",
                     "free",
                     "free")}

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


# %% Text initialisations

header = ("\"\"\"\n"
          "File generated with `extract_rules.py` with an `areas.wotw` file.\n\n"
          "You can find such a file at https://github.com/ori-community/wotw-seedgen/tree/main/wotw_seedgen .\n\n"
          "Do not edit manually.\n"
          "\"\"\"\n\n"
          )

imports = "from .Rules Func import total_keystones, BreakCrystal\n\n"

lightM = "    add_rule(world.get_location(\"DepthsLight\", player), lambda state: state.has_any((\"UpperDepths.ForestsEyes\", \"Flash\"), player))\n"
lightG = "    add_rule(world.get_location(\"DepthsLight\", player), lambda state: state.has(\"Bow\", player))\n"
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
         "def set_moki_rules(world, player):\n"
         "    \"\"\"Moki (or easy, default) rules.\"\"\"\n" + lightM)
    G = (header + imports + "from worlds.generic.Rules import add_rule\n\n\n"
         "def set_gorlek_rules(world, player):\n"
         "    \"\"\"Gorlek (or medium) rules.\"\"\"\n" + lightM + lightG)
    Gg = (header + imports + "from worlds.generic.Rules import add_rule\n\n\n"
          "def set_gorlek_glitched_rules(world, player):\n"
          "    \"\"\"Gorlek (or medium) rules with glitches\"\"\"\n" + lightM + lightG)
    K = (header + imports + "from worlds.generic.Rules import add_rule\n\n\n"
         "def set_kii_rules(world, player):\n"
         "    \"\"\"Kii (or hard) rules\"\"\"\n" + lightM + lightG)
    Kg = (header + imports + "from worlds.generic.Rules import add_rule\n\n\n"
          "def set_kii_glitched_rules(world, player):\n"
          "    \"\"\"Kii (or hard) rules with glitches.\"\"\"\n" + lightM + lightG)
    U = (header + imports + "from worlds.generic.Rules import add_rule\n\n\n"
         "def set_unsafe_rules(world, player):\n"
         "    \"\"\"Unsafe rules.\"\"\"\n" + lightM + lightG)
    Ug = (header + imports + "from worlds.generic.Rules import add_rule\n\n\n"
          "def set_unsafe_glitched_rules(world, player):\n"
          "    \"\"\"Unsafe rules with glitches.\"\"\"\n" + lightM + lightG)

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
        file.write(L_rules[0])
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
    diff: difficulty of the path (str)
    req: requirements to access the element
    """
    words = {"conn": "entrance", "pickup": "location", "state": "location", "quest": "location", "refill": "location"}
    area_req = ""
    text_req = ""
    glitch_path = False

    if "." in anc:  # Gets the requirements when entering a new area.
        s = anc.find(".")
        i_area = anc[:s]
        if p_type == "anchor" and "." in p_name:
            s = p_name.find(".")
            f_area = p_name[:s]
            if i_area != f_area:
                area_req = req_area(f_area, diff)

    s_req = req.split(", ")
    for elem in s_req:
        if " OR " in elem:
            chain = elem.split(" OR ")
            temp = ""
            for s_elem in chain:
                result, glitch = inter(s_elem, diff)
                if result:
                    if temp:
                        temp += " or " + result
                    else:
                        temp += "(" + result
            temp += ")"
        else:
            temp, glitch = inter(elem, diff)

        if temp:
            if text_req:
                text_req += " and " + temp
            else:
                text_req += temp
        if glitch:
            glitch_path = True

    if p_type == "conn":
        p_name = f"{anc}_to_{p_name}"
        if p_name not in entrances:
            entrances.append(p_name)
        if area_req and text_req:
            tot_req = area_req + " and " + text_req
        elif text_req:
            tot_req = text_req
        elif area_req:
            tot_req = area_req
        else:
            tot_req = True
    elif p_type == "refill":
        p_name = ref_type + anc
        if text_req:
            tot_req = text_req
        else:
            tot_req = True
    else:
        tot_req = f"state.can_reach_region(\"{anc}\", player)"
        if area_req:
            tot_req += " and " + area_req
        if text_req:
            tot_req += " and " + text_req

    p_type = words[p_type]
    text = f"    add_rule(world.get_{p_type}(\"{p_name}\", player), lambda state: {tot_req})\n"

    if glitch_path:
        diff += 1

    # L_rules[diff] += text TODO decomment
    if diff == 0:
        L_rules[0] += text
    else:   # TODO Other difficulties not implemented yet
        pass
    return L_rules, entrances


def inter(text, diff):
    """Converts the isolated requirement (single keyword, or a chain of OR) into a rule function."""
    # Skills that do not use energy
    inf_skills = ("Sword", "DoubleJump", "Regenerate", "Dash", "Bash", "Grapple", "Glide", "Flap", "WaterDash",
                  "Burrow", "Launch", "Water", "WaterBreath", "Hammer")
    glitches = {"ShurikenBreak": "Shuriken",  # TODO separate the ones with an =
                "SentryJump": "Sentry",
                "SwordSJump": "Sword, Sentry",
                "HammerSJump": "Hammer, Sentry",
                "SentryBurn": "Sentry",
                "RemoveKillPlane": "free",
                "SentryBreak": "Sentry",
                "HammerBreak": "Hammer",
                "SpearBreak": "Spear",
                "LaunchSwap": "Launch",
                "FlashSwap": "Flash",
                "SentrySwap": "Sentry",
                "BlazeSwap": "Blaze",
                "WaveDash": "Dash, Regenerate",
                "GrenadeJump": "Grenade",
                "GrenadeCancel": "Grenade",
                "BowCancel": "Bow",
                "HammerJump": "Hammer, DoubleJump",
                "SwordJump": "Sword, DoubleJump",
                "GrenadeRedirect": "Grenade",
                "SentryRedirect": "Sentry",
                "PauseHover": "free",
                "GlideJump": "Glide",
                "GlideHammerJump": "Glide, Hammer",
                "SpearJump": "Spear"}

    if text in inf_skills:
        return f"state.has(\"{text}\", player)", False
    if text == "free":
        return "", False

    if "=" in text:
        s = text.find("=")
        need = text[:s]

        # TODO : compute the energy cost, and remove the base weapon requirement.
        if need == "Combat":
            value = text[s+1:]
            enemies = value.split("+")
            dangers = []
            damage = []
            for elem in enemies:
                amount = 1
                if elem[1] == "x":
                    elem = elem[2:]
                    damage.append([elem])
                    amount = int(elem[-1])
                danger = ref_en[elem][1]
                damage.append([ref_en[elem][0]] * amount)
                if isinstance(danger, str):  # Case when only one danger type for all the enemies
                    if danger not in dangers:
                        dangers.append(danger)
                else:
                    for dan in danger:
                        if dan not in dangers:
                            dangers.append(dan)
            if diff == 0:
                out = "state.has_any((\"Sword\", \"Hammer\"), player)"  # require non energy weapon for moki
            else:
                out = f"Damage({damage}, state, player, {anc}, {arrival}, diff_g)"  # TODO: complete region, arrival ?
            for elem in dangers:
                out_t = ref_rule[elem][(diff+1)//2]  # This gives 0->0, 1->1, 3->2, 5->3 (it maps diff to the index)
                if out_t != "free":
                    out += " and " + out_t
            return out, False
        if need == "Boss":
            return "state.has_any((\"Sword\", \"Hammer\"), player)", False

        value = int(text[s+1:])
        # TODO: compute cost (now : 5 energy)
        if need in ("Grenade", "Sentry", "Shuriken", "Bow", "Flash", "Spear", "Blaze"):
            return f"state.has(\"{need}\", player) and state.count(\"Energy\", player) >= 4", False
        if need == "Damage":  # TODO : route refills, and use game difficulty
            HC = int(max(0, np.ceil((value-29)/5)))
            return f"state.count(\"Health\", player) >= {HC}", False  # TODO: change
        if need == "BreakWall":
            return f"Damage({value}, state, player, {anc}, {arrival}, diff_g)", False  # TODO fix
        if need == "Keystone":
            return "state.count(\"Keystone\", player) >= total_keystones(state, player)", False
        if need == "SpiritLight":
            return f"state.count(\"SpiritLight\", player) >= {np.ceil(value/100)}", False
        if need == "Ore":
            return f"state.count(\"Ore\", player) >= {value}", False
        if need in glitches.keys():
            return "", True  # TODO associate requirement
        raise ValueError(f"Invalid input: {text}.")
    if text == "BreakCrystal":
        return "BreakCrystal(state, player, diff)", False
    return f"state.has(\"{text}\", player)", False


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
        return None
    if diff >= 5:  # Unsafe
        return None
    if diff >= 1:
        if M_dat[area][1]:  # Kii, Gorlek
            return "state.has(\"Regenerate\", player)"
        return None

    HC = int(max(0, np.ceil((M_dat[area][0]-29)/5)))  # TODO change, just put the health amount
    if M_dat[area][1]:  # Moki
        return f"state.has(\"Regenerate\", player) and state.count(\"Health\", player) >= {HC}"  # TODO change
    return f"state.count(\"Health\", player) >= {HC}"

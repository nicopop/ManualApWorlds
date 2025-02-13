from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World

skills_ids: dict[str, str] = {
    "Sword": "spell:1002",
    "Double Jump": "spell:3004",
    "Regenerate": "spell:2013",
    "Bow": "spell:1001",
    "Dash": "spell:4000",
    "Bash": "spell:3000",
    "Grapple": "spell:3001",
    "Glide": "spell:4002",
    "Flap": "spell:3005",
    "Grenade": "spell:2010",
    "Flash": "spell:2004",
    "Water Dash": "spell:4004",
    "Burrow": "spell:3002",
    "Launch": "spell:2019",
    "Clean Water": "file:assets/icons/game/water.png",
    "Water Breath": "opher:10",
    "Hammer": "spell:1000",
    "Sentry": "spell:2011",
    "Shuriken": "spell:2015",
    "Spear": "spell:2012",
    "Blaze": "spell:2016"
}

collectibles_ids: dict[str, str] = {
    "Health Fragment": "file:assets/icons/game/healthfragment.png",
    "Energy Fragment": "file:assets/icons/game/energyfragment.png",
    "Ore": "file:assets/icons/game/gorlekore.png",
    "Keystone": "file:assets/icons/game/keystone.png",
    "Shard Slot": "file:assets/icons/game/shardslot.png",
    "Ancestral Light 1": "spell:4007",
    "Ancestral Light 2": "spell:4008"
}
shards_ids: dict[str, str] = {
    "Overcharge": "shard:1",
    "Triple Jump": "shard:2",
    "Wingclip": "shard:3",
    "Bounty": "shard:4",
    "Swap": "shard:5",
    "Magnet": "shard:8",
    "Splinter": "shard:9",
    "Reckless": "shard:13",
    "Quickshot": "shard:14",
    "Resilience": "shard:18",
    "Light Harvest": "shard:19",
    "Vitality": "shard:22",
    "Life Harvest": "shard:23",
    "Energy Harvest": "shard:25",
    "Energy": "shard:26",
    "Life Pact": "shard:27",
    "Last Stand": "shard:28",
    "Sense": "shard:30",
    "Ultra Bash": "shard:32",
    "Ultra Grapple": "shard:33",
    "Overflow": "shard:34",
    "Thorn": "shard:35",
    "Catalyst": "shard:36",
    "Turmoil": "shard:38",
    "Sticky": "shard:39",
    "Finesse": "shard:40",
    "Spirit Surge": "shard:41",
    "Lifeforce": "shard:43",
    "Deflector": "shard:44",
    "Fracture": "shard:46",
    "Arcing": "shard:47"
}
upgrades_ids: dict[str, str] = {
    "Rapid Sentry": "opher:1",
    "Hammer Shockwave": "opher:3",
    "Static Shuriken": "opher:5",
    "Exploding Spear": "opher:7",
    "Charge Blaze": "opher:9",
    "Water Breath": "opher:10"
}
bonus_ids: dict[str, str] = { #Generated using the 'randomizer\assets\icons\bonus' folder and group_table["bonus"] + group_table["bonus+"]
    "Health Regeneration": "file:assets/icons/bonus/healthregeneration.png",
    "Energy Regeneration": "file:assets/icons/bonus/energyregeneration.png",
    "Extra Double Jump": "file:assets/icons/bonus/extradoublejump.png",
    "Extra Air Dash": "file:assets/icons/bonus/extraairdash.png",
    "Blaze Efficiency": "file:assets/icons/bonus/blazeefficiency.png",
    "Spear Efficiency": "file:assets/icons/bonus/spearefficiency.png",
    "Shuriken Efficiency": "file:assets/icons/bonus/shurikenefficiency.png",
    "Sentry Efficiency": "file:assets/icons/bonus/sentryefficiency.png",
    "Bow Efficiency": "file:assets/icons/bonus/bowefficiency.png",
    "Regenerate Efficiency": "file:assets/icons/bonus/regenerateefficiency.png",
    "Flash Efficiency": "file:assets/icons/bonus/flashefficiency.png",
    "Grenade Efficiency": "file:assets/icons/bonus/grenadeefficiency.png",
    "Rapid Sword": "file:assets/icons/bonus/rapidsword.png",
    "Rapid Hammer": "file:assets/icons/bonus/rapidsmash.png", # Manually Found
    "Rapid Spear": "file:assets/icons/bonus/rapidspear.png",
    "Rapid Grenade": "file:assets/icons/bonus/rapidgrenade.png",
    "Quickshot Upgrade": "file:assets/icons/bonus/rapidquickshot.png", # Manually Found
    "Rapid Regenerate": "file:assets/icons/bonus/rapidregen.png", # Manually Found
    "Melting Bow":  skills_ids["Bow"], # Manually Found
    "Melting Blaze": "file:assets/icons/bonus/meltingblaze.png",
    "Melting Sword": "file:assets/icons/bonus/meltingsword.png",
    "Melting Hammer": skills_ids["Hammer"], # Manually Found
    "Melting Spear": "file:assets/icons/bonus/meltingspear.png",
    "Melting Shuriken": "file:assets/icons/bonus/meltingshuriken.png",
    "Uncharged Bashnades": "file:assets/icons/bonus/unchargedbashgrenade.png", # Manually Found
    "Extra Grenade": "file:assets/icons/bonus/extragrenade.png",
    "Splinter Grenade": "file:assets/icons/bonus/splintergrenade.png",
    "Unlimited Sentries": "file:assets/icons/bonus/unlimitedsentries.png",
    "Sentry Burst Upgrade": "file:assets/icons/bonus/sentryburstupgrade.png",
    "Sentry Fire Rate": "file:assets/icons/bonus/sentryattackspeed.png", # Manually Found
    "Extra Shurikens": "file:assets/icons/bonus/extrashuriken.png", # Manually Found
    "Splinter Shurikens": "file:assets/icons/bonus/splintershuriken.png", # Manually Found
    "Bashable Shurikens": "file:assets/icons/bonus/bashableshuriken.png" # Manually Found
}
others_ids: dict[str, str] = {
    "teleporter": "file:assets/icons/game/teleporter.png",
    "experience": "file:assets/icons/game/experience.png",
    "map": "file:assets/icons/game/map.png",
    "message": "file:assets/icons/game/message.png",
    "moki": "file:assets/icons/game/moki.png"
}

def get_item_iconpath(world: World, item: Item, keyword_based_icons: bool = True) -> str|None:
    classification = ItemClassification(item.classification) #sometimes apworld use ints that since 0.6.0 need to be converted explicitly

    icon_path = None
    if item.game == world.game: #Try to use base game and rando icons
        if item.name.endswith("Spirit Light"):
            icon_path = others_ids["experience"]

        elif item.name.endswith(" TP"):
            icon_path = others_ids["teleporter"]

        elif skills_ids.get(item.name):
            icon_path = skills_ids[item.name]

        elif shards_ids.get(item.name):
            icon_path = shards_ids[item.name]

        elif collectibles_ids.get(item.name):
            icon_path = collectibles_ids[item.name]

        elif upgrades_ids.get(item.name):
            icon_path = upgrades_ids[item.name]

        elif bonus_ids.get(item.name):
            icon_path = bonus_ids[item.name]

        else: #If seen mean we missed an item
            icon_path = others_ids["message"] # message meaning tell us on discord...

    elif keyword_based_icons: #Some generic icons for any games
        if "key" in item.name.lower():
            icon_path = collectibles_ids["Keystone"]
        elif "health" in item.name.lower() or "life" in item.name.lower() or "Heart" in item.name.lower():
            icon_path = collectibles_ids["Health Fragment"]
        elif "energy" in item.name.lower():
            icon_path = collectibles_ids["Energy Fragment"]
        elif "map" in item.name.lower():
            icon_path = others_ids["map"]
        elif "TP" in item.name:
            icon_path = others_ids["teleporter"]
        elif "ore" in item.name.lower():
            icon_path = collectibles_ids["Ore"]
        elif "exp" in item.name.lower() or "xp" in item.name.lower() or "ability" in item.name.lower():
            icon_path = others_ids["experience"]

    if icon_path is None: # Fallback to Classification system if keyword_based_icons is turned off or fail
        if ItemClassification.trap in classification:
            icon_path = world.random.choice(list(skills_ids.values()) + list(collectibles_ids.values()))

        elif ItemClassification.progression in classification:
            icon_path = collectibles_ids["Shard Slot"] #placeholder

        elif ItemClassification.useful in classification:
            icon_path = others_ids["moki"] #placeholder

        #Else None aka default ? icon for now

    return icon_path

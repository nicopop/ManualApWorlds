# Outer Wilds Archipelago Manual Randomizer Setup Guide

<p align="center">
    <img alt="OuterWilds Logo"
     src="https://upload.wikimedia.org/wikipedia/fr/thumb/d/dc/Outer_Wilds_Logo.png/800px-Outer_Wilds_Logo.png?20190112131250"
    >
    <h1 align="center">Base Game Archipelago Manual Randomizer Edition</h1>
    <p align="center">v3.1.1</p>
</p>

## Required Software

- OuterWilds Game ([Steam](https://store.steampowered.com/app/753640/Outer_Wilds/)
 / [Epic Games](https://launcher.store.epicgames.com/en-US/p/outerwilds)
 / [Xbox](https://www.xbox.com/en-CA/games/store/outer-wilds/C596FKDKMQN7)
 / [PS4/5](https://store.playstation.com/en-us/product/UP2470-PPSA08101_00-OUTERWILDSSIEA00)
 / [Switch](https://www.nintendo.com/en-ca/store/products/outer-wilds-switch/))
- The latest stable [ManualClient](https://discord.gg/T5bcsVHByx)

## Optional Software

- [OuterWilds Mod Manager](https://outerwildsmods.com/mod-manager/)*
    + PC versions only (Steam or Epic Games)

## ↑ Recommended* and Optional mods from manager↑

Install those from the Mod Manager
- [Clock](https://outerwildsmods.com/mods/clock/)*
    - Shows a timer with the main event at the bottom right of the screen.
- [Hiker's Mod](https://outerwildsmods.com/mods/hikersmod/)*
    - By default only add sprint but can also add walljumps(not in logic)
- [Achievements+](https://outerwildsmods.com/mods/achievements/)*
    - Add popup when you would get an achievement on new save even if you allready have that steam achievement.
- [Enable Meditation](https://outerwildsmods.com/mods/enablemeditation/)*
    - Like the name might suggest you always have the "meditate until next loop button" in the pause menu.
- [Suit Log](https://outerwildsmods.com/mods/suitlog/)
    - Allows you to open your ship log from anywhere. 
- [Trajectory Prediction](https://outerwildsmods.com/mods/trajectoryprediction/)
    - Shows where your shipscout/player is going vs selected planet
    - Require you enabling "Use Incremental GC" in the modmanager settings

## Installation Procedures

Make sure a copy of the Manual world is in the lib/world directory of your client-side installation.

### Optional install:

1. Open the link in [Optional Software](#optional-software) or using this [direct link](https://outerwildsmods.com/mod-manager/)
2. Press the 'Big Green Download Button' or the portable version link under it.
3. Save the downloaded installer somewhere.
    1. If you downloaded the portable version save it somewhere easy to access and that you wont forget.
4. Run the installer, the Mod Manager should start automatically.
    1. If you downloaded the portable version launch the OuterWilds Mod Manager.
5. First you have to install the OWML mod (should be the first in the list)  
by pressing the download icon (third button from the right)
6. To install the mods you either find them in the list and press download icon  
or you can search for them by name at the top of the Mod tab 
7. Once you have all the mods you want press the Start Game button at the top, it will enable all the mods  
you installed and after that you'll only need to start from the Mod Manager when you add/remove/update mods

## Joining a MultiWorld Game

- Launch the client.  
- At the top enter your server's ip with the port provided (by default archipelago.gg:38281).  
- In Manual Game ID put "Manual_OuterWilds_Nicopopxd" then press the Connect button on the top right.  
- In the command field at the bottom enter the name of your slot you chose in your Player.yaml then press enter.  

## Manual Client

In the "Tracker and Locations" tab you'll find buttons corresponding with all the available locations in the Randomizer.  
Since this is a manual game its built on trust™ you press the locations when you get to them,  
hopefully in the futur only what you can access will be visible but at the moment  
you could press victory and it would accept it.

## Main Game

- Launch the game
- Either make a new Profile (maybe call it randomizer) or start a expedition(will wipe the save on the current profile)
- Press new expedition 
    - (or continue expedition if you are loading a save from the randomizer)

# Logic

## Main Game Logic

For now, everything in the "0 - Beginning" category can be accessed from the start.  
- You needs the "launch codes" item to get to the ship.
- Everything that gives a signal need that signal item and the signaloscope item,
- Most "talk to" location require the "Signal > OW Ventures" signal (except for Solanum)
- Going to anything quantum needs the "Signal > Quantum" item (to help with progression)
- all the categories starting with "# - " then a planet name contains everything locations of that planet
- For now no going into Sunless city from a shortcut unless you have "signal > distress"

## Game Troubleshooting

### Items

In doubts look at the items :

#### Needed for GO mode

- "Coords to the eye" in the "Need For End" category 
- "Warp drive" in the "Need For End" category
- "Seen Coords" in the "Visits" category
- "Seen WarpDrive" in the "Visits" category
- "Signaloscope" in the "Tools" and "Signal" categories
- "Scout" in the "Tools" category
- All the [Knowledges](#knowledges)

#### Knowledges  

- "Tornado Knowledge"
- "Jellyfish Knowledge"
- "Teleporter Knowledge"
- "Anglerfish Knowledge"
 
#### Tools   

- "Launch Codes" in the "Tools" category
- "Scout" in the "Tools" category
- "Scout Photos" in the "Tools" category
- "Signaloscope" in the "Tools" and "Signal" categories

#### Bonus

- "Meditation"
- "Landing Camera" in the "Tools" category

#### Signals 
  
- "Signal > OW Ventures"
- "Signal > Quantum"
- "Signal > Distress"
- "Signal > DeepSpace"

#### Quantum   

- "Quantum Rule > imaging"  
    - You need the scout + scout photos to make use of this one.
- "Quantum Rule > entanglement"
- "Quantum Rule > sixth location"
- "Musical Instrument", "count": 5
    - (Currently filler items, Might make those needed for ending if run is too short)

#### TRAPS

- "forced Meditation", "count": 3
    - Ignore if you don't have the "Meditation" item
- "Disabled Ship controls 'Till next loop/meditation", "count": 3
- "Minor Damage to ship", "count": 3
    - You define by yourself what counts as minor/major damage
- "Major Damage to ship", "count": 2

#### Visits

- "Seen Coords"
- "Seen WarpDrive"
- "Seen Solanum"

### Regions

(think of those like super category that have item requirements before you can do any location in them)

#### Tutorial

The one you start in.

#### Space

requires: "Launch Codes"

#### Quantum Trials

requires: "Signal > Quantum", "Signaloscope"

#### Dark Bramble 

requires": "Anglerfish Knowledge"

### Locations

In doubts here are the locations and their respective requirements: 

##### 0 - Beginning

(the [Tutorial](#tutorial) region)
- "'Learn' the Launch Codes in the observatory" 
- "Do the repairs in the Zero-G Cave"
- "Land the model Ship on the small landing pad target thingy"
- "Get in ship for the first time"
    - Always contains a item from the "[Signal](#signals)" category. 

#### Main Game

(Every location below is in the [Space](#space) Region unless state otherwise)

##### 1 - Ash Twin

- "Visit > Get in the Ash Twin Project"
    - requires: "Teleporter Knowledge" 
    - Always contain: "**[Seen WarpDrive](#visits)**"
- "Item > Get in the Ash Twin Project"
    - requires: "Teleporter Knowledge" 
- "Get to the sun station"
    - requires: "Teleporter Knowledge"

##### 1 - Ember Twin

- "Get in the High Energy Lab",
    - requires: "Signaloscope", "Signal > Distress"
- "Break space time in the lab"
    - requires: "Signaloscope", "Signal > Distress"
- "Visit the Eye Shrine in the Sunless City"
    - requires: "Signaloscope", "Signal > Distress"
- "Visit the Quantum Moon Locator"
- "Launch the gravity cannon's ship ET"
- "Talk to Chert"
    - requires: "Signaloscope", "Signal > OW Ventures"
- "Reach the Anglerfish Fossil and read the text left by the Nomai children"
    - requires: "Signaloscope", "Signal > Distress", "Scout"
- "Find Escape Pod 2"
    - requires: "Signaloscope", "Signal > Distress"
- "Find the Cave Shard"
    - **region**: [Quantum Trials](#quantum-trials)
- "Ride Cave Quantum shard and 'learn' the second rule of Quantum"
    - **region**: [Quantum Trials](#quantum-trials)
    - requires: "Quantum Rule > entanglement"

##### 2 - Timber Hearth

- "Visit the Crater with the Bramble seed",
    - **Region**: "Space",
- "Moon > Visit Eye Signal Locator"
- "Visit the Nomai mines and read any Nomain wall"
- "Play Hide and seek with the kids"
    - requires: "Signaloscope"
- "Moon > Talk to Esker"
    - requires: "Signaloscope", "Signal > OW Ventures"
- "Shoot your Scout in the Bramble seed and see the dead Anglerfish"
    - requires: "Scout", "Scout Photos"
- "Find the Museum Shard"
    - **Region**: [Quantum Trials](#quantum-trials)
- "Find the Grove Shard"
    - **Region**: [Quantum Trials](#quantum-trials)
- "Visit the Radio Station and get it's signal"
    - requires: "Signaloscope", "Signal > DeepSpace"

##### 3 - Brittle Hollow

- "Get in Southern Observatory and witness the tornados"
- "Visit the Old Settlement"
- "Visit the Gravity Crystal Workshop"
- "Visit the Classroom in the School District"
- "Launch the gravity cannon's ship BH"
- "Moon > Get inside Hollow's lantern's volcanic testing site"
- "Talk to Riebeck"
    - requires: "Signaloscope", "Signal > OW Ventures"
- "Get in the Blackhole Forge"
    - requires: "Teleporter Knowledge"
- "Find Escape Pod 1"
    - requires: "Signaloscope", "Signal > Distress"  
- "Find the Tower Shard"
    - **Region**: [Quantum Trials](#quantum-trials)
- "Get to the top of the Tower of Quantum Knowledge and 'learn' the third rule of Quantum"
    - **Region**: [Quantum Trials](#quantum-trials)

##### 4 - Giant's Deep

- "Get in Orbital Cannon"
- "Read the log on the Bramble Island"
    - requires: "Scout", "Scout Photos"
- "Read any text wall in the Construction yard"
- "Get in the Statue Island Workshop"
- "Visit the Ocean Depths"
    - requires: "Tornado Knowledge"
- "Visit the Planet's Core"
    - requires: "Tornado Knowledge", "Jellyfish Knowledge"
- "Get the Meditation dialog from Gabbro"
    - requires: "Signaloscope", "Signal > OW Ventures" 
- "Find the Island Shard"
    - **Region**": [Quantum Trials](#quantum-trials),
    - requires: "Quantum Rule > imaging", "Scout", "Scout Photos"
- "Complete the Tower of Quantum Trials"
    - **Region**": [Quantum Trials](#quantum-trials),
    - requires: "Quantum Rule > imaging", "Scout", "Scout Photos"
- "Visit > Get in the Probe Tracking Module and see the Coords to the eye"
    - requires: "Tornado Knowledge", "Jellyfish Knowledge"
    - Always contain: "**[Seen Coords](#visits)**"
- "Item > Get in the Probe Tracking Module and see the Coords to the eye"
    - requires: "Seen Coords", "Tornado Knowledge", "Jellyfish Knowledge"
    - Never Contains a trap.

##### 5 - Dark Bramble

Every location in this category is part of the "[Dark Bramble](#dark-bramble)" region
- "Get through at least 2 nodes and get out alive"
- "Get the Jellyfish dialog from Feldspar"
    - requires: (Signaloscope and Signal > OW Ventures) or Scout 
- "Find Escape Pod 3"
    - requires: "Signaloscope", "Signal > Distress"

##### 6 - Quantum Moon

Every location in this category is part of the "[Quantum Trials](#quantum-trials)" region
- "Land on the Quantum moon"
    - requires: "Quantum Rule > imaging", "Scout", "Scout Photos"
- "Visit Solanum"
    - requires: "Quantum Rule > imaging", "Scout", "Scout Photos",  
    "Quantum Rule > entanglement", "Quantum Rule > sixth location"
    - Always Contains "[Seen Solanum](#visits)"
- "Communicate with Solanum"
    - requires: "Seen Solanum", "Quantum Rule > imaging", "Scout",  
    "Scout Photos", "Quantum Rule > entanglement", "Quantum Rule > sixth location"
  
##### 7 - Interloper

- "Get in Ruptured Core of the Interloper"
    - requires: "Scout", "Scout Photos" 
- "Find the frozen shuttle's log on the Interloper"

#### End Game

- "FINAL > Get the warp drive to the vessel and Warp to the Eye",
    - **Region**: [Dark Bramble](#dark-bramble),
    - requires: "Coords to the eye", "Seen Coords", "Warp drive", "Seen WarpDrive",  
    "Signaloscope", "Signal > Distress", "Scout"
    - Always contain: "1 beautiful campfire song"
- "VICTORY! (seed finished)",
    - **Region**: [Dark Bramble](#dark-bramble),
    - requires: "1 beautiful campfire song",
    - "victory": true
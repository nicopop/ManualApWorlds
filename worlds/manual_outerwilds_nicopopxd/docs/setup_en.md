# Outer Wilds Manual Randomizer Setup Guide

## Required Software

- OuterWilds Game
- The latest Unstable ManualClient

## Installation Procedures

Make sure a copy of the Manual world is in the lib/world directory of your clientside installation.

## Joining a MultiWorld Game

- Launch the client.  
- At the top enter your server's ip with the port provided (by default archipellago.gg:38281).  
- In Manual Game ID put "Manual_OuterWilds_Nicopopxd" then press the Connect button on the top right.  
- In the command field at the bottom enter the name of your slot you choosed in your Player.yaml then press enter.  
## Multiplayer Manual

In the "Tracker and Locations" tab you'll find buttons corresponding with all the available locations in the Randomizer.
Since this is a manual game its built on trust™ you press the locations when you get to them, 
hopefully in the futur only what you can access will be visible but at the moment you could press victory and it would accept it.

For now, everything in the "Beginning" category can be accessed from the start.  
- all the categoies starting with "P - " contains everything locations of that planet
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
#### Knowledges  
- "Tornado Knowledge", "progression": true
- "Jellyfish Knowledge", "progression": true
- "Teleporter Knowledge", "progression": true
- "Anglerfish Knowledge", "progression": true
#### Tools   
- "Launch Codes", "progression": true, "category": ["Basics"]
- "Scout", "progression": true, "category": ["Basics", "Tools"]
- "Scout Photos", "progression": true, "category": ["Basics", "Tools"]
#### Bonus:
- "Meditation", "useful": true, "category": ["Bonus"]
- "Landing Camera", "useful": true, "category": ["Basics", "Bonus", "Tools"]
#### Signals:   
- "Signaloscope", "progression": true, "category": ["Basics", "Tools", "Signal"]
- "Signal > OW Ventures", "progression": true, "category": ["Signal"]
- "Signal > Quantum", "progression": true, "category": ["Signal", "Quantum"]
- "Signal > Distress", "progression": true, "category": ["Signal"]
- "Signal > DeepSpace", "progression": true, "category": ["Signal"]
#### Quantum:   
- "Quantum Rule > imaging", "progression": true, "category": ["Quantum"]
- "Quantum Rule > entanglement", "progression": true, "category": ["Quantum"]
- "Quantum Rule > sixth location", "progression": true, "category": ["Quantum"]
- "Quantum Moon key Fragment", "count": 5
  (Currently filler items, Might make those needed for ending if run is too short)
#### TRAPS:
- "forced Meditation", "count": 3, "category": ["Trap"]
- "Disabled Ship controles 'Till next loop/meditation", "count": 3, "category": ["Trap"]
- "Minor Damage to ship", "count": 3, "category": ["Trap"],
- "Major Damage to ship", "count": 2, "category": ["Trap"],
#### Visits
- "Seen Coords", "progression": true
- "Seen WarpDrive", "progression": true

### Regions
(think of those has super category that have item requirements before you can do any location in them)
- Default or no region  
##### "Space"
  requires: "Launch Codes"
##### "Quantum Trials": 
  requires: "Launch Codes", "Signal > Quantum", "Signaloscope"
##### "Dark Bramble": 
  requires": "Launch Codes", "Anglerfish Knowledge"

### Locations
In doubts here are the locations and their respective requirements: 
#### Start
(the Beginning category)(default region)
- "TH > 'Learn' the Launch Codes in the observatory" 
- "TH > Do the repairs in the Zero-G Cave"
- "TH > Land the model Ship on the small landing pad target thingy"
#### Early Game
- "TH > Get in ship for the first time",
  - **Region**: "Space",
  - "place_item_category": [ "Signal" ]
- "TH > Visit the Crater with the Bramble seed",
  - **Region**: "Space",
- "ET > Get in the High Energy Lab"
  - **Region**: "Space"  
- "ET > Visit the Eye Shrine in the Sunless City",
  - **Region**: "Space",
- "ET > Visit the Quantum Moon Locator",
  - **Region**: "Space",
- "ET > Launch the gravity cannon's ship",
  - **Region**: "Space",
- "ET > Reach the Anglerfish Fossil and read the text left by the Nomai childrens",
  - **Region**: "Space",
  - "requires": "Scout"
- "IN > Get in Ruptured Core of the Interlopper",
  - **Region**: "Space"  
- "GD > Get in Orbital Cannon",
  - **Region**: "Space"  
- "BH > Get in Southern Observatory and witness the tornados",
  - **Region**: "Space"  
- "BH > Visit the Old Settlement",
  - **Region**: "Space",
- "BH > Visit the Gravity Crystal Workshop",
  - **Region**: "Space",
- "BH > Visit the School District of the Hanging City",
  - **Region**: "Space",
- "BH > Launch the gravity cannon's ship",
  - **Region**: "Space",
- "BH > Get inside Hollow's lantern's volcanic testing site",
  - **Region**: "Space"  
- "TH > Visit the Nomai mines and read the already activated Nomain wall",
  - **Region**: "Space"  
- "TH > Play Hide and seek with the kids",
  - **Region**: "Space",
  - "requires": [ "Signaloscope" ]
And more...
#### Peoples    
- "ET > Talk to Chert",  
  - **Region**: "Space",  
  - "requires": "Signaloscope", "Signal > OW Ventures"  
- "TH > Talk to Esker",  
  - **Region**: "Space",  
  - "requires": "Signaloscope", "Signal > OW Ventures"  
- "BH > Talk to Riebeck",  
  - **Region**: "Space",  
  - "requires": "Signaloscope", "Signal > OW Ventures"  
- "GD > Get the Meditation dialog from Gabbro",  
  - **Region**: "Space",  
  - "requires": "Signaloscope", "Signal > OW Ventures"  
- "DB > Get the Jellyfish dialog from Feldspar",  
  - **Region**: "Dark Bramble",  
  - "requires": "Signaloscope", "Signal > OW Ventures", "Scout"  
- "QM > Talk to Solanum",  
  - **Region**: "Quantum Trials",  
  - "requires": "Scout" , "Scout Photos", "Quantum Rule > imaging", "Quantum Rule > entanglement", "Quantum Rule > sixth location"
#### Teleporters
- "AT > Get in the Ash Twin Project",  
  - **Region**: "Space",  
  - "requires": "Teleporter Knowledge"
- "AT > Get to the sun station",  
  - **Region**: "Space",  
  - "requires": "Teleporter Knowledge"
- "BH > Get in the Blackhole Forge",  
  - **Region**: "Space",  
  - "requires": "Teleporter Knowledge"
#### Escape Pods
- "BH > Find Escape Pod 1",  
  - **Region**: "Space",  
  - "requires": "Signaloscope", "Signal > Distress"
- "ET > Find Escape Pod 2",  
  - **Region**: "Space",  
  - "requires": "Signaloscope", "Signal > Distress"
- "DB > Find Escape Pod 3",  
  - **Region**: "Dark Bramble",  
  - "requires": "Signaloscope", "Signal > Distress"
#### Quantum Trials
- "QM > Land on the Quantum moon",  
  - **Region**: "Quantum Trials",  
  - "requires": "Quantum Rule > imaging", "Scout" , "Scout Photos"
- "TH > Find the Museum Shard",  
  - **Region**: "Quantum Trials",  
- "TH > Find the Grove Shard",  
  - **Region**: "Quantum Trials",  
- "ET > Find the Cave Shard",  
  - **Region**: "Quantum Trials",
- "GD > Find the Island Shard",  
  - **Region**: "Quantum Trials",  
  - "requires": "Quantum Rule > imaging", "Scout", "Scout Photos"
- "BH > Find the Tower Shard",  
  - **Region**: "Quantum Trials",  
- "GD > Complete the Tower of Quantum Trials",  
  - **Region**: "Quantum Trials",  
  - "requires": "Quantum Rule > imaging", "Scout", "Scout Photos"  
- "ET > Ride Cave Quantum shard and 'learn' the second rule of Quantum",  
  - **Region**: "Quantum Trials",  
  - "requires": "Quantum Rule > entanglement"  
- "BH > Get to the top of the Tower of Quantum Knowledge and 'learn' the third rule of Quantum",  
  - **Region**: "Quantum Trials",  
#### DeepSpace signal 
(In the DLC edittion this is renamed and reused for the stranger)
- "Space > Visit the deepspace satelite",  
  - **Region**: "Space",  
  - "requires": "Signaloscope", "Signal > DeepSpace"  
- "TH > Visit the Radio Station and get it's signal",  
  - **Region**: "Space",  
  - "requires": "Signaloscope", "Signal > DeepSpace"  
#### End Game
- "Visit > Get in the Probe Tracking Module and see the Coords to the eye",
  - **Region**: "Space",
  - "requires": [ "Tornado Knowledge", "Jellyfish Knowledge" ],
  - "place_item": [ "Seen Coords" ]
- "Item > Get in the Probe Tracking Module and see the Coords to the eye",
  - **Region**: "Space",
  - "requires": [ "Tornado Knowledge", "Jellyfish Knowledge" ]
- "Visit > Get in the Ash Twin Project",
  - **Region**: "Space",
  - "requires": [ "Teleporter Knowledge" ],
  - "place_item": [ "Seen WarpDrive" ]
- "Item > Get in the Ash Twin Project",
  - **Region**: "Space",
  - "category": [ "P - Ash Twin"],
  - "requires": [ "Teleporter Knowledge" ]
- "FINAL > Get the warp drive to the vessel and Warp to the Eye",
  - **Region**: "Dark Bramble",
  -	"requires": "Coords to the eye", "Seen Coords", "Warp drive", "Seen WarpDrive", "Signaloscope", "Signal > Distress", "Scout"
  - "place_item": "1 beautiful campfire song"
- "VICTORY! (seed finished)",
  - **Region**:  "Dark Bramble",
  -	"requires": "1 beautiful campfire song",
  -	"victory": true
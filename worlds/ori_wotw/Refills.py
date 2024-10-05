"""
File generated with `extract_rules.py` with an `areas.wotw` file.

You can find such a file at https://github.com/ori-community/wotw-seedgen/tree/main/wotw_seedgen .

Do not edit manually.
"""


refills = {  # key: region name. List: [health restored, energy restored, refill type]
    # For refill type: 0 is no refill, 1 is Checkpoint, 2 is Full refill.
    "HeaderStates": [0, 0, 0],
    "Teleporters": [0, 0, 0],
    "MarshSpawn.Main": [0, 0, 2],
    "MarshSpawn.OpherBarrier": [0, 0, 1],
    "MarshSpawn.BrokenBridge": [0, 0, 1],
    "MarshSpawn.CaveEntrance": [0, 0, 1],
    "MarshSpawn.Cave": [1, 0, 1],
    "MarshSpawn.BurrowFightArena": [1, 0, 0],
    "MarshSpawn.LifepactLedge": [0, 0, 0],
    "MarshSpawn.PoolsBurrowsSignpost": [0, 1, 1],
    "MarshSpawn.BeforeBurrows": [0, 0, 1],
    "MarshSpawn.BurrowsEntry": [0, 0, 1],
    "MarshSpawn.LeftSpawnSignpost": [0, 0, 1],
    "MarshSpawn.PoolsPath": [0, 0, 1],
    "MarshSpawn.RegenDoor": [0, 0, 0],
    "MarshSpawn.HowlApproach": [0, 0, 1],
    "MarshSpawn.MokkTheBrave": [0, 0, 0],
    "MarshSpawn.AboveHowlArena": [1, 0, 1],
    "MarshSpawn.FangPlatform": [1, 0, 0],
    "MarshSpawn.HowlsDenEntrance": [0, 0, 0],
    "HowlsDen.UpperLoopExit": [1, 0, 1],
    "HowlsDen.AboveBoneBridge": [0, 0, 1],
    "HowlsDen.UpperLoopEntrance": [0, 0, 1],
    "HowlsDen.BoneBridge": [0, 0, 1],
    "HowlsDen.BoneBridgeDoor": [0, 0, 1],
    "HowlsDen.OutsideSecretRoom": [0, 0, 0],
    "HowlsDen.MidwayBottomLoop": [1, 0, 0],
    "HowlsDen.SecretRoom": [0, 0, 1],
    "HowlsDen.LeftSecretRoom": [0, 0, 0],
    "HowlsDen.AboveTeleporter": [0, 0, 0],
    "HowlsDen.Teleporter": [0, 0, 2],
    "HowlsDen.DoubleJumpApproach": [0, 0, 1],
    "HowlsDen.DoubleJumpTreeLedge": [0, 0, 1],
    "HowlsDen.DoubleJumpTreeArea": [0, 0, 0],
    "DenShrine": [0, 0, 2],
    "MarshPastOpher.MillView": [0, 3, 1],
    "MarshPastOpher.OpherSkipBranch": [0, 0, 0],
    "MarshPastOpher.TrialStart": [0, 0, 1],
    "MarshPastOpher.UnderTrunk": [0, 0, 1],
    "MarshPastOpher.TrialArea": [1, 0, 1],
    "MarshShrine": [0, 0, 2],
    "MarshPastOpher.BowPath": [1, 1, 1],
    "MarshPastOpher.BowApproach": [1, 0, 1],
    "MarshPastOpher.BowArea": [0, 1, 0],
    "MarshPastOpher.UpperBowArea": [0, 1, 1],
    "MarshPastOpher.PoolsPathEast": [1, 3, 1],
    "MarshPastOpher.PoolsPathMiddle": [0, 0, 1],
    "MarshPastOpher.PoolsPathOneWayWall": [0, 0, 1],
    "MarshPastOpher.PoolsPathBellowOneWayWall": [0, 0, 0],
    "MarshPastOpher.PoolsPathWest": [0, 0, 1],
    "MidnightBurrows.Teleporter": [0, 0, 2],
    "MidnightBurrows.BelowLupo": [0, 0, 0],
    "MidnightBurrows.Central": [0, 0, 1],
    "MidnightBurrows.TabletRoom": [1, 0, 1],
    "MidnightBurrows.PortalRoom": [0, 0, 1],
    "MidnightBurrows.LeverRoom": [0, 0, 1],
    "MidnightBurrows.East": [0, 0, 1],
    "MidnightBurrows.DenConnection": [0, 0, 1],
    "MidnightBurrows.PortalCorridor": [0, 0, 1],
    "MidnightBurrows.BelowUpperKS": [0, 0, 0],
    "WestHollow.Entrance": [0, 3, 1],
    "WestHollow.MokiByTwillen": [1, 0, 0],
    "WestHollow.InFrontPurpleDoor": [0, 0, 0],
    "WestHollow.InFrontPurpleDoorEnemyPaths": [0, 0, 0],
    "WestHollow.HollowDrainMiddle": [0, 3, 1],
    "WestHollow.RockPuzzle": [1, 3, 1],
    "WestHollow.FarLeftRoom": [0, 3, 0],
    "WestHollow.SubmergedPlatform": [0, 1, 0],
    "WestHollow.AboveJumppad": [0, 0, 0],
    "WestHollow.HollowDrainLower": [0, 0, 1],
    "WestHollow.TrialApproach": [0, 0, 1],
    "WestHollow.TrialStart": [0, 0, 1],
    "WestHollow.PolesPound": [0, 0, 1],
    "WestHollow.DashApproach": [0, 3, 1],
    "WestHollow.DashArea": [0, 0, 1],
    "WestHollow.DashCrushers": [0, 0, 1],
    "WestHollow.DashRoomTopRight": [0, 0, 1],
    "WestHollow.AboveDashSemisolid": [0, 0, 0],
    "EastHollow.Teleporter": [0, 0, 2],
    "BeetleFight": [0, 0, 2],
    "EastHollow.VoiceDoorPlatform": [0, 0, 0],
    "EastHollow.MapMoki": [0, 0, 1],
    "EastHollow.OutsideGlades": [0, 0, 0],
    "EastHollow.AfterBeetleFight": [0, 0, 1],
    "EastHollow.AboveBash": [0, 0, 0],
    "EastHollow.BashTreeCheckpoint": [0, 0, 1],
    "EastHollow.Kwolok": [0, 0, 1],
    "EastHollow.AboveDepths": [0, 3, 1],
    "GladesTown.Teleporter": [0, 0, 2],
    "GladesTown.TwillenHome": [0, 0, 1],
    "GladesTown.West": [0, 0, 1],
    "GladesTown.MotayHut": [0, 0, 1],
    "GladesTown.UpperWest": [0, 0, 1],
    "GladesTown.AcornMoki": [0, 4, 1],
    "GladesTown.BelowBountyShard": [0, 0, 0],
    "GladesTown.LeftAboveCoals": [0, 0, 0],
    "GladesTown.AboveOpher": [0, 0, 1],
    "GladesTown.PlayfulMoki": [0, 0, 0],
    "GladesTown.LupoHouse": [0, 0, 0],
    "GladesTown.HoleHut": [0, 0, 0],
    "GladesTown.HoleHutEntrance": [0, 0, 1],
    "WestGlades.PastTown": [0, 3, 1],
    "WestGlades.LowerPool": [0, 0, 0],
    "WestGlades.Center": [0, 0, 1],
    "WestGlades.Upper": [1, 0, 1],
    "WestGlades.MillApproach": [1, 0, 1],
    "WestGlades.ShrineArea": [0, 0, 1],
    "GladesShrine": [0, 0, 2],
    "OuterWellspring.EntranceDoor": [1, 3, 1],
    "OuterWellspring.LifeHarvestEntry": [0, 0, 0],
    "OuterWellspring.Basement": [0, 0, 0],
    "OuterWellspring.AboveEntranceDoor": [0, 3, 0],
    "OuterWellspring.WestDoor": [0, 0, 1],
    "OuterWellspring.EastDoor": [0, 0, 1],
    "OuterWellspring.AboveWestDoor": [0, 3, 0],
    "OuterWellspring.TopDoor": [0, 0, 0],
    "OuterWellspring.RightWallMidpoint": [0, 0, 0],
    "OuterWellspring.TrialApproach": [0, 0, 1],
    "OuterWellspring.TrialRoom": [1, 1, 1],
    "OuterWellspring.TrialStart": [0, 0, 1],
    "InnerWellspring.EntranceDoor": [0, 3, 1],
    "InnerWellspring.ThornShardArea": [0, 0, 1],
    "InnerWellspring.ShortcutLever": [0, 0, 0],
    "InnerWellspring.DrainRoom": [0, 3, 1],
    "InnerWellspring.DrainAreaEntrance": [0, 0, 0],
    "InnerWellspring.DrainAreaEX": [0, 0, 0],
    "InnerWellspring.DrainAreaExit": [0, 0, 1],
    "InnerWellspring.DrainRoomCenter": [0, 0, 0],
    "InnerWellspring.DrainRoomTop": [1, 0, 1],
    "InnerWellspring.BelowDrainLever": [0, 0, 1],
    "InnerWellspring.AbovePole": [0, 0, 0],
    "InnerWellspring.WestDoor": [2, 3, 1],
    "InnerWellspring.EastDoor": [1, 4, 1],
    "InnerWellspring.SpinPuzzle": [0, 0, 1],
    "InnerWellspring.PastSpinPuzzle": [0, 0, 1],
    "InnerWellspring.GrappleThroughZigZagSpikes": [0, 0, 1],
    "InnerWellspring.TopSecondRoom": [0, 0, 0],
    "InnerWellspring.Teleporter": [0, 0, 2],
    "InnerWellspring.EscapeSequence": [0, 0, 2],
    "WoodsEntry.ShriekMeet": [0, 0, 1],
    "WoodsEntry.FirstMud": [0, 0, 1],
    "WoodsEntry.BelowTeleporter": [0, 0, 1],
    "WoodsEntry.Teleporter": [0, 0, 2],
    "WoodsEntry.TwoKeystoneRoom": [0, 3, 1],
    "WoodsMain.AfterKuMeet": [0, 0, 1],
    "WoodsMain.BelowFourKeystoneRoom": [0, 0, 0],
    "WoodsMain.WallOreLedge": [0, 0, 0],
    "WoodsMain.FourKeystoneRoom": [0, 0, 1],
    "WoodsMain.GiantSkull": [0, 0, 1],
    "WoodsMain.BalloonLure": [0, 0, 1],
    "WoodsMain.BelowHiddenOre": [0, 0, 0],
    "WoodsMain.PetrifiedHowl": [1, 0, 1],
    "WoodsMain.BrokenOwl": [0, 0, 1],
    "WoodsMain.TrialStart": [0, 0, 1],
    "WoodsMain.MidwayTrial": [0, 0, 1],
    "WoodsMain.TrialEnd": [0, 0, 1],
    "WoodsMain.AboveHowl": [0, 0, 0],
    "WoodsMain.BeforeLog": [0, 0, 1],
    "WoodsMain.Teleporter": [0, 0, 2],
    "WoodsMain.OrangeTree": [0, 0, 0],
    "WoodsMain.AbovePit": [0, 3, 0],
    "WoodsMain.FeedingGrounds": [0, 0, 1],
    "WoodsShrine": [0, 0, 2],
    "LowerReach.Entry": [1, 0, 1],
    "LowerReach.AboveEntry": [0, 0, 1],
    "LowerReach.Icefall": [0, 3, 1],
    "LowerReach.CentralEnemyPaths": [0, 0, 1],
    "LowerReach.Central": [0, 0, 0],
    "LowerReach.OutsideTPRoom": [1, 3, 2],
    "LowerReach.BelowTokk": [0, 0, 1],
    "LowerReach.Teleporter": [0, 0, 2],
    "LowerReach.SecondSoup": [0, 0, 0],
    "LowerReach.BelowLupo": [0, 0, 0],
    "LowerReach.CentralFurnacePedestal": [0, 3, 1],
    "LowerReach.WindChannel": [0, 0, 1],
    "LowerReach.SoupMoki": [0, 4, 0],
    "LowerReach.EastEnemyPaths": [0, 0, 2],
    "LowerReach.East": [0, 0, 0],
    "LowerReach.SnowballEnemyPaths": [0, 0, 1],
    "LowerReach.Snowball": [0, 0, 0],
    "LowerReach.PastSnowball": [0, 4, 1],
    "LowerReach.IceCavern": [0, 0, 0],
    "LowerReach.HalfwayIceCavern": [0, 0, 0],
    "LowerReach.SwimmingPool": [0, 4, 0],
    "LowerReach.EastFurnace": [0, 0, 1],
    "LowerReach.ArenaArea": [1, 3, 1],
    "LowerReach.WindSpinners": [0, 0, 0],
    "LowerReach.WispPathCheckpoint": [1, 4, 1],
    "LowerReach.BridgeWispPath": [0, 0, 1],
    "LowerReach.SnowEscape": [0, 0, 2],
    "LowerReach.VeralHome": [0, 0, 1],
    "LowerReach.TownEntry": [0, 0, 0],
    "LowerReach.TrialStart": [0, 0, 1],
    "UpperReach.BurrowArea": [0, 0, 0],
    "UpperReach.KeystoneRoom": [0, 0, 1],
    "UpperReach.KeystoneSnapPlant": [0, 0, 0],
    "UpperReach.KeystoneSnapPlantThawed": [0, 0, 0],
    "UpperReach.KeystoneSnapPlantPaths": [0, 0, 0],
    "UpperReach.KeystoneSnapPlantThawedPaths": [0, 0, 0],
    "UpperReach.UpperSoup": [0, 0, 0],
    "UpperReach.UpperSoupFrozen": [0, 0, 0],
    "UpperReach.UpperSoupThawed": [0, 0, 0],
    "UpperReach.UpperSoupPaths": [1, 0, 1],
    "UpperReach.UpperSoupFrozenPaths": [0, 0, 1],
    "UpperReach.UpperSoupThawedPaths": [0, 0, 1],
    "UpperReach.OutsideTreeRoom": [0, 3, 1],
    "UpperReach.TreeRoomLedge": [0, 0, 0],
    "UpperReach.TreeRoom": [0, 4, 1],
    "UpperDepths.Entry": [0, 0, 0],
    "UpperDepths.FirstFirefly": [0, 0, 1],
    "UpperDepths.FirstKSRoom": [0, 3, 1],
    "UpperDepths.KeydoorLedge": [0, 0, 1],
    "UpperDepths.RightKeystonePath": [0, 0, 1],
    "UpperDepths.BelowHive": [0, 3, 2],
    "UpperDepths.Teleporter": [0, 0, 2],
    "UpperDepths.Central": [0, 3, 1],
    "UpperDepths.SecondKSRoom": [0, 4, 1],
    "UpperDepths.MoraPath": [0, 3, 1],
    "UpperDepths.OutsideMoraFight": [0, 0, 1],
    "MoraFirstPhase": [0, 0, 2],
    "MoraEscape": [0, 0, 1],
    "MoraSecondPhase": [0, 3, 1],
    "UpperDepths.LowerConnection": [0, 0, 1],
    "LowerDepths.West": [1, 3, 1],
    "DepthsShrine": [0, 0, 2],
    "LowerDepths.Central": [0, 0, 1],
    "LowerDepths.East": [0, 3, 1],
    "LowerDepths.BeforeTree": [0, 0, 1],
    "LowerDepths.TreeArea": [0, 4, 1],
    "PoolsApproach.MillPathCheckpoint": [0, 0, 1],
    "PoolsApproach.MillPath": [0, 0, 1],
    "PoolsApproach.MarshBreakableWall": [0, 0, 0],
    "PoolsApproach.OnTopOfWheel": [0, 0, 1],
    "EastPools.LeverRoom": [1, 0, 1],
    "EastPools.BehindEntryDoor": [0, 0, 1],
    "EastPools.TokkBubble": [0, 0, 1],
    "EastPools.TPArea": [0, 0, 2],
    "EastPools.Teleporter": [0, 0, 2],
    "EastPools.FishingPool": [0, 0, 0],
    "EastPools.AboveFishingPool": [0, 0, 0],
    "EastPools.NextToLupoOre": [0, 0, 1],
    "EastPools.LupoArea": [0, 0, 1],
    "EastPools.WaterdashArena": [0, 0, 1],
    "EastPools.MissilePuzzle": [0, 0, 1],
    "EastPools.CentralRoom": [0, 0, 1],
    "UpperPools.KeystoneRoomEntrance": [0, 0, 1],
    "UpperPools.KeystoneRoomBubbleSpawner": [0, 0, 1],
    "UpperPools.KeystoneRoom": [0, 3, 1],
    "UpperPools.BeforeKeystoneDoor": [1, 0, 1],
    "UpperPools.TreeRoomEntrance": [0, 0, 1],
    "UpperPools.TreeRoom": [0, 0, 0],
    "UpperPools.AboveTree": [0, 0, 0],
    "UpperPools.DrainPuzzleEntrance": [0, 0, 1],
    "UpperPools.DrainPuzzleRight": [1, 3, 0],
    "UpperPools.DrainPuzzleExit": [0, 0, 1],
    "UpperPools.RightBubbleSpamRoom": [0, 0, 1],
    "UpperPools.LeftBubbleSpamRoom": [0, 0, 1],
    "WestPools.Teleporter": [0, 0, 2],
    "WestPools.LeftKwolokPlatform": [0, 0, 1],
    "WestPools.RightKwolokPlatform": [0, 0, 1],
    "KwolokEscape": [0, 0, 2],
    "KwolokFight": [0, 3, 1],
    "LowerWastes.WestTP": [0, 0, 2],
    "LowerWastes.SunsetView": [0, 0, 1],
    "LowerWastes.Shovel": [0, 3, 0],
    "LowerWastes.MuncherTunnel": [0, 3, 1],
    "LowerWastes.SandPot": [0, 0, 1],
    "LowerWastes.WoodenBridge": [0, 0, 1],
    "LowerWastes.BeforeMinesEntrance": [0, 0, 0],
    "LowerWastes.MinesEntranceEnemyPaths": [0, 0, 0],
    "LowerWastes.MinesEntrance": [0, 0, 0],
    "LowerWastes.LeverArea": [0, 3, 1],
    "LowerWastes.MuncherClimb": [0, 0, 1],
    "LowerWastes.LastStandArea": [0, 0, 0],
    "LowerWastes.SkeetoHive": [0, 0, 1],
    "LowerWastes.ThirstyGorlek": [0, 0, 1],
    "LowerWastes.UpperPath": [0, 3, 1],
    "LowerWastes.EastTP": [0, 0, 2],
    "UpperWastes.KeystoneRoom": [0, 0, 1],
    "UpperWastes.MissilePuzzleLeft": [0, 0, 1],
    "UpperWastes.MissilePuzzleMiddle": [0, 0, 1],
    "UpperWastes.MissilePuzzleRight": [0, 0, 0],
    "UpperWastes.SpinLasers": [0, 0, 1],
    "UpperWastes.RuinsApproach": [0, 0, 1],
    "UpperWastes.NorthTP": [0, 0, 2],
    "UpperWastes.OutsideRuins": [0, 0, 1],
    "WindtornRuins.UpperRuinsDoor": [0, 3, 1],
    "WindtornRuins.BrokenMural": [0, 0, 1],
    "WindtornRuins.FallenPillar": [0, 0, 0],
    "WindtornRuins.RuinsTP": [0, 0, 2],
    "WindtornRuins.Escape": [0, 0, 2],
    "WindtornRuins.LowerRuins": [0, 0, 0],
    "WeepingRidge.Bottom": [1, 3, 1],
    "WeepingRidge.LaunchArea": [1, 0, 1],
    "WeepingRidge.AboveTree": [0, 0, 1],
    "WillowsEnd.Entry": [0, 4, 1],
    "WillowsEnd.GrappleHeartMidPoint": [1, 0, 1],
    "WillowsEnd.GrappleHeart": [1, 3, 1],
    "WillowsEnd.BoulderHeartPath": [0, 3, 1],
    "WillowsEnd.InnerTP": [0, 0, 2],
    "WillowsEnd.AboveInnerTP": [0, 4, 1],
    "WillowsEnd.East": [0, 0, 0],
    "WillowsEnd.RedirectHeartPath": [1, 4, 0],
    "WillowsEnd.RedirectHeartPuzzle": [0, 0, 1],
    "WillowsEnd.Upper": [0, 4, 1],
    "WillowsEnd.West": [0, 4, 1],
    "WillowsEnd.GlideHeartPath": [1, 0, 1],
    "WillowsEnd.GlideRooms": [0, 4, 1],
    "WillowsEnd.UpperHeartPath": [0, 4, 1],
    "WillowsEnd.UpperHeartCheckpoint": [0, 0, 1],
    "Tokk": [0, 0, 0],
    "TwillenShop": [0, 0, 0],
    "OpherShop": [0, 0, 0],
    "TuleyShop": [0, 0, 0]
    }

refill_events = [
    "F.MarshSpawn.Main",
    "C.MarshSpawn.OpherBarrier",
    "C.MarshSpawn.BrokenBridge",
    "C.MarshSpawn.CaveEntrance",
    "C.MarshSpawn.Cave",
    "H.MarshSpawn.Cave",
    "H.MarshSpawn.BurrowFightArena",
    "C.MarshSpawn.PoolsBurrowsSignpost",
    "E.MarshSpawn.PoolsBurrowsSignpost",
    "C.MarshSpawn.BeforeBurrows",
    "C.MarshSpawn.BurrowsEntry",
    "C.MarshSpawn.LeftSpawnSignpost",
    "C.MarshSpawn.PoolsPath",
    "C.MarshSpawn.HowlApproach",
    "C.MarshSpawn.AboveHowlArena",
    "H.MarshSpawn.AboveHowlArena",
    "H.MarshSpawn.FangPlatform",
    "C.HowlsDen.UpperLoopExit",
    "H.HowlsDen.UpperLoopExit",
    "C.HowlsDen.AboveBoneBridge",
    "C.HowlsDen.UpperLoopEntrance",
    "C.HowlsDen.BoneBridge",
    "C.HowlsDen.BoneBridgeDoor",
    "H.HowlsDen.MidwayBottomLoop",
    "C.HowlsDen.SecretRoom",
    "F.HowlsDen.Teleporter",
    "C.HowlsDen.DoubleJumpApproach",
    "C.HowlsDen.DoubleJumpTreeLedge",
    "F.DenShrine",
    "C.MarshPastOpher.MillView",
    "E.MarshPastOpher.MillView",
    "C.MarshPastOpher.TrialStart",
    "C.MarshPastOpher.UnderTrunk",
    "C.MarshPastOpher.TrialArea",
    "H.MarshPastOpher.TrialArea",
    "F.MarshShrine",
    "C.MarshPastOpher.BowPath",
    "H.MarshPastOpher.BowPath",
    "E.MarshPastOpher.BowPath",
    "C.MarshPastOpher.BowApproach",
    "H.MarshPastOpher.BowApproach",
    "E.MarshPastOpher.BowArea",
    "C.MarshPastOpher.UpperBowArea",
    "E.MarshPastOpher.UpperBowArea",
    "C.MarshPastOpher.PoolsPathEast",
    "H.MarshPastOpher.PoolsPathEast",
    "E.MarshPastOpher.PoolsPathEast",
    "C.MarshPastOpher.PoolsPathMiddle",
    "C.MarshPastOpher.PoolsPathOneWayWall",
    "C.MarshPastOpher.PoolsPathWest",
    "F.MidnightBurrows.Teleporter",
    "C.MidnightBurrows.Central",
    "C.MidnightBurrows.TabletRoom",
    "H.MidnightBurrows.TabletRoom",
    "C.MidnightBurrows.PortalRoom",
    "C.MidnightBurrows.LeverRoom",
    "C.MidnightBurrows.East",
    "C.MidnightBurrows.DenConnection",
    "C.MidnightBurrows.PortalCorridor",
    "C.WestHollow.Entrance",
    "E.WestHollow.Entrance",
    "H.WestHollow.MokiByTwillen",
    "C.WestHollow.HollowDrainMiddle",
    "E.WestHollow.HollowDrainMiddle",
    "C.WestHollow.RockPuzzle",
    "H.WestHollow.RockPuzzle",
    "E.WestHollow.RockPuzzle",
    "E.WestHollow.FarLeftRoom",
    "E.WestHollow.SubmergedPlatform",
    "C.WestHollow.HollowDrainLower",
    "C.WestHollow.TrialApproach",
    "C.WestHollow.TrialStart",
    "C.WestHollow.PolesPound",
    "C.WestHollow.DashApproach",
    "E.WestHollow.DashApproach",
    "C.WestHollow.DashArea",
    "C.WestHollow.DashCrushers",
    "C.WestHollow.DashRoomTopRight",
    "F.EastHollow.Teleporter",
    "F.BeetleFight",
    "C.EastHollow.MapMoki",
    "C.EastHollow.AfterBeetleFight",
    "C.EastHollow.BashTreeCheckpoint",
    "C.EastHollow.Kwolok",
    "C.EastHollow.AboveDepths",
    "E.EastHollow.AboveDepths",
    "F.GladesTown.Teleporter",
    "C.GladesTown.TwillenHome",
    "C.GladesTown.West",
    "C.GladesTown.MotayHut",
    "C.GladesTown.UpperWest",
    "C.GladesTown.AcornMoki",
    "E.GladesTown.AcornMoki",
    "C.GladesTown.AboveOpher",
    "C.GladesTown.HoleHutEntrance",
    "C.WestGlades.PastTown",
    "E.WestGlades.PastTown",
    "C.WestGlades.Center",
    "C.WestGlades.Upper",
    "H.WestGlades.Upper",
    "C.WestGlades.MillApproach",
    "H.WestGlades.MillApproach",
    "C.WestGlades.ShrineArea",
    "F.GladesShrine",
    "C.OuterWellspring.EntranceDoor",
    "H.OuterWellspring.EntranceDoor",
    "E.OuterWellspring.EntranceDoor",
    "E.OuterWellspring.AboveEntranceDoor",
    "C.OuterWellspring.WestDoor",
    "C.OuterWellspring.EastDoor",
    "E.OuterWellspring.AboveWestDoor",
    "C.OuterWellspring.TrialApproach",
    "C.OuterWellspring.TrialRoom",
    "H.OuterWellspring.TrialRoom",
    "E.OuterWellspring.TrialRoom",
    "C.OuterWellspring.TrialStart",
    "C.InnerWellspring.EntranceDoor",
    "E.InnerWellspring.EntranceDoor",
    "C.InnerWellspring.ThornShardArea",
    "C.InnerWellspring.DrainRoom",
    "E.InnerWellspring.DrainRoom",
    "C.InnerWellspring.DrainAreaExit",
    "C.InnerWellspring.DrainRoomTop",
    "H.InnerWellspring.DrainRoomTop",
    "C.InnerWellspring.BelowDrainLever",
    "C.InnerWellspring.WestDoor",
    "H.InnerWellspring.WestDoor",
    "E.InnerWellspring.WestDoor",
    "C.InnerWellspring.EastDoor",
    "H.InnerWellspring.EastDoor",
    "E.InnerWellspring.EastDoor",
    "C.InnerWellspring.SpinPuzzle",
    "C.InnerWellspring.PastSpinPuzzle",
    "C.InnerWellspring.GrappleThroughZigZagSpikes",
    "F.InnerWellspring.Teleporter",
    "F.InnerWellspring.EscapeSequence",
    "C.WoodsEntry.ShriekMeet",
    "C.WoodsEntry.FirstMud",
    "C.WoodsEntry.BelowTeleporter",
    "F.WoodsEntry.Teleporter",
    "C.WoodsEntry.TwoKeystoneRoom",
    "E.WoodsEntry.TwoKeystoneRoom",
    "C.WoodsMain.AfterKuMeet",
    "C.WoodsMain.FourKeystoneRoom",
    "C.WoodsMain.GiantSkull",
    "C.WoodsMain.BalloonLure",
    "C.WoodsMain.PetrifiedHowl",
    "H.WoodsMain.PetrifiedHowl",
    "C.WoodsMain.BrokenOwl",
    "C.WoodsMain.TrialStart",
    "C.WoodsMain.MidwayTrial",
    "C.WoodsMain.TrialEnd",
    "C.WoodsMain.BeforeLog",
    "F.WoodsMain.Teleporter",
    "E.WoodsMain.AbovePit",
    "C.WoodsMain.FeedingGrounds",
    "F.WoodsShrine",
    "C.LowerReach.Entry",
    "H.LowerReach.Entry",
    "C.LowerReach.AboveEntry",
    "C.LowerReach.Icefall",
    "E.LowerReach.Icefall",
    "C.LowerReach.CentralEnemyPaths",
    "C.LowerReach.OutsideTPRoom",
    "F.LowerReach.OutsideTPRoom",
    "H.LowerReach.OutsideTPRoom",
    "E.LowerReach.OutsideTPRoom",
    "C.LowerReach.BelowTokk",
    "F.LowerReach.Teleporter",
    "C.LowerReach.CentralFurnacePedestal",
    "E.LowerReach.CentralFurnacePedestal",
    "C.LowerReach.WindChannel",
    "E.LowerReach.SoupMoki",
    "F.LowerReach.EastEnemyPaths",
    "C.LowerReach.SnowballEnemyPaths",
    "C.LowerReach.PastSnowball",
    "E.LowerReach.PastSnowball",
    "E.LowerReach.SwimmingPool",
    "C.LowerReach.EastFurnace",
    "C.LowerReach.ArenaArea",
    "H.LowerReach.ArenaArea",
    "E.LowerReach.ArenaArea",
    "C.LowerReach.WispPathCheckpoint",
    "H.LowerReach.WispPathCheckpoint",
    "E.LowerReach.WispPathCheckpoint",
    "C.LowerReach.BridgeWispPath",
    "F.LowerReach.SnowEscape",
    "C.LowerReach.VeralHome",
    "C.LowerReach.TrialStart",
    "C.UpperReach.KeystoneRoom",
    "C.UpperReach.UpperSoupPaths",
    "H.UpperReach.UpperSoupPaths",
    "C.UpperReach.UpperSoupFrozenPaths",
    "C.UpperReach.UpperSoupThawedPaths",
    "C.UpperReach.OutsideTreeRoom",
    "E.UpperReach.OutsideTreeRoom",
    "C.UpperReach.TreeRoom",
    "E.UpperReach.TreeRoom",
    "C.UpperDepths.FirstFirefly",
    "C.UpperDepths.FirstKSRoom",
    "E.UpperDepths.FirstKSRoom",
    "C.UpperDepths.KeydoorLedge",
    "C.UpperDepths.RightKeystonePath",
    "C.UpperDepths.BelowHive",
    "F.UpperDepths.BelowHive",
    "E.UpperDepths.BelowHive",
    "F.UpperDepths.Teleporter",
    "C.UpperDepths.Central",
    "E.UpperDepths.Central",
    "C.UpperDepths.SecondKSRoom",
    "E.UpperDepths.SecondKSRoom",
    "C.UpperDepths.MoraPath",
    "E.UpperDepths.MoraPath",
    "C.UpperDepths.OutsideMoraFight",
    "F.MoraFirstPhase",
    "C.MoraEscape",
    "C.MoraSecondPhase",
    "E.MoraSecondPhase",
    "C.UpperDepths.LowerConnection",
    "C.LowerDepths.West",
    "H.LowerDepths.West",
    "E.LowerDepths.West",
    "F.DepthsShrine",
    "C.LowerDepths.Central",
    "C.LowerDepths.East",
    "E.LowerDepths.East",
    "C.LowerDepths.BeforeTree",
    "C.LowerDepths.TreeArea",
    "E.LowerDepths.TreeArea",
    "C.PoolsApproach.MillPathCheckpoint",
    "C.PoolsApproach.MillPath",
    "C.PoolsApproach.OnTopOfWheel",
    "C.EastPools.LeverRoom",
    "H.EastPools.LeverRoom",
    "C.EastPools.BehindEntryDoor",
    "C.EastPools.TokkBubble",
    "C.EastPools.TPArea",
    "F.EastPools.TPArea",
    "F.EastPools.Teleporter",
    "C.EastPools.NextToLupoOre",
    "C.EastPools.LupoArea",
    "C.EastPools.WaterdashArena",
    "C.EastPools.MissilePuzzle",
    "C.EastPools.CentralRoom",
    "C.UpperPools.KeystoneRoomEntrance",
    "C.UpperPools.KeystoneRoomBubbleSpawner",
    "C.UpperPools.KeystoneRoom",
    "E.UpperPools.KeystoneRoom",
    "C.UpperPools.BeforeKeystoneDoor",
    "H.UpperPools.BeforeKeystoneDoor",
    "C.UpperPools.TreeRoomEntrance",
    "C.UpperPools.DrainPuzzleEntrance",
    "E.UpperPools.DrainPuzzleRight",
    "H.UpperPools.DrainPuzzleRight",
    "C.UpperPools.DrainPuzzleExit",
    "C.UpperPools.RightBubbleSpamRoom",
    "C.UpperPools.LeftBubbleSpamRoom",
    "F.WestPools.Teleporter",
    "C.WestPools.LeftKwolokPlatform",
    "C.WestPools.RightKwolokPlatform",
    "F.KwolokEscape",
    "C.KwolokFight",
    "E.KwolokFight",
    "F.LowerWastes.WestTP",
    "C.LowerWastes.SunsetView",
    "E.LowerWastes.Shovel",
    "C.LowerWastes.MuncherTunnel",
    "E.LowerWastes.MuncherTunnel",
    "C.LowerWastes.SandPot",
    "C.LowerWastes.WoodenBridge",
    "C.LowerWastes.LeverArea",
    "E.LowerWastes.LeverArea",
    "C.LowerWastes.MuncherClimb",
    "C.LowerWastes.SkeetoHive",
    "C.LowerWastes.ThirstyGorlek",
    "C.LowerWastes.UpperPath",
    "E.LowerWastes.UpperPath",
    "F.LowerWastes.EastTP",
    "C.UpperWastes.KeystoneRoom",
    "C.UpperWastes.MissilePuzzleLeft",
    "C.UpperWastes.MissilePuzzleMiddle",
    "C.UpperWastes.SpinLasers",
    "C.UpperWastes.RuinsApproach",
    "F.UpperWastes.NorthTP",
    "C.UpperWastes.OutsideRuins",
    "C.WindtornRuins.UpperRuinsDoor",
    "E.WindtornRuins.UpperRuinsDoor",
    "C.WindtornRuins.BrokenMural",
    "F.WindtornRuins.RuinsTP",
    "F.WindtornRuins.Escape",
    "C.WeepingRidge.Bottom",
    "H.WeepingRidge.Bottom",
    "E.WeepingRidge.Bottom",
    "C.WeepingRidge.LaunchArea",
    "H.WeepingRidge.LaunchArea",
    "C.WeepingRidge.AboveTree",
    "C.WillowsEnd.Entry",
    "E.WillowsEnd.Entry",
    "C.WillowsEnd.GrappleHeartMidPoint",
    "H.WillowsEnd.GrappleHeartMidPoint",
    "C.WillowsEnd.GrappleHeart",
    "E.WillowsEnd.GrappleHeart",
    "H.WillowsEnd.GrappleHeart",
    "C.WillowsEnd.BoulderHeartPath",
    "E.WillowsEnd.BoulderHeartPath",
    "F.WillowsEnd.InnerTP",
    "C.WillowsEnd.AboveInnerTP",
    "E.WillowsEnd.AboveInnerTP",
    "H.WillowsEnd.RedirectHeartPath",
    "E.WillowsEnd.RedirectHeartPath",
    "C.WillowsEnd.RedirectHeartPuzzle",
    "C.WillowsEnd.Upper",
    "E.WillowsEnd.Upper",
    "C.WillowsEnd.West",
    "E.WillowsEnd.West",
    "C.WillowsEnd.GlideHeartPath",
    "H.WillowsEnd.GlideHeartPath",
    "C.WillowsEnd.GlideRooms",
    "E.WillowsEnd.GlideRooms",
    "C.WillowsEnd.UpperHeartPath",
    "E.WillowsEnd.UpperHeartPath",
    "C.WillowsEnd.UpperHeartCheckpoint"
    ]

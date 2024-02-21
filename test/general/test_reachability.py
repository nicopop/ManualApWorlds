import unittest

from BaseClasses import CollectionState
from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    gen_steps = ["generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill"]

    default_settings_unreachable_regions = {
        "A Link to the Past": {
            "Chris Houlihan Room",  # glitch room by definition
            "Desert Northern Cliffs",  # on top of mountain, only reachable via OWG
            "Dark Death Mountain Bunny Descent Area"  # OWG Mountain descent
        },
        "Ocarina of Time": {
            "Prelude of Light Warp",  # Prelude is not progression by default
            "Serenade of Water Warp",  # Serenade is not progression by default
            "Lost Woods Mushroom Timeout",  # trade quest starts after this item
            "ZD Eyeball Frog Timeout",  # trade quest starts after this item
            "ZR Top of Waterfall",  # dummy region used for entrance shuffle
        },
        # The following SM regions are only used when the corresponding StartLocation option is selected (so not with
        # default settings). Also, those don't have any entrances as they serve as starting Region (that's why they
        # have to be excluded for testAllStateCanReachEverything).
        "Super Metroid": {
            "Ceres",
            "Gauntlet Top",
            "Mama Turtle"
        },
        "Manual_PlateUp_Nicopopxd":{
            "Extra 01",
            "Early Extra 01",
            "Middle Extra 01",
            "Late Extra 01",
            "Extra 02",
            "Early Extra 02",
            "Middle Extra 02",
            "Late Extra 02",
            "Extra 03",
            "Early Extra 03",
            "Middle Extra 03",
            "Late Extra 03",
            "Extra 04",
            "Early Extra 04",
            "Middle Extra 04",
            "Late Extra 04",
            "Extra 05",
            "Early Extra 05",
            "Middle Extra 05",
            "Late Extra 05",
            "Extra 06",
            "Early Extra 06",
            "Middle Extra 06",
            "Late Extra 06",
            "Extra 07",
            "Early Extra 07",
            "Middle Extra 07",
            "Late Extra 07",
            "Extra 08",
            "Early Extra 08",
            "Middle Extra 08",
            "Late Extra 08",
            "Extra 09",
            "Early Extra 09",
            "Middle Extra 09",
            "Late Extra 09",
            "Extra 10",
            "Early Extra 10",
            "Middle Extra 10",
            "Late Extra 10"
        }

    }

    def test_default_all_state_can_reach_everything(self):
        """Ensure all state can reach everything and complete the game with the defined options"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            unreachable_regions = self.default_settings_unreachable_regions.get(game_name, set())
            with self.subTest("Game", game=game_name):
                world = setup_solo_multiworld(world_type)
                excluded = world.exclude_locations[1].value
                state = world.get_all_state(False)
                for location in world.get_locations():
                    if location.name not in excluded:
                        with self.subTest("Location should be reached", location=location):
                            self.assertTrue(location.can_reach(state), f"{location.name} unreachable")

                for region in world.get_regions():
                    if region.name in unreachable_regions:
                        with self.subTest("Region should be unreachable", region=region):
                            self.assertFalse(region.can_reach(state))
                    else:
                        with self.subTest("Region should be reached", region=region):
                            self.assertTrue(region.can_reach(state))

                with self.subTest("Completion Condition"):
                    self.assertTrue(world.can_beat_game(state))

    def test_default_empty_state_can_reach_something(self):
        """Ensure empty state can reach at least one location with the defined options"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                world = setup_solo_multiworld(world_type)
                state = CollectionState(world)
                all_locations = world.get_locations()
                if all_locations:
                    locations = set()
                    for location in all_locations:
                        if location.can_reach(state):
                            locations.add(location)
                    self.assertGreater(len(locations), 0,
                                       msg="Need to be able to reach at least one location to get started.")

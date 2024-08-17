from test.general.test_implemented import TestImplemented
from test.general.test_fill import TestFillRestrictive, TestDistributeItemsRestrictive, TestBalanceMultiworldProgression
from test.general.test_locations import TestBase
from test.general.test_reachability import TestBase as TestReach


class WotWTestImpl(TestImplemented):  # TODO fails, use entrances for the region linked to the location/event
    game = "Ori and the Will of the Wisps"


class WotWTestFill(TestFillRestrictive):
    game = "Ori and the Will of the Wisps"


class WotWTestItems(TestDistributeItemsRestrictive):
    game = "Ori and the Will of the Wisps"


class WotWTestBalance(TestBalanceMultiworldProgression):
    game = "Ori and the Will of the Wisps"


class WotWTestLoc(TestBase):
    game = "Ori and the Will of the Wisps"


class WotWTestReach(TestReach):
    game = "Ori and the Will of the Wisps"

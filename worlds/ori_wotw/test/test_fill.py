from test.bases import WorldTestBase
from test.general.test_implemented import TestImplemented
from test.multiworld.test_multiworlds import TestTwoPlayerMulti
from test.options.test_option_classes import TestNumericOptions


class WotWTestBase(WorldTestBase):
    game = "Ori and the Will of the Wisps"


class WotWTestMultiworld(TestTwoPlayerMulti):
    game = "Ori and the Will of the Wisps"


class WotWTestOptions(TestNumericOptions):
    game = "Ori and the Will of the Wisps"

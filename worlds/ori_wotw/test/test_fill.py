from test.bases import WorldTestBase
from test.multiworld.test_multiworlds import TestTwoPlayerMulti


class WotWTestBase(WorldTestBase):
    game = "Ori and the Will of the Wisps"


class WotWTestMultiworld(TestTwoPlayerMulti):
    game = "Ori and the Will of the Wisps"

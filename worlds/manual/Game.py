import json
import os

with open(os.path.join(os.path.dirname(__file__), '_game.json'), 'r') as file:
    game_table = json.loads(file.read())

game_name = "Manual_%s_%s" % (game_table["game"], game_table["player"])
filler_item_name = game_table["filler_item_name"]

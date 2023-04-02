import json
import os

from BaseClasses import Item
from .Game import filler_item_name

######################
# Load item tables from JSON
######################

item_table = {}
with open(os.path.join(os.path.dirname(__file__), '_items.json'), 'r') as file:
    item_table = json.loads(file.read())

progressive_item_table = {}
# with open(os.path.join(os.path.dirname(__file__), '_progressive_items.json'), 'r') as file:
#     if file:        
#         progressive_item_table = json.loads(file.read())

######################
# Generate item lookups
######################

item_id_to_name = {}
item_name_to_item = {}
advancement_item_names = set()
lastItemId = -1

count = 777000

# add the filler item to the list of items for lookup
item_table.append({
    "name": filler_item_name
})

# add sequential generated ids to the lists
for key, val in enumerate(item_table):
    item_table[key]["id"] = count
    item_table[key]["progression"] = val["progression"] if "progression" in val else False
    count += 1

for item in item_table:
    item_name = item["name"]
    item_id_to_name[item["id"]] = item_name
    item_name_to_item[item_name] = item
    if item["progression"]:
        advancement_item_names.add(item_name)
    
    if item["id"] != None:
        lastItemId = max(lastItemId, item["id"])

progressive_item_list = {}

for item in progressive_item_table:
    progressiveName = progressive_item_table[item]
    if progressiveName not in progressive_item_list:
        progressive_item_list[progressiveName] = []
    progressive_item_list[progressiveName].append(item)

for progressiveItemName in progressive_item_list.keys():
    lastItemId += 1
    generatedItem = {}
    generatedItem["id"] = lastItemId
    generatedItem["name"] = progressiveItemName
    generatedItem["progression"] = item_name_to_item[progressive_item_list[progressiveItemName][0]]["progression"]
    item_name_to_item[progressiveItemName] = generatedItem
    item_id_to_name[lastItemId] = progressiveItemName

item_id_to_name[None] = "__Victory__"
item_name_to_id = {name: id for id, name in item_id_to_name.items()}

######################
# Item classes
######################


class ManualItem(Item):
    game = "Manual"

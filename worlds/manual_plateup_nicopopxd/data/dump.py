import json
for file in ["items.json", "locations.json"]:
    with open(file, 'r') as ifile:
        data = json.load(ifile)
    with open("new-"+file, 'w') as ofile:
        json.dump({i['name']: i['name'] for i in data}, ofile)
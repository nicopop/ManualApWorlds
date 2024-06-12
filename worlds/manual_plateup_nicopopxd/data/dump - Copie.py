import json
for file in ["items.json", "locations.json"]:
    with open(file, 'r') as ifile:
        data = json.load(ifile)
    with open(file+"Names", 'w') as ofile:
        json.dump([i['name'] for i in data], ofile)
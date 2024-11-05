import json
import sys

tree = json.load(open(sys.argv[-1], "rb")).get("tree", {})

types = {}
for object in tree:
    types[object["type"]] = types.get(object["type"], 0) + 1

match len(types.keys()):
    case 0:
        print("No tree objects found")
        raise SystemExit(1)
    case 1:
        print(f"Found {types[object["type"]]} objects of type {object["type"]}")
    case _:
        print(f"Found {len(types.keys())} types:")
        for type_name, amount in types.items():
            print(f"  > {amount} {type_name}" + ("s" if amount == 1 else ""))

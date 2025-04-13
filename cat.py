import argparse

parser = argparse.ArgumentParser(description="Random Cat Generator")
parser.add_argument(
    "name", metavar="name", type=str, help="Name for randomly generated cat"
)
args = parser.parse_args()

import random

random.seed(args.name)
output: list[dict[str, str]] = [{"Name": args.name}]

output[0]["Size"] = random.choice(["small", "medium", "small", "medium", "large"])
output[0]["Age"] = random.choice(
    {
        "small": ["kitten", "kitten", "junior", "mature", "senior"],
        "medium": ["junior", "mature", "adult", "senior"],
        "large": ["mature", "adult", "senior"],
    }[output[0]["Size"]]
)

output.append({})
output[1]["Color"] = random.choice(
    ["orange", "black", "white", "gray", "light gray", "brown", "creme", "yellow"]
)
output[1]["Eye Color"] = random.choice(
    ["yellow", "amber", "yellow", "green", "blue", "orange", "copper"]
)
output[1]["Hair Length/Texture"] = random.choice(
    ["short", "long", "curly", "silky", "fluffy"]
)

output.append({})
output[2]["Energy"] = random.choice(["lazy", "playful", "hyperactive"])
output[2]["Social Behavior"] = random.choice(
    ["affectionate", "aloof", "shy", "friendly"]
)
output[2]["Vocalization"] = random.choice(
    {
        "lazy": ["quiet", "chatty"],
        "playful": ["quiet", "chatty", "loud"],
        "hyperactive": ["chatty", "loud"],
    }[output[2]["Energy"]]
)


m = max([max([len(_) for _ in i.keys()]) for i in output])
mv = max([max([len(_) for _ in i.values()]) for i in output])
p = False
f = True
for i in output:
    if not f:
        print(f"\x1b[48;5;{232 + int(p) * 2}m{(m + mv + 2) * " "}\x1b[0m")
        p = not p
    for k, v in i.items():
        print(
            f"\x1b[48;5;{232 + int(p) * 2}m{k}:{(m - len(k)) * " "} {v}{(mv - len(v)) * " "}\x1b[0m"
        )
        p = not p
    f = False

print("\x1b[0m", end="")

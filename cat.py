#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(
    description="Random Cat Generator\n DISCLAIMER: THIS PRIGRAM USES RANDOMLY GENERATED DATA\n IF SOMEONES NAME GENERATES A COMBINATION THEY FIND UNFITTING,\n THEY JUST HAVE TO DEAL WITH IT (looking at you cris)",
    usage="cat.py [-f] name [...]",
)
parser.add_argument(
    "name", metavar="name", type=str, help="Name for randomly generated cat", nargs="+"
)
parser.add_argument(
    "-f", "--force", action="store_true", help="Bypass name validation", dest="force"
)
args = parser.parse_args()

name = " ".join(args.name)

if not args.force:
    import re
    import sys

    if not re.fullmatch(
        r"(?:[a-z]+ ?)*[a-z]+", name, re.IGNORECASE
    ) and name.lower() not in [":(){:|:&};:", "baer1"]:
        print(f"Invalid name: {name}", file=sys.stderr)
        raise SystemExit(1)

import random

random.seed(name)
output: list[dict[str, str]] = [{"Name": name}]

output[0]["Size"] = random.choice(["small", "medium", "small", "medium", "large"])
output[0]["Age"] = random.choice(
    {
        "small": ["kitten", "kitten", "junior", "mature", "senior"],
        "medium": ["junior", "mature", "adult", "senior"],
        "large": ["mature", "adult", "senior"],
    }[output[0]["Size"]]
)

output.append({})
output[1]["Colour"] = random.choice(
    ["orange", "black", "white", "gray", "light gray", "brown", "creme", "yellow"]
)
output[1]["Eye Colour"] = random.choice(
    ["yellow", "amber", "yellow", "green", "blue", "orange", "copper"]
)
output[1]["Hair Length/Texture"] = random.choice(
    ["short", "long", "curly", "silky", "fluffy"]
)

output.append({})
output[2]["Energy"] = random.choice(["lazy", "playful", "hyperactive"])
output[2]["Social Behaviour"] = random.choice(
    ["affectionate", "aloof", "shy", "friendly"]
)
output[2]["Vocalization"] = random.choice(
    {
        "lazy": ["quiet", "chatty"],
        "playful": ["quiet", "chatty", "loud"],
        "hyperactive": ["chatty", "loud"],
    }[output[2]["Energy"]]
)

match name.lower():
    case ":(){:|:&};:":
        output[0]["Size"] = "tiny"
        output[0]["Age"] = "very old"

        output[2]["Energy"] = "unstoppable"
        output[2]["Social Behaviour"] = "silly"
        output[2]["Vocalization"] = "silent"

        output.append({"Preferred food": "RAM", "Note": "will blow up your computer"})

    case "angrybadwolf":
        # :)
        output[0]["Size"] = "small"
        output[0]["Age"] = "kitten"

        output.append({"Note": "small kitten"})

    case "baer1":
        output.append({"Note": "fuck C Programming Language"})

    case "crisdeck":
        random.seed(None)
        output.append(
            {
                "Final words": '> "Can you get MVM tickets?"\n> "No, I\'m too lazy to go to the store"\n> "Fuck you"\n*leaves vc, never seen since*',
                "Note": f"cris please this is randomly generated this was never supposed to represent you\nand yes i know crisdeck is not your real name thats how usernames work\nrandom number (maybe this will help you understand randomness): {random.randint(1, 9)}",
            }
        )


m = max([max([len(_) for _ in i.keys()]) for i in output])
mv = max([max([len(_) for _ in i.values()]) for i in output])
p = False
f = True
for i in output:
    if not f:
        print(f"\x1b[48;5;{232 + int(p) * 2}m\x1b[K\x1b[0m")
        p = not p
    for k, v in i.items():
        print(
            f"\x1b[48;5;{232 + int(p) * 2}m {k}:{(m - len(k)) * " "} {f"\x1b[K\n{m * " "}   ".join(v.splitlines())}\x1b[K\x1b[0m",
        )
        p = not p
    f = False

print("\x1b[0m", end="")

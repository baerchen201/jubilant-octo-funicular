import os
import argparse
import requests
import re
import base64
import json
from datetime import datetime, timedelta


def exit(*args, **kwargs):
    print(*args, **kwargs)
    raise SystemExit(1)


argparser = argparse.ArgumentParser(
    prog="setdiscordstatus.py",
    description="Sets the status of one or more discord accounts",
)
argparser.add_argument("-D", help=argparse.SUPPRESS, action="store_true")  # Debug
storemode = argparser.add_mutually_exclusive_group()
storemode.add_argument(
    "-d",
    help="Display each tokens current status (before change) and save it to a file",
)
storemode.add_argument(
    "-r", help="Restore from a file generated by -d. This is prioritized over -s and -t"
)
argparser.add_argument(
    "-R", help="Removes all files that are used (useful with -r)", action="store_true"
)
argparser.add_argument(
    "-S",
    help="Safe file handling - -d doesn't overwrite existing files - -r doesn't fail when file is missing",
    action="store_true",
)
argparser.add_argument(
    "-s", help="The status to set", choices=("online", "idle", "dnd", "invisible")
)
argparser.add_argument(
    "-t", help="The status text to set (removes custom status if empty)"
)
expire = argparser.add_mutually_exclusive_group()
expire.add_argument(
    "-e", help="The expiration date for the custom status (in ISO format)"
)
expire.add_argument(
    "-E", help="The expiration date for the custom status (in UNIX seconds)"
)
expire.add_argument(
    "-o",
    help="The expiration date for the custom status (offset in seconds from the current time, can't be negative)",
)
argparser.add_argument(
    "-O", help="The emoji to set (not validated, use at your own risk)"
)
argparser.add_argument(
    "-i", help="Includes tokens from local discord installations", action="store_true"
)
argparser.add_argument(
    "tokens",
    help="The tokens to apply the changes to",
    nargs="*",
)
args = argparser.parse_args()

tokens = args.tokens

if args.i:
    _ = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    import discordtoken

    os.chdir(_)

    for token in discordtoken.get_tokens():
        if not token in tokens:
            tokens.append(token)
    if not tokens:
        exit("No discord tokens found")

if not tokens:
    exit("No discord tokens specified")

data = {}
if args.s:
    data["status"] = args.s
if args.t == "":
    data["custom_status"] = None
elif args.t:
    data["custom_status"] = {"text": args.t}

    e = None
    if args.e:
        try:
            e = datetime.fromisoformat(args.e).isoformat()
        except ValueError:
            exit("Malformed ISO timestamp")
    elif args.E:
        try:
            e = datetime.fromtimestamp(int(args.E)).isoformat()
        except ValueError:
            exit("Invalid timestamp")
    elif args.o:
        try:
            e = (
                datetime.now()
                + timedelta(
                    seconds=(
                        int(args.o) if int(args.o) > 0 else exit("Negative time offset")
                    )
                )
            ).isoformat()
        except ValueError:
            exit("Invalid time offset")

    data["custom_status"]["expires_at"] = e

    if args.O:
        data["custom_status"]["emoji_name"] = args.O


if not data and not args.d and not args.r:
    exit("No modifications")

store = {}
if args.r:
    try:
        with open(os.path.expanduser(args.r), "rb") as f:
            store = json.loads(f.read().decode())
    except Exception as e:
        if args.S:
            _ = print
        else:
            _ = exit
        _(
            f"Invalid -r file specified (could not be read): {type(e).__name__}{' - ' + str(e) if str(e).strip() else ''}"
        )

for token in tokens:
    try:
        user = None
        settings = None
        headers = {
            "authorization": token,
            "content-type": "application/json",
            "user-agent": "setdiscordstatus.py (https://github.com/baerchen201/jubilant-octo-funicular/tree/main/linux/setdiscordstatus.py, contact https://baerchen201.github.io) via python-requests module",
        }
        if args.D:
            print(headers)
        userid = base64.b64decode(token.split(".")[0] + "==").decode()

        if args.d:
            user = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            user.raise_for_status()
            user = user.json()
            settings = requests.get(
                "https://discord.com/api/v9/users/@me/settings", headers=headers
            )
            settings.raise_for_status()
            settings = settings.json()
            print(
                f"{user['username']}: {settings['status']}{' ' + str(settings['custom_status']) if settings['custom_status'] else ''}"
            )
            store[userid] = {
                "status": settings["status"],
                "custom_status": settings["custom_status"],
            }

        if data or (args.r and store[userid]):
            response = requests.patch(
                "https://discord.com/api/v9/users/@me/settings",
                json=data | (store.get(userid, {}) if args.r else {}),
                headers=headers,
            )
            response.raise_for_status()
            response = response.json()
            print(
                f"Status {response['status']} {response['custom_status']} for user {user['username'] if user else userid} set successfully"
            )
    except Exception as e:
        if args.D:
            raise e
        en = type(e).__name__
        print(
            f"Unexpected {en} {'' if 'error' in en.lower() or 'exception' in en.lower() else 'exception '}occurred while processing token {token.split('.', 1)[0]}{re.sub(r'[a-zA-Z0-9]', '*', '.' + token.split('.', 1)[1]) if len(token.split('.', 1)) > 1 else ''}: {e}"
        )

if args.d:
    if not (args.S and os.path.isfile(os.path.expanduser(args.d))):
        with open(os.path.expanduser(args.d), "wb") as f:
            f.write(json.dumps(store).encode())
    else:
        print("-d file not written - File exists")

if args.R:
    try:
        os.remove(os.path.expanduser(args.r))
    except Exception as e:
        if args.S:
            _ = print
        else:
            _ = exit
        _(
            f"Invalid -r file specified (could not be deleted): {type(e).__name__}{' - ' + str(e) if str(e).strip() else ''}"
        )

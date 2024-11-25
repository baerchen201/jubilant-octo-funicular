import argparse
import requests
import re  # For error handling
import base64


def exit(*args, **kwargs):
    print(*args, **kwargs)
    raise SystemExit(1)


argparser = argparse.ArgumentParser(
    prog="setdiscordstatus.py",
    description="Sets the status of one or more discord accounts",
)
argparser.add_argument("-D", help=argparse.SUPPRESS, action="store_true")  # Debug
argparser.add_argument(
    "-d", help="Display each tokens current status (before change)", action="store_true"
)
argparser.add_argument(
    "-s", help="The status to set", choices=("online", "idle", "dnd", "invisible")
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
    import discordtoken

    for token in discordtoken.get_tokens():
        if not token in tokens:
            tokens.append(token)
    if not tokens:
        exit("No discord tokens found")

if not tokens:
    exit("No discord tokens specified")

data = {
    "status": args.s,
}
_data = {}
for k, v in data.items():
    if v:
        _data[k] = v
if not _data and not args.d:
    exit("No modifications")

for token in tokens:
    try:
        user = None
        settings = None
        headers = {
            "authorization": token,
            "content-type": "application/json",
            "user-agent": "setdiscordstatus.py (https://github.com/baerchen201/jubilant-octo-funicular/tree/main/linux/setdiscordstatus.py, contact https://baerchen201.github.io) via python-requests module",
        }

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

        if _data:
            response = requests.patch(
                "https://discord.com/api/v9/users/@me/settings",
                json=data,
                headers=headers,
            )
            response.raise_for_status()
            print(
                f"Status {_data['status']} for user {user['username'] if user else base64.b64decode(token.split('.')[0] + '==').decode()} set successfully"
            )  #! Replace _data['status'] later
    except Exception as e:
        if args.D:
            raise e
        en = type(e).__name__
        print(
            f"Unexpected {en} {'' if 'error' in en.lower() or 'exception' in en.lower() else 'exception '}occurred while processing token {token.split('.', 1)[0]}{re.sub(r'[a-zA-Z0-9]', '*', '.' + token.split('.', 1)[1]) if len(token.split('.', 1)) > 1 else ''}: {e}"
        )

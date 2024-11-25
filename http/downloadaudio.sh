#!/bin/bash
yt-dlp -f 'bestaudio' $1 --exec 'python3 convertaudio.py {}'

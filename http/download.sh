#!/bin/bash
yt-dlp -f 'worstvideo+bestaudio' $1 --exec 'python3 convert.py {}'

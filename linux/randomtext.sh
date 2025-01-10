while true; do
  dd if=/dev/random status=progress bs=2000 count=1 | wl-copy -t text/plain
  sleep 0.1
done

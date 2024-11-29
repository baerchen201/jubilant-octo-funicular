echo "Installing dependencies from npm..."
npm i

echo "Installing openssl and python3 from apt..."
sudo apt update
sudo apt install -y openssl python3 python3-requests

echo "Building typescript..."
(
  cd www
  tsc -p "./tsconfig.json"
)

echo "Building scss..."
sass www

echo "Decrypting secret gif..."
openssl enc -aes-256-cbc -d -in "./www/secret.gif.bin" -out "./www/secret.gif" -nosalt -K "$1" -iv "$2"

#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
if ! command -v python >/dev/null 2>&1; then
  echo 'Installing Python in Termux ...'
  pkg update -y && pkg install -y python
fi
if [ ! -s .api_key ]; then
  echo 'Enter your OpenAI API key (input hidden; stored only on this phone):'
  read -r -s KEY
  printf '\n'
  if [ -z "$KEY" ]; then echo 'No key entered. Rerun to configure.'; exit 1; fi
  umask 077
  printf '%s' "$KEY" > .api_key
  unset KEY
fi
python server.py

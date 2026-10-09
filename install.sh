#!/bin/sh
# jev-nano install — fetch the mtlm-router appliance and start the
# Jev-compatible server on http://127.0.0.1:8097
set -e
DIR="${JEVNANO_DIR:-$HOME/jev-nano}"
URL="https://github.com/javimosch/mtlm-router/releases/download/v0.3.0/mtlm-router-v0.3.0-linux-amd64.tar.gz"
mkdir -p "$DIR" && cd "$DIR"
echo "jev-nano: downloading appliance (8MB)…"
curl -fsSL "$URL" -o appliance.tar.gz
tar -xzf appliance.tar.gz
cd mtlm-router-v0.3.0-linux-amd64
echo "jev-nano: starting server on :8097 (Ctrl-C to stop)…"
PORT=8097 exec ./start.sh

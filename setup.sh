#!/bin/bash
# Outline VPN server setup script
# Run on a fresh Ubuntu droplet as root:
#   bash setup.sh

set -e

echo "=== Installing Docker ==="
curl -fsSL https://get.docker.com | sh

echo "=== Installing Outline Server ==="
bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh)"

echo ""
echo "=== Done ==="
echo "Copy the 'apiUrl' and 'certSha256' values above into Outline Manager."

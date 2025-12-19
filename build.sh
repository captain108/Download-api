#!/usr/bin/env bash
set -e

# Install deno
curl -fsSL https://deno.land/install.sh | sh

# Persist deno path
echo 'export DENO_INSTALL="$HOME/.deno"' >> ~/.bashrc
echo 'export PATH="$DENO_INSTALL/bin:$PATH"' >> ~/.bashrc

source ~/.bashrc

pip install -r requirements.txt

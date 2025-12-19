#!/usr/bin/env bash

# Install Deno
curl -fsSL https://deno.land/install.sh | sh

# Add deno to PATH
export DENO_INSTALL="$HOME/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"

# Install Python dependencies
pip install -r requirements.txt

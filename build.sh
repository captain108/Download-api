#!/usr/bin/env bash
set -e

# Install deno (needed by yt-dlp for YouTube)
curl -fsSL https://deno.land/install.sh | sh

# Add deno to PATH
export DENO_INSTALL="$HOME/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"

# Install python deps
pip install -r requirements.txt


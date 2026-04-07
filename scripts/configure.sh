#!/usr/bin/env bash

# This script prepares the development envrionment.
# It installs all relevant plugins, additional packages
# and creates a template .env file.

uv sync --all-extras

uv run pre-commit install

cat > .env <<EOL

EOL

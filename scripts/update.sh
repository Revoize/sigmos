#!/usr/bin/env bash

uv sync --all-extras
uv run pre-commit autoupdate

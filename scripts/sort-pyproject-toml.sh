#!/usr/bin/env bash

set -exu -o pipefail

cd "$(dirname "$0")"

# First use toml sort to sort the pyproject.toml file.
toml-sort \
    --in-place \
    --sort-inline-arrays \
    --sort-inline-tables \
    --sort-table-keys \
    --spaces-indent-inline-array 4 \
    --trailing-comma-inline-array \
    ../pyproject.toml

# Then use taplo to format the pyproject.toml file again which aligns with the vscode extension being used.  This
# results in consistent formatting across the project.
taplo format ../pyproject.toml

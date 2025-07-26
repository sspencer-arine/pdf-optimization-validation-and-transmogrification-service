#!/usr/bin/env bash

set -exu -o pipefail

# Change the current working directory to the directory of the script.
cd "$(dirname "$0")"

# Ensure we are operating in our virtual environment.
source ../.venv/bin/activate

# # Generate stub files because yeh...
# # NOTE(SRS): We can't generate arine_pdfs as a package due to some invalid python code in some of the files.
# stubgen -o ../typings \
#     -p arine_pdfs \
#     -p arine_schemas \
#     -p auto_all \
#     ;

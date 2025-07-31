#!/usr/bin/env bash

set -exu -o pipefail

# Change the current working directory to the directory of the script.
cd "$(dirname "$0")"

# Create a temporary directory for the build and ensure it is cleaned up on exit.
temp_dir=$(mktemp -d)
trap 'rm -rf "${temp_dir}"' EXIT

# Do the build.
docker build \
    --platform=linux/arm64 \
    --progress=plain \
    --file=../layers/python/Dockerfile \
    --output "type=local,dest=${temp_dir}" \
    ..

# Zip the output into ../build/python.zip relative to the temporary directory.
(
    cd "${temp_dir}"
    zip -r python.zip ./python
    du -h -c -s ./python
)

# Ensure the build directory exists.
mkdir -p ../build

# Move the zip file to the build directory.
mv "${temp_dir}/python.zip" ../build/python.zip

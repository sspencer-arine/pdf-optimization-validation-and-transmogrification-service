#!/usr/bin/env bash

set -exu -o pipefail

# Change the current working directory to the directory of the script.
cd "$(dirname "$0")"

# Create a temporary directory for the build and ensure it is cleaned up on exit.
temp_dir=$(mktemp -d)
trap 'rm -rf "${temp_dir}"' EXIT

arine_spack_branch="arine/v1.0"
arine_spack_packages_branch="arine/v2025.07"

arine_spack_commit=$(git ls-remote https://github.com/sspencer-arine/spack ${arine_spack_branch} | cut -f 1)
arine_spack_packages_commit=$(git ls-remote https://github.com/sspencer-arine/spack-packages ${arine_spack_packages_branch} | cut -f 1)

# Do the build.
docker build \
    --platform=linux/arm64 \
    --progress=plain \
    --build-arg ARINE_SPACK_BRANCH="${arine_spack_branch}" \
    --build-arg ARINE_SPACK_COMMIT="${arine_spack_commit}" \
    --build-arg ARINE_SPACK_PACKAGES_BRANCH="${arine_spack_packages_branch}" \
    --build-arg ARINE_SPACK_PACKAGES_COMMIT="${arine_spack_packages_commit}" \
    --file=../layers/programs/Dockerfile \
    --output "type=local,dest=${temp_dir}" \
    ..

# Zip the output into ../build/programs.zip relative to the temporary directory.
(
    cd "${temp_dir}"
    zip -y -r programs.zip ./programs
    du -h -c -s ./programs
)

# Ensure the build directory exists.
mkdir -p ../build

# Move the zip file to the build directory.
mv "${temp_dir}/programs.zip" ../build/programs.zip

# syntax=docker/dockerfile:1.17.1
ARG TARGETARCH

FROM public.ecr.aws/lambda/provided:al2.2025.07.23.13 AS build

RUN <<EOF
    # Install Development Tools, Python, and Git.
    set -e
    yum update -y
    yum group install -y "Development Tools"
    yum install -y python3 git
EOF

# Set up environment variables for Spack.
ENV SPACK_ROOT=/build/spack

# Create directories for Spack and its environment.  The SPACK_ROOT is important since it informs build processes that
# have to deal with Rosetta 2 compatibility what to do as well.
RUN mkdir -p "/build/spack"
RUN mkdir -p "/build/packages"

RUN --mount=type=ssh <<EOF
    # Install Spack.
    set -e

    # Clone the Spack repository and the Spack packages repository.
    git clone --depth=20 --branch=arine/v1.0 https://github.com/sspencer-arine/spack /build/spack
    git clone --depth=20 --branch=arine/v2025.07 https://github.com/sspencer-arine/spack-packages /build/packages

    # Source Spack into the environment.
    . /build/spack/share/spack/setup-env.sh

    # Set the Spack configuration to use the cloned packages repository and bootstrap the environment.
    spack repo set --destination /build/packages builtin
    spack bootstrap now
    spack compiler find
EOF

FROM build AS build-amd64

RUN <<EOF
    # Set up the Spack environment for x86_64 builds.
    set -e
    . /build/spack/share/spack/setup-env.sh
    # Do anything we need to do here that is specific to x86_64 builds.
    spack config add packages:all:target:[x86_64]
EOF

FROM build AS build-arm64

RUN --mount=type=ssh <<EOF
    # Set up the Spack environment for aarch64 builds.
    set -e
    . /build/spack/share/spack/setup-env.sh
    # Do anything we need to do here that is specific to aarch64 builds.
    spack config add packages:all:target:[aarch64]
EOF

ARG TARGETARCH

FROM build-${TARGETARCH} AS build-targetarch

# Set up ccache to speed up builds by caching compiled objects.
ENV CCACHE_DIR=/opt/ccache

RUN mkdir -p "${CCACHE_DIR}"

RUN <<EOF
    # Source the Spack environment and install ccache to speed up subsequent builds.  This has a side effect of
    # installing a bunch of build dependencies as well.
    set -e
    . /build/spack/share/spack/setup-env.sh
    spack install ccache -redis
EOF

RUN mkdir -p "/opt/pdf_optimization_validation_and_transmogrification_service/bin"
RUN mkdir -p "/opt/pdf_optimization_validation_and_transmogrification_service/environment"
RUN mkdir -p "/opt/pdf_optimization_validation_and_transmogrification_service/view"
RUN mkdir -p "/opt/pdf_optimization_validation_and_transmogrification_service/software"

# Create a Spack environment file that defines the packages we want to compartmentalize.
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/coreutils/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/curl/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/findutils/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/ghostscript_fonts/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/ghostscript/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/grep/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/openssh/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/openssl/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/poppler/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/qpdf/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/rsync/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/tar/package.py
#   - https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/zip/package.py
COPY <<EOF /opt/pdf_optimization_validation_and_transmogrification_service/environment/spack.yaml
spack:
  specs:
    # - coreutils@9.5 +gprefix
    # - curl@8.11.1 tls=openssl
    # - findutils@4.10.0
    # - ghostscript-fonts@8.11
    - ghostscript@10.05.0 -gtk -dbus -x11 -krb5
    # - openssh@9.9p1
    # - openssl@3.4.1
    # - poppler@21.09.0 +cms +jpeg +tiff +png
    - qpdf@11.9.1 crypto=openssl
    # - rsync@3.4.1
    # - tar@1.35
    # - zip@3.0
  concretizer:
    unify: true
  config:
    install_tree: /opt/pdf_optimization_validation_and_transmogrification_service/software
    ccache: true
    shared_linking:
        bind: true
  view: /opt/pdf_optimization_validation_and_transmogrification_service/view
EOF

ARG TARGETARCH

RUN --mount=type=cache,target=/opt/ccache,id=ccache-cache-${TARGETARCH},sharing=locked <<EOF
    # Activate the Spack environment and install the packages defined in the spack.yaml file.
    set -e
    . /build/spack/share/spack/setup-env.sh
    spack load ccache
    spack env activate /opt/pdf_optimization_validation_and_transmogrification_service/environment
    spack install --concurrent-packages 1 --fail-fast
EOF

RUN <<EOF
    # Clean up the Spack environment to remove unnecessary files and directories.
    set -e
    . /build/spack/share/spack/setup-env.sh
    spack env activate /opt/pdf_optimization_validation_and_transmogrification_service/environment
    spack gc --yes-to-all
EOF

RUN <<EOF
    # Strip unnecessary symbols from the binaries in the view directory to reduce the size of the final image.
    set -e
    find -L /opt/pdf_optimization_validation_and_transmogrification_service/software -type f -exec readlink -f '{}' \; \
    | xargs file -i \
    | grep 'charset=binary' \
    | grep 'x-executable\|x-archive\|x-sharedlib' \
    | awk -F: '{print $1}' \
    | xargs strip -s
EOF

# Bring over only what we need at this point to create a minimal layer asset.
FROM scratch
COPY --from=build-targetarch /opt/pdf_optimization_validation_and_transmogrification_service /opt/pdf_optimization_validation_and_transmogrification_service

# syntax=docker/dockerfile:1.17.1
ARG TARGETARCH

FROM public.ecr.aws/sam/build-python3.13:latest AS build

RUN <<EOF
    # Install Development Tools, Python, and Git.
    dnf group install -y "Development Tools"
    dnf install -y python3 git
EOF

# Set up environment variables for Spack.
ENV SPACK_ROOT=/build/spack

# Create directories for Spack and its environment.  The SPACK_ROOT is important since it informs build processes that
# have to deal with Rosetta 2 compatibility what to do as well.
RUN mkdir -p "/build/spack"
RUN mkdir -p "/build/packages"

ARG ARINE_SPACK_BRANCH
ARG ARINE_SPACK_COMMIT

ARG ARINE_SPACK_PACKAGES_BRANCH
ARG ARINE_SPACK_PACKAGES_COMMIT

RUN --mount=type=ssh <<EOF
    # Install Spack (spack@${ARINE_SPACK_BRANCH}:${ARINE_SPACK_COMMIT} spack-packages@${ARINE_SPACK_PACKAGES_BRANCH}:${ARINE_SPACK_PACKAGES_COMMIT}).
    set -e

    # Clone the Spack repository and the Spack packages repository.
    git clone --depth=20 --branch=${ARINE_SPACK_BRANCH} https://github.com/sspencer-arine/spack /build/spack
    git clone --depth=20 --branch=${ARINE_SPACK_PACKAGES_BRANCH} https://github.com/sspencer-arine/spack-packages /build/packages

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

RUN mkdir -p "/opt/programs/bin"
RUN mkdir -p "/opt/programs/environment"
RUN mkdir -p "/opt/programs/view"
RUN mkdir -p "/opt/programs/software"

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
COPY <<EOF /opt/programs/environment/spack.yaml
spack:
  specs:
    # - coreutils@9.5 +gprefix
    # - curl@8.11.1 tls=openssl
    # - findutils@4.10.0
    # - font-util@1.4.1 fonts=font-alias
    - ghostscript-fonts@8.11
    - ghostscript@10.05.0 -gtk -dbus -x11 -krb5
    # - openssh@9.9p1 -gssapi
    # - openssl@3.4.1
    # - poppler@21.09.0 +cms +jpeg +tiff +png
    - qpdf@11.9.1 crypto=openssl
    # - rsync@3.4.1
    - tar@1.35
    - zip@3.0
  concretizer:
    unify: true
  config:
    install_tree: /opt/programs/software
    shared_linking:
        bind: true
  view: /opt/programs/view
EOF

ARG TARGETARCH

RUN <<EOF
    # Activate the Spack environment and install the packages defined in the spack.yaml file.
    set -e
    . /build/spack/share/spack/setup-env.sh
    spack env activate /opt/programs/environment
    spack install --concurrent-packages 1 --fail-fast
EOF

RUN <<EOF
    # Clean up the Spack environment to remove unnecessary programs, files and directories.
    set -e
    . /build/spack/share/spack/setup-env.sh
    spack env activate /opt/programs/environment
    spack clean --all
    spack gc --yes-to-all
EOF

RUN <<EOF
    # Clean up the Spack environment to remove unnecessary files and directories.
    set -e
    . /build/spack/share/spack/setup-env.sh
    spack env activate /opt/programs/environment
    spack spec | tee /opt/programs/environment/spack-spec.txt
EOF

RUN <<EOF
    # Remove unnecessary directories from the software directory to reduce the size of the final image.
    set -e

    rm -rf /opt/programs/software/linux-aarch64/*/include
    rm -rf /opt/programs/software/linux-aarch64/*/lib*/*.a
    rm -rf /opt/programs/software/linux-aarch64/*/lib*/cmake
    rm -rf /opt/programs/software/linux-aarch64/*/lib*/pkgconfig
    rm -rf /opt/programs/software/linux-aarch64/*/man
    rm -rf /opt/programs/software/linux-aarch64/*/share/*-completion
    rm -rf /opt/programs/software/linux-aarch64/*/share/aclocal
    rm -rf /opt/programs/software/linux-aarch64/*/share/doc
    rm -rf /opt/programs/software/linux-aarch64/*/share/examples
    rm -rf /opt/programs/software/linux-aarch64/*/share/gtk-doc
    rm -rf /opt/programs/software/linux-aarch64/*/share/i18n
    rm -rf /opt/programs/software/linux-aarch64/*/share/info
    rm -rf /opt/programs/software/linux-aarch64/*/share/locale
    rm -rf /opt/programs/software/linux-aarch64/*/share/man
    rm -rf /opt/programs/software/linux-aarch64/*/share/terminfo
    rm -rf /opt/programs/software/linux-aarch64/*/share/vim
    rm -rf /opt/programs/software/linux-aarch64/*/share/zsh

    # Remove symlinks that point to non-existent files.
    find /opt/programs -xtype l -delete

    # Remove empty directories.
    find /opt/programs -type d -empty -delete
EOF

RUN <<EOF
    # Strip unnecessary symbols from the binaries in the view directory to reduce the size of the final image.
    set -e
    find -L /opt/programs/software -type f -exec readlink -f '{}' \; \
    | xargs file -i \
    | grep 'charset=binary' \
    | grep 'x-executable\|x-archive\|x-sharedlib' \
    | awk -F: '{print $1}' \
    | xargs strip --verbose --strip-debug --strip-unneeded
EOF

# Bring over only what we need at this point to create a minimal layer asset.
FROM scratch AS target

COPY --from=build-targetarch /opt/programs /programs

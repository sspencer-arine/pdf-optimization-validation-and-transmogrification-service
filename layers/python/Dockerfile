# syntax=docker/dockerfile:1.17.1
ARG TARGETARCH

FROM public.ecr.aws/sam/build-python3.13:latest AS build

WORKDIR /build

COPY requirements requirements

RUN python3 -m venv ./ --upgrade-deps

RUN ./bin/python3 -m pip install --compile -r requirements/production.txt
RUN ./bin/python3 -m pip uninstall -y -r requirements/provided.txt
RUN ./bin/python3 -m compileall -o 0 -o 1 -o 2 -f ./lib/python3.13/site-packages/

RUN <<EOF
    # Strip unnecessary symbols from the binaries in the view directory to reduce the size of the final image.
    set -e
    find -L ./lib/python3.13/site-packages/ -type f -exec readlink -f '{}' \; \
    | xargs file -i \
    | grep 'charset=binary' \
    | grep 'x-executable\|x-archive\|x-sharedlib' \
    | awk -F: '{print $1}' \
    | xargs strip --verbose --strip-debug --strip-unneeded
EOF

FROM scratch
COPY --from=build /build/lib/python3.13/site-packages/ /python/

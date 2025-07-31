# syntax=docker/dockerfile:1.17.1
ARG TARGETARCH

FROM public.ecr.aws/sam/build-python3.13:latest AS build

WORKDIR /build

COPY . .

RUN python3 -m venv ./ --upgrade-deps

RUN ./bin/python3 -O -m pip install . --no-deps --no-compile --target ./project/
RUN ./bin/python3 -m compileall -o 0 -o 1 -o 2 -f ./project/

RUN <<EOF
    # Strip unnecessary symbols from the binaries in the view directory to reduce the size of the final image.
    set -e
    find -L ./lib/python3.13/site-packages/ -type f -exec readlink -f '{}' \; \
    | xargs file -i \
    | grep 'charset=binary' \
    | grep 'x-executable\|x-archive\|x-sharedlib' \
    | awk -F: '{print $1}' \
    | echo xargs strip --verbose --strip-debug --strip-unneeded
EOF

FROM scratch
COPY --from=build /build/project/ /project/

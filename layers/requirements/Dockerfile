# syntax=docker/dockerfile:1.17.1
ARG TARGETARCH

FROM public.ecr.aws/sam/build-python3.13:latest AS build

WORKDIR /build

COPY requirements requirements

RUN python3 -m venv ./ --upgrade-deps

RUN ./bin/python3 -m pip install --compile -r requirements/production.txt
RUN ./bin/python3 -m pip uninstall -y -r requirements/provided.txt

RUN find ./lib/python3.13/site-packages/ -name "*.so" -exec strip --verbose --strip-debug --strip-unneeded {} \;

FROM scratch
COPY --from=build /build/lib/python3.13/site-packages/ /python/

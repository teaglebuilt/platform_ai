FROM python:3.12-slim-bookworm as base

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

FROM base as metrics

COPY metrics /opt/platform/metrics

WORKDIR /opt/platform/metrics

RUN uv pip install "git+https://github.com/teaglebuilt/platform_ai.git"

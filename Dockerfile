FROM python:3.12-slim-bookworm as base

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates git

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

FROM base as api

COPY api /opt/platform/api

WORKDIR /opt/platform/api

RUN pip install prometheus_client
RUN pip install "git+https://github.com/teaglebuilt/platform_ai.git"

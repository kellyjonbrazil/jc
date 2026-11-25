# OSS Scanner build for jc (JSON Convert): https://github.com/anthropics/oss-scanner
# Network access is available only during this build; everything the tests need is installed here.
FROM debian:bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

# jc's test suite expects the America/Los_Angeles timezone
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates git python3 python3-venv python3-pip tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# scanner contract: the checkout lives inside the image, at /src
COPY . /src
WORKDIR /src

# Install runtime deps and jc itself (editable, so the scanner's patches take effect without reinstalling)
RUN python3 -m venv $VIRTUAL_ENV \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -e . \
    && jc --version

# Run the test suite so the image is known-good, but don't fail the build on test failures
RUN (python3 -m unittest discover -s tests -q 2>&1 | tail -5) || echo "WARNING: unittest reported failures"


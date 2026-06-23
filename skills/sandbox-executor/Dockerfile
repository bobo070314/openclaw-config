FROM python:3.12-slim

LABEL maintainer="OpenClaw Sandbox Executor"
LABEL description="Isolated execution environment for AI-generated code"

WORKDIR /skill

# Install only sanctioned dependencies
RUN pip install --no-cache-dir requests pyyaml

# Create non-root user for defense-in-depth
RUN useradd --create-home --shell /bin/bash sandbox && \
    chown -R sandbox:sandbox /skill

USER sandbox

# Default entrypoint: execute the mounted skill's run.py
ENTRYPOINT ["python", "/skill/run.py"]

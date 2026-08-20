FROM python:3.13-slim

ENV VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=0 \
    MPLBACKEND=Agg

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        ca-certificates curl git gettext-base \
    && rm -rf /var/lib/apt/lists/*

COPY --from=node:22-slim /usr/local /usr/local

RUN python -m venv $VIRTUAL_ENV \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        "numpy==2.3.2" \
        "matplotlib==3.10.5" \
        "pytest==8.3.4" \
        "sphinx>=7.2,<9" \
        "myst-parser>=2.0,<5" \
        "sphinx-rtd-theme>=3.0" \
        "sphinxcontrib-mermaid>=0.9"

RUN npm install -g @anthropic-ai/claude-code

CMD ["/bin/bash"]
# buzzle/Dockerfile
# Multi-stage build: Go CLI + Python API in one image

# ── Stage 1: Build Go CLI ─────────────────────────────────────────────────────
FROM golang:1.22-alpine AS go-builder

WORKDIR /build
COPY cli/go.mod ./
COPY cli/main.go ./
RUN go build -ldflags="-s -w" -o buzzle-cli .


# ── Stage 2: Python API ───────────────────────────────────────────────────────
FROM python:3.11-slim

LABEL maintainer="hevkyr <github.com/hevkyr>"
LABEL description="buzzle — motivational nonsense as a service"
LABEL version="1.0.0"

# Copy Go binary
COPY --from=go-builder /build/buzzle-cli /usr/local/bin/buzzle

# API
WORKDIR /app
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

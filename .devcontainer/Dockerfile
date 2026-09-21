# Imagen base ligera (Debian 13 "trixie"). Python NO viene de la imagen:
# uv instala la versión exacta de .python-version (la misma build que en local).
FROM mcr.microsoft.com/devcontainers/base:2.2-trixie

# Misma versión de uv que se usa localmente para generar uv.lock
COPY --from=ghcr.io/astral-sh/uv:0.12.17 /uv /uvx /usr/local/bin/

#!/usr/bin/env bash
# Verifica que el entorno de Codespaces (devcontainer) sea idéntico al .venv local.
#
#   bash .claude/skills/auditar-curso/scripts/env_parity.sh <ruta_repo> <carpeta_temporal> [--run-notebooks]
#
# 1. Copia sólo los archivos versionados (+ cambios sin commit) a una carpeta limpia: simula un clon fresco,
#    que es lo que ve Codespaces (los archivos sin versionar NO existen allí).
# 2. Construye y levanta el devcontainer con el CLI oficial (@devcontainers/cli vía npx).
# 3. Compara `python -VV` y `uv pip freeze` del contenedor contra el .venv local.
# 4. Opcional: ejecuta todos los notebooks dentro del contenedor.
# 5. Elimina el contenedor.
#
# Requiere Docker Desktop corriendo. Las descargas de imágenes pueden colgarse dentro del sandbox:
# ejecuta este script con el sandbox deshabilitado.
set -euo pipefail

if ! docker info > /dev/null 2>&1; then
    echo "Docker no está corriendo. Inícialo con: open -a Docker (y espera ~30 s)" >&2
    exit 1
fi

REPO="$(cd "$1" && pwd)"
WORK="$2"
RUN_NB="${3:-}"
NAME="$(basename "$REPO" | tr ' ' '_' | tr -cd '[:alnum:]_-')"
CLONE="$WORK/parity-$NAME"
SCRIPTS="$(cd "$(dirname "$0")/../../crear-laboratorio/scripts" && pwd)"

rm -rf "$CLONE" && mkdir -p "$CLONE"
(cd "$REPO" && git ls-files -z --cached --modified | sort -zu | while IFS= read -r -d '' f; do
    [ -e "$f" ] && mkdir -p "$CLONE/$(dirname "$f")" && cp "$f" "$CLONE/$f"
done)
echo "Copia limpia en $CLONE ($(cd "$CLONE" && find . -type f | wc -l | tr -d ' ') archivos)"

npx -y @devcontainers/cli@latest up --workspace-folder "$CLONE" --remove-existing-container 2>&1 | tail -1
CID="$(docker ps -q --filter "label=devcontainer.local_folder=$CLONE")"
WS="/workspaces/$(basename "$CLONE")"

(cd "$REPO" && .venv/bin/python -VV && uv pip freeze --python .venv/bin/python) > "$WORK/$NAME-local.txt"
docker exec -u vscode -w "$WS" "$CID" bash -lc '.venv/bin/python -VV; uv pip freeze --python .venv/bin/python' > "$WORK/$NAME-container.txt"

echo "--- Diferencias local vs contenedor (esperado: sólo la fecha de compilación de Python y paquetes exclusivos de macOS como appnope)"
diff "$WORK/$NAME-local.txt" "$WORK/$NAME-container.txt" || true
echo "--- Paquetes: local $(($(wc -l < "$WORK/$NAME-local.txt") - 1)) | contenedor $(($(wc -l < "$WORK/$NAME-container.txt") - 1))"

if [ "$RUN_NB" = "--run-notebooks" ]; then
    cp "$SCRIPTS/run_notebooks.py" "$CLONE/"
    docker exec -u vscode -w "$WS" "$CID" bash -lc 'uv run --with nbclient python run_notebooks.py . 2>&1 | grep -v IPKernelApp' || true
    rm "$CLONE/run_notebooks.py"
fi

docker rm -f "$CID" > /dev/null && echo "Contenedor eliminado"

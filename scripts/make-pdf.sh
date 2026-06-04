#!/usr/bin/env bash
#
# Generate public/pqc-field-guide.pdf from the current content by rendering the
# /book-print route with headless Chrome. Run after `npm run convert` so the PDF
# always reflects the latest manuscript.
#
# Usage: npm run pdf   (or: bash scripts/make-pdf.sh)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PORT="${PDF_PORT:-4399}"
OUT="public/pqc-field-guide.pdf"
TMP_PDF="$(mktemp -t pqc-pdf).pdf"

CHROME="${CHROME_BIN:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
if [ ! -e "${CHROME}" ]; then
  echo "Chrome not found at: ${CHROME}" >&2
  echo "Set CHROME_BIN to a Chrome/Chromium binary and retry." >&2
  exit 1
fi

echo "[pdf] building site..."
npm run build >/dev/null

echo "[pdf] starting preview server on port ${PORT}..."
node_modules/.bin/astro preview --port "${PORT}" >/tmp/pqc-pdf-preview.log 2>&1 &
PREVIEW_PID=$!
trap 'kill "${PREVIEW_PID}" 2>/dev/null || true' EXIT

URL="http://localhost:${PORT}/book-print/"
for _ in $(seq 1 40); do
  if curl -fsS -o /dev/null "${URL}"; then break; fi
  sleep 0.3
done

echo "[pdf] rendering with headless Chrome..."
"${CHROME}" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="${TMP_PDF}" "${URL}" >/dev/null 2>&1 || true

if [ ! -s "${TMP_PDF}" ]; then
  echo "[pdf] ERROR: Chrome produced no output" >&2
  exit 1
fi

mv "${TMP_PDF}" "${OUT}"
echo "[pdf] wrote ${OUT} ($(wc -c < "${OUT}") bytes)"
echo "[pdf] run 'npm run build' to copy it into dist/"

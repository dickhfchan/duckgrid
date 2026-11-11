#!/usr/bin/env bash
# Builds dist/ for DuckGrid:
#   dist/duckgrid.html               the page (DuckDB client bundle inlined; D3 loads from cdnjs)
#   dist/duckdb-eh.gz.wasm           the DuckDB engine, gzipped (~7 MB; the page unzips it in the browser)
#   dist/duckdb-browser-eh.worker.js the DuckDB worker
#   dist/index.html + dist/d3.min.js a full-document wrapper with a local D3, for local testing
#
# Publish to a claude.ai artifact: duckgrid.html as the page, the .gz.wasm and worker.js as supporting
# files (the .gz.wasm name matters: artifacts only serve known extensions and cap files at 15 MB).
set -euo pipefail
cd "$(dirname "$0")"
npm install --no-audit --no-fund
mkdir -p dist
npx esbuild src/entry.js --bundle --minify --format=iife --platform=browser --legal-comments=none --outfile=dist/duckdb.bundle.js
gzip -9 -c node_modules/@duckdb/duckdb-wasm/dist/duckdb-eh.wasm > dist/duckdb-eh.gz.wasm
cp node_modules/@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js dist/
cp node_modules/d3/dist/d3.min.js dist/
python3 - <<'EOF'
src = open('src/duckgrid.template.html').read()
bundle = open('dist/duckdb.bundle.js').read()
page = src.replace('__DUCKDB_BUNDLE__', bundle)
open('dist/duckgrid.html', 'w').write(page)
local = page.replace('https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js', 'd3.min.js')
open('dist/index.html', 'w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>[hidden]{display:none!important}</style></head><body>' + local + '</body></html>')
EOF
rm dist/duckdb.bundle.js
ls -la dist

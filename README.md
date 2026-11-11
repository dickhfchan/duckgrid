# DuckGrid

A single-page data explorer: DuckDB-WASM + canvas grid + pivot + auto-insights + a D3 chart gallery, in one HTML page.

```bash
bash build.sh                       # npm install, bundle the DuckDB client, gzip the engine → dist/
cd dist && python3 -m http.server 8765
# open http://localhost:8765/index.html
```

- **Source:** `src/duckgrid.template.html` is the whole app (HTML, CSS and JS). The build replaces the `__DUCKDB_BUNDLE__` placeholder with the bundled DuckDB client.
- **Publishing as a claude.ai artifact:** publish `dist/duckgrid.html` as the page, with `duckdb-eh.gz.wasm` and `duckdb-browser-eh.worker.js` as supporting files.
- **Views:**
  - **Insights:** KPI tiles, a monthly trend with the anomaly marked, "What changed" sentences, a ranked breakdown and a heatmap.
  - **Charts:** a gallery of 11 D3 samples; picking one rebuilds it from your data.
  - **Table:** the canvas grid, with sorting, filtering and 256-row windowed fetches.
  - **Side panel:** the pivot and the SQL log.
- **Script and agent API:** `window.duckgrid.sql()`, `filter()`, `sort()`, `pivot()`, `insights()`, `chartTypes()`, `chart(type, fields)`, `state()`.
- **Sample data:** 10M generated sales rows with built-in patterns. **Load CSV** replaces them with your own file.
- **Tests:** `test/*.py` use Playwright with the system Chrome against `http://localhost:8765/index.html`:
  - `test_insights.py [light|dark]` checks the KPIs and insights and takes screenshots;
  - `test_charts.py [light|dark]` renders every chart type;
  - `test_crossfilter.py` covers click-to-filter, switching views and phone width.

  They write screenshots to the parent directory.

## Licences

DuckDB and DuckDB-WASM are MIT, D3 is ISC, and Apache Arrow is Apache-2.0.

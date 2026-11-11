import asyncio, time, json, sys
from playwright.async_api import async_playwright
scheme = sys.argv[1] if len(sys.argv)>1 else 'light'
async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = await b.new_page(viewport={'width':1440,'height':900}, color_scheme=scheme)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type in ('error','warning') and 'ERR_TUNNEL' not in m.text and '404' not in m.text else None)
    await pg.goto('http://localhost:8765/index.html')
    for i in range(120):
      await asyncio.sleep(1)
      if 'Pivot ready' in await pg.evaluate("document.querySelector('#stOpText').textContent"): break
    await pg.click('.seg button[data-view=charts]'); await asyncio.sleep(1.5)
    await pg.screenshot(path=f'../gal_{scheme}.png')
    for t in ['scatter','stacked','donut']:
      r = await pg.evaluate(f"window.duckgrid.chart('{t}').then(r=>JSON.stringify({{spec:r.spec, n:r.rows.length}}))")
      await asyncio.sleep(0.6)
      await pg.screenshot(path=f'../ch_{t}_{scheme}.png')
      print(t, r[:160], await pg.evaluate("document.querySelector('#stOpText').textContent"))
    print(errs[:10]); await b.close()
asyncio.run(main())

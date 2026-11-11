import asyncio, time, sys, json
from playwright.async_api import async_playwright
scheme = sys.argv[1] if len(sys.argv)>1 else 'light'
async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = await b.new_page(viewport={'width':1440,'height':900}, color_scheme=scheme)
    errs=[]
    pg.on('pageerror', lambda e: errs.append('PAGEERR '+str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' and 'ERR_TUNNEL' not in m.text and '404' not in m.text else None)
    await pg.goto('http://localhost:8765/index.html')
    t=time.time()
    for i in range(120):
      await asyncio.sleep(1)
      st = await pg.evaluate("document.querySelector('#stOpText').textContent")
      if ('Pivot ready' in st) or 'failed' in st.lower(): break
    print('boot', round(time.time()-t,1), st)
    r = await pg.evaluate("window.duckgrid.insights().then(r=>JSON.stringify(r))")
    d=json.loads(r); print(json.dumps(d['kpis'])); [print('-',x['kind'],':',x['text']) for x in d['insights']]
    await pg.screenshot(path=f'../ins_{scheme}.png', full_page=False)
    await pg.evaluate("document.querySelector('#insights').scrollTop=1400"); await asyncio.sleep(0.3)
    await pg.screenshot(path=f'../ins_{scheme}_2.png')
    print(errs)
    await b.close()
asyncio.run(main())

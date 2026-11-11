import asyncio, time, json
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = await b.new_page(viewport={'width':1440,'height':900})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto('http://localhost:8765/index.html')
    for i in range(120):
      await asyncio.sleep(1)
      if 'Pivot ready' in await pg.evaluate("document.querySelector('#stOpText').textContent"): break
    await pg.click('#bars .bar-row >> nth=0')
    for i in range(60):
      await asyncio.sleep(0.5)
      st=await pg.evaluate("document.querySelector('#stOpText').textContent")
      if 'Insights ready' in st or 'Pivot ready' in st: 
        if i>2: break
    await asyncio.sleep(2)
    print('where:', await pg.evaluate("document.querySelector('#whereInput').value"), '|', await pg.evaluate("document.querySelector('#insPeriod').textContent"))
    print([x['text'][:90] for x in json.loads(await pg.evaluate("window.duckgrid.insights().then(r=>JSON.stringify(r))"))['insights']])
    await pg.click('.seg button[data-view=table]'); await asyncio.sleep(1)
    await pg.screenshot(path='../tbl.png')
    await pg.evaluate("document.querySelector('#insights').scrollTop=1400")
    await pg.click('.seg button[data-view=insights]'); await asyncio.sleep(1)
    await pg.evaluate("document.querySelector('#insights').scrollTop=1400"); await asyncio.sleep(0.3)
    await pg.screenshot(path='../heat_light.png')
    await pg.set_viewport_size({'width':400,'height':860}); await asyncio.sleep(1)
    print('scrollW', await pg.evaluate("document.documentElement.scrollWidth"))
    await pg.evaluate("document.querySelector('#insights').scrollTop=0"); await asyncio.sleep(0.5)
    await pg.screenshot(path='../ins_mobile.png')
    print(errs); await b.close()
asyncio.run(main())

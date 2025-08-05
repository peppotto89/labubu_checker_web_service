from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pyppeteer import launch

app = FastAPI()

@app.get("/checkpp")
async def checkpypeter():
    browser = await launch(
        headless=True,
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--single-process',
            '--no-zygote',
            '--disable-software-rasterizer',
        ],
    )
    page = await browser.newPage()

    # Stealth manuale semplice
    await page.evaluateOnNewDocument('''() => {
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    }''')

    await page.goto('https://www.popmart.com/it/products/5610', {'waitUntil': 'networkidle2'})

    # Aspetta un po' per caricamento JS dinamico
    await asyncio.sleep(5)

    # Cerca i bottoni per testo
    buy_now = await page.querySelectorEval('div', '''(els) => {
        return Array.from(document.querySelectorAll('div')).some(el => el.innerText.toLowerCase().includes('buy now'));
    }''')

    add_to_cart = await page.querySelectorEval('div', '''(els) => {
        return Array.from(document.querySelectorAll('div')).some(el => el.innerText.toLowerCase().includes('add to cart'));
    }''')

    print(f"Buy Now found: {buy_now}")
    print(f"Add To Cart found: {add_to_cart}")

    await browser.close()
    return JSONResponse(content={
                "buynow": f"{buy_now}",
                "addcart": f"{add_to_cart}"
            })

@app.get("/checkk")
async def check_buttons():
    return JSONResponse(content={
            "status": "ohohohohoo33333",
            "prova": "prova"
        }, status_code=500)

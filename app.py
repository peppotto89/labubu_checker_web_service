from fastapi import FastAPI
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import traceback
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
            "status": "ohohohohoo22222",
            "prova": "prova"
        }, status_code=500)
        
@app.get("/check")
async def check_buttons():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) return 'Intel Inc.';
                    if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                    return getParameter(parameter);
                };
                Object.defineProperty(window, 'RTCPeerConnection', {value: undefined});
            """)

            await page.goto("https://www.popmart.com/it/products/5610", timeout=30000)
            await page.wait_for_timeout(15000)  # aspetta caricamento
            
            # Cerca bottone BUY NOW per testo (case insensitive)
            #buy_now_count = await page.locator("text=/BUY NOW/i").count()
            # Cerca bottone ADD TO CART per testo (case insensitive)
            #add_to_cart_count = await page.locator("text=/ADD TO CART/i").count()
            found = await page.locator("text=/your connection before proceeding/i").count()

            await browser.close()

            return JSONResponse(content={
                "security": found > 0,
                "status": "success"
            })

    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }, status_code=500)

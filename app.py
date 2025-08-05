from fastapi import FastAPI
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import traceback

app = FastAPI()

@app.get("/checkk")
async def check_buttons():
    return JSONResponse(content={
            "status": "ohohohohoo99999",
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
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
                );
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

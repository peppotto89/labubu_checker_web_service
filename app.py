from fastapi import FastAPI
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/checkk")
async def check_buttons():
    return JSONResponse(content={
            "status": "ohohohohooh",
            "error": "error erroe"
        }, status_code=500)
        
@app.get("/check")
async def check_buttons():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto("https://www.popmart.com/it/products/5610", timeout=30000)
            await page.wait_for_timeout(5000)  # aspetta caricamento

            buy_now_button = await page.query_selector("text=/buy now/i")
            add_to_cart_button = await page.query_selector("text=/add to cart/i")

            await browser.close()

            return JSONResponse(content={
                "buy_now_found": bool(buy_now_button),
                "add_to_cart_found": bool(add_to_cart_button),
                "status": "success"
            })

    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "error": str(e)
        }, status_code=500)

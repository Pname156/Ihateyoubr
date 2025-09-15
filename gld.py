import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

def get_prices():
    try:
        url = "https://www.tgju.org/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        dollar_price = soup.find("span", {"data-col": "info.last_trade"}).text.strip()
        gold_price = soup.find("span", {"data-col": "info.last_trade", "data-market": "coin"}).text.strip()
        return {
            "dollar": dollar_price,
            "gold": gold_price
        }
    except Exception as e:
        return {"error": str(e)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات قیمت دلار و طلا هستم.\n"
        "از دستور /price برای دریافت قیمت‌ها استفاده کنید."
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = get_prices()
    if "error" in prices:
        await update.message.reply_text(f"خطا در دریافت قیمت‌ها: {prices['error']}")
    else:
        response = (
            f"💵 قیمت دلار: {prices['dollar']} تومان\n"
            f"🪙 قیمت سکه امامی: {prices['gold']} تومان"
        )
        await update.message.reply_text(response)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
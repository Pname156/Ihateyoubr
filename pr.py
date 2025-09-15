from telegram.ext import Application, CommandHandler
import requests
from bs4 import BeautifulSoup

TOKEN = "8212226011:AAGtELxlNeS-o5uNlh0Z4Wu21QP-XCXPC8k"

async def get_dollar_price():
    try:
        url = "https://www.tgju.org/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find('span', class_='price').text
        return f"قیمت دلار: {price} تومان"
    except:
        return "خطا در دریافت قیمت دلار. بعداً امتحان کنید."

async def get_gold_price():
    try:
        url = "https://www.tgju.org/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find('span', class_='gold-price').text
        return f"قیمت طلا: {price} تومان"
    except:
        return "خطا در دریافت قیمت طلا. بعداً امتحان کنید."

async def start(update, context):
    await update.message.reply_text("به ربات قیمت خوش آمدید! از دستورات زیر استفاده کنید:\n/dollar - قیمت دلار\n/gold - قیمت طلا")

async def dollar(update, context):
    price = await get_dollar_price()
    await update.message.reply_text(price)

async def gold(update, context):
    price = await get_gold_price()
    await update.message.reply_text(price)

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dollar", dollar))
    app.add_handler(CommandHandler("gold", gold))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
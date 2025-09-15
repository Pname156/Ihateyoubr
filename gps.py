import requests
from telegram.ext import Application, CommandHandler
import asyncio
import nest_asyncio

TOKEN = "8212226011:AAGtELxlNeS-o5uNlh0Z4Wu21QP-XCXPC8k"

async def get_dollar_price():
    try:
        response = requests.get("https://api.tgju.org/v1/market/indicator")
        data = response.json()
        dollar_price = data["data"]["usd"]["p"]
        return f"قیمت دلار: {dollar_price} تومان"
    except:
        return "خطا در دریافت قیمت دلار"

async def get_gold_price():
    try:
        response = requests.get("https://api.tgju.org/v1/market/indicator")
        data = response.json()
        gold_price = data["data"]["gold_18"]["p"]
        return f"قیمت طلا (18 عیار): {gold_price} تومان"
    except:
        return "خطا در دریافت قیمت طلا"

async def dollar(update, context):
    await update.message.reply_text(await get_dollar_price())

async def gold(update, context):
    await update.message.reply_text(await get_gold_price())

async def main():
    application = Application.builder().token(TOKEN).job_queue(None).build()
    application.add_handler(CommandHandler("dollar", dollar))
    application.add_handler(CommandHandler("gold", gold))
    await application.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
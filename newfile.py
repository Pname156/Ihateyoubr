import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = '8212226011:AAGtELxlNeS-o5uNlh0Z4Wu21QP-XCXPC8k'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def download_video(url, update, context):
    download_path = '/sdcard/Download/'
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    ydl_opts = {
        'outtmpl': f'{download_path}%(title)s.%(ext)s',
        'format': 'best[height<=720]',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            with open(filename, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=video_file,
                    caption=f"دانلود شد: {info.get('title', 'Unknown')}"
                )
            
            os.remove(filename)
            
    except Exception as e:
        await update.message.reply_text(f"خطا در دانلود: {str(e)}\nلینک رو چک کن یا مطمئن شو عمومی باشه.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لینک پورن‌هاب بفرست تا دانلود کنم.\n"
        "مثال: https://www.pornhub.com/view_video.php?viewkey=...\n"
        "توجه: فقط ویدیوهای عمومی و کوچک (کمتر از ۵۰ مگ)."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if 'pornhub.com' in url:
        await update.message.reply_text("در حال دانلود... صبر کن.")
        await download_video(url, update, context)
    else:
        await update.message.reply
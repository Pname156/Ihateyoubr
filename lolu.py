import telebot
import instaloader
import os
import tempfile
from urllib.parse import urlparse

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CUSTOM_MESSAGE = "دانلود شده توسط ربات ما! برای حمایت، به کانال ما بپیوندید: @YourChannel"
bot = telebot.TeleBot(BOT_TOKEN)
L = instaloader.Instaloader(download_video_thumbnails=False, download_geotags=False, download_comments=False, save_metadata=False, compress_json=False, post_metadata_txt_pattern='')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "سلام! لینک اینستاگرام (پست عمومی) بفرست تا دانلود کنم. فقط پست‌های عمومی کار می‌کنه.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if 'instagram.com' not in url:
        bot.reply_to(message, "لطفاً یک لینک معتبر اینستاگرام بفرست!")
        return
    try:
        bot.reply_to(message, "در حال دانلود... صبر کن (ممکنه چند ثانیه طول بکشه).")
        parsed_url = urlparse(url)
        path = parsed_url.path
        if '/p/' in path:
            shortcode = path.split('/p/')[1].split('/')[0]
        elif '/reel/' in path:
            shortcode = path.split('/reel/')[1].split('/')[0]
        else:
            bot.reply_to(message, "لینک پست یا ریلز معتبر نیست!")
            return
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        with tempfile.TemporaryDirectory() as temp_dir:
            L.dirname_pattern = temp_dir
            L.download_post(post, target=message.from_user.username)
            files = os.listdir(temp_dir)
            if not files:
                bot.reply_to(message, "خطا در دانلود! پست خصوصی یا نامعتبره.")
                return
            media_files = [f for f in files if f.endswith(('.mp4', '.jpg', '.jpeg'))]
            if not media_files:
                bot.reply_to(message, "هیچ رسانه‌ای پیدا نشد!")
                return
            latest_file = max(media_files, key=lambda f: os.path.getctime(os.path.join(temp_dir, f)))
            file_path = os.path.join(temp_dir, latest_file)
            caption = f"{post.caption or ''}\n\n{CUSTOM_MESSAGE}"
            if latest_file.endswith('.mp4'):
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption=caption)
            else:
                with open(file_path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=caption)
        bot.reply_to(message, "دانلود و ارسال موفق!")
    except Exception as e:
        bot.reply_to(message, f"خطا: {str(e)}. مطمئن شو پست عمومی باشه و لینک درست باشه.")

if __name__ == '__main
import logging
import openai
import os
from dotenv import load_dotenv
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

# Load environment variables from .env file
load_dotenv()

# Set up logging
log_file = "dreadgpt.log"
logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load your password for encrypting the log file from the .env file
password = os.getenv("LOG_FILE_PASSWORD").encode()

def encrypt_log_file():
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    fernet = Fernet(key)

    with open(log_file, "rb") as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    with open(log_file, "wb") as f:
        f.write(salt + encrypted_data)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hey, I'm Pixel - An AI Chatbot! Ask me anything. If you want to create an AI image, please type '/image' followed by your prompt.")

def handle_message(update: Update, context: CallbackContext):
    try:
        input_text = update.message.text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text},
            ],
        )
        answer = response.choices[0].message['content'].strip()
        update.message.reply_text(answer, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error("An error occurred while handling the message: %s", e)
        update.message.reply_text("Oops! An error occurred. Please try again later.")

def generate_image(update: Update, context: CallbackContext):
    try:
        prompt = ' '.join(context.args)
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        update.message.reply_photo(photo=image_url)
    except Exception as e:
        logger.error("An error occurred while generating the image: %s", e)
        update.message.reply_text("Oops! An error occurred. Please try again later.")

def error_handler(update: Update, context: CallbackContext):
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main():
    # Set up the Telegram bot token
    updater = Updater(os.getenv("TELEGRAM_API_TOKEN"))

    # Add handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("image", generate_image))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("An unhandled exception occurred: %s", e)
    finally:
        encrypt_log_file()

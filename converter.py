import os.path
import telebot
from gtts import gTTS
import pdfplumber
from pathlib import Path
from telebot import TeleBot

bot = telebot.TeleBot('5522367235:AAFddRA5aZ1q80sOmi-WJflM4m62Zmhjrb0')


def pdf_to_audio(file_path: str, language: str):
    if Path(file_path).is_file() and Path(file_path).suffix == ".pdf":

        with pdfplumber.PDF(open(file=file_path, mode="rb")) as pdf:
            pages = [page.extract_text() for page in pdf.pages]

        text = ''.join(pages)
        text = text.replace('\n', '')

        my_audio = gTTS(text=text, lang=language, slow=False)
        file_name = Path(file_path).stem
        my_audio.save(f'converted_audio_files/{file_name}.mp3')

        return f'{file_name}.mp3 saved successfully!'
    else:
        return 'File not found. Check file path'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Hello do you want convert file?\n Enter 'yes' or 'no'")


@bot.message_handler()
def main_function(message):
    if message.text in ("yes", "YES", "Yes"):
        bot.send_message(message.chat.id, "Please send file which you want convert")
    if message.text in ("no", "NO", "No"):
        bot.send_message(message.chat.id, "I didn't know do other operation")


@bot.message_handler(func=lambda message: message.document,
                     content_types=['document',])
def manage_files(message):
    raw = message.document.file_id
    path = f"pdf_files/{raw}.pdf"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)

    convert = pdf_to_audio(path, "en")
    if convert:
        doc = open(f'converted_audio_files/{raw}.mp3', 'rb')
        bot.send_document(message.chat.id, doc)




bot.polling(none_stop=True)

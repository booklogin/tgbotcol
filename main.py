import os
import time
import requests
import fitz  # PyMuPDF
from telegram import Bot
from datetime import datetime, timedelta

# Токен вашего бота
TOKEN = '6345371895:AAGtHaYeYDPfcuCpa21Agm7GEyGYPzInbno'
CHAT_ID = '-1002224342955'
bot = Bot(token=TOKEN)

def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    return False

def extract_page_as_png(pdf_path, page_number, output_png):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)
    pix = page.get_pixmap()
    pix.save(output_png)

def check_and_send_file():
    today = datetime.now()
    check_date = today + timedelta(days=1)
    check_day = check_date.strftime('%d')

    url = f'https://ркэ.рф/assets/rasp/{check_day}0920241.pdf'
    pdf_filename = f'rasp_{check_day}.pdf'
    png_filename = 'page7.png'

    if download_pdf(url, pdf_filename):
        extract_page_as_png(pdf_filename, 6, png_filename)  # Page 7 = index 6
        bot.send_photo(chat_id=CHAT_ID, photo=open(png_filename, 'rb'))
        os.remove(pdf_filename)
        os.remove(png_filename)
        return True
    return False

def main():
    while True:
        if check_and_send_file():
            time.sleep(86400)  # Ожидание следующего дня
        else:
            time.sleep(10)  # Повторная проверка через 10 секунд

if __name__ == '__main__':
    main()

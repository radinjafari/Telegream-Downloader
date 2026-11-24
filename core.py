import logging
import requests
import re
import os

from pathlib import Path
from urllib.parse import urlsplit, unquote

from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


class Downloader:

    def __init__(self, bot: TeleBot):

        self.bot = bot
        self.logger = logging.getLogger(__name__)

        self.download_dir = Path("./downloads")
        self.download_dir.mkdir(exist_ok=True)

        self.max_file_size = 45 * 1024 * 1024  # 45 MB

        self.user_formats = {}

        self.backend()

    # ==========================================
    # DOWNLOAD FILE
    # ==========================================

    def download_file(self, url: str):

        filename = Path(unquote(urlsplit(url).path)).name or "download.bin" 
        # unquote --> filtering the path; urlsplit(url) --> splits the url in some parts; .path.name --> returns the name in the path
        filename = re.sub(r'[^\w.-]', '_', filename)

        file_path = self.download_dir / filename

        downloaded_size = 0

        with requests.get(url, stream=True, timeout=(10, 30)) as response:

            response.raise_for_status()

            if int(response.headers.get("Content-Length", 0)) > self.max_file_size:
                raise ValueError("File is too large!")

            with open(file_path, "wb") as file:

                for chunk in response.iter_content(chunk_size=8192):

                    if chunk:

                        downloaded_size += len(chunk)

                        if downloaded_size > self.max_file_size:
                            raise ValueError("File is too large!")

                        file.write(chunk)

        return file_path

    # ==========================================
    # SEND FILE
    # ==========================================

    def send_file(self, chat_id, file_path, file_type):

        with open(file_path, "rb") as file:

            if file_type == "photo":

                self.bot.send_photo(chat_id, file)

            elif file_type == "video":

                self.bot.send_video(chat_id, file)

            elif file_type == "audio":

                self.bot.send_audio(chat_id, file)

            elif file_type == "voice":

                self.bot.send_voice(chat_id, file)

            elif file_type == "animation":

                self.bot.send_animation(chat_id, file)

            else:

                self.bot.send_document(chat_id, file)

    # ==========================================
    # BACKEND
    # ==========================================

    def backend(self):

        # START COMMAND

        @self.bot.message_handler(commands=['start', 'شروع'])
        def start(message: Message):

            keyboard = InlineKeyboardMarkup()

            keyboard.row(
                InlineKeyboardButton(
                    "Document",
                    callback_data="document"
                ),
                InlineKeyboardButton(
                    "Photo",
                    callback_data="photo"
                )
            )

            keyboard.row(
                InlineKeyboardButton(
                    "Video",
                    callback_data="video"
                ),
                InlineKeyboardButton(
                    "Audio",
                    callback_data="audio"
                )
            )

            keyboard.row(
                InlineKeyboardButton(
                    "Voice",
                    callback_data="voice"
                ),
                InlineKeyboardButton(
                    "Animation",
                    callback_data="animation"
                )
            )

            self.bot.send_message(
                message.chat.id,
                "Welcome to File Downloader!\n\n"
                "Choose your preferred download format:",
                reply_markup=keyboard
            )

        # FORMAT SELECTION

        @self.bot.callback_query_handler(
            func=lambda call: call.data in [
                "document",
                "photo",
                "video",
                "audio",
                "voice",
                "animation"
            ]
        )
        def choose_callback(call):

            self.user_formats[call.message.chat.id] = call.data # E.G. {123456... : Video}

            self.bot.answer_callback_query(call.id)

            self.bot.send_message(
                call.message.chat.id,
                f"Selected format: {call.data}\n\n"
                "Now send your download link."
            )

        # DOWNLOAD LINK

        @self.bot.message_handler(regexp=r'https?://\S+')
        def send_link(message: Message):

            self.logger.info(f"Received link: {message.text}")

            chat_id = message.chat.id

            file_type = self.user_formats.get(chat_id)

            if not file_type:

                self.bot.send_message(
                    chat_id,
                    "Please select a format first using /start."
                )

                return

            file_path = None

            try:

                self.bot.send_message(
                    chat_id,
                    "Downloading file..."
                )

                url = message.text.strip()

                file_path = self.download_file(url)

                self.bot.send_message(
                    chat_id,
                    "Download completed! Sending file..."
                )

                self.send_file(
                    chat_id,
                    file_path,
                    file_type
                )

                self.bot.send_message(
                    chat_id,
                    "File sent successfully!"
                )

            except Exception as e:

                self.logger.exception(
                    f"Error downloading file: {e}" # Recording Program's ""Log""
                )

                self.bot.send_message(
                    chat_id,
                    f"Error: {e}"
                )


    # ==========================================
    # RUN BOT
    # ==========================================

    def run_bot(self):

        self.bot.infinity_polling()

# 📥 Telegram Downloader

A Python-powered Telegram bot that downloads files from URLs and sends them directly to Telegram users.

Users can choose their preferred file format through an inline keyboard before sending a download link.

## ✨ Features

- 📁 Document delivery
- 🖼 Photo delivery
- 🎬 Video delivery
- 🎵 Audio delivery
- 🎤 Voice delivery
- 🎞 Animation delivery
- 🔘 Inline keyboard format selection
- 📥 Automatic file downloading
- 📏 File size limitation
- 🧹 Automatic cleanup of downloaded files
- 📝 Logging for download activity and errors

## 🛠️ Technologies

- Python
- pyTelegramBotAPI
- Requests
- python-dotenv

## 📂 Project Structure

```text
Telegram-Downloader/
│
├── main.py
├── core.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
└── downloads/
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/radinjafari/Telegram-Downloader.git
```

### 2. Enter the project directory

```bash
cd Telegram-Downloader
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
```

### 4. Activate the virtual environment

**Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Configuration

Create a `.env` file in the project directory:

```env
TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual Telegram bot token.

**Important:** Never share your bot token or upload your `.env` file to GitHub.

## ▶️ Usage

Run the bot:

```bash
python main.py
```

Then:

1. Open your Telegram bot.
2. Send `/start`.
3. Choose your preferred file format.
4. Send a download URL.
5. The bot downloads the file and sends it to you.

## 📏 File Size Limit

The current maximum download size is **45 MB**.

## 👨‍💻 Developer

**Radin Jafari**

---

*Built with Python and pyTelegramBotAPI.*

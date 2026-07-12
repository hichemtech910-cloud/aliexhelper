# DZ Express Bot

Telegram bot that adds AliExpress products to the DZ Express website.

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python bot.py`

## Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `ALIEXPRESS_API_PUBLIC` - AliExpress API public key
- `ALIEXPRESS_API_SECRET` - AliExpress API secret key
- `WEBSITE_URL` - Website URL (default: http://localhost:10000)
- `API_SECRET` - Website API secret key

## Deploy to Render

1. Create a new Worker service
2. Connect your GitHub repo
3. Set build command: `pip install -r bot/requirements.txt`
4. Set start command: `python bot/bot.py`
5. Add environment variables

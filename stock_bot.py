from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Replace with your Bot Token from BotFather
BOT_TOKEN = '8116406715:AAHHCmvrj0eCqXtQXuqqlogTNzoPpIr_UKY'

# Replace with your Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY = 'ONXHZ78UTFIYA8IM'
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Send me a stock symbol (e.g., AAPL), and I'll fetch the latest price for you!"
    )

# Fetch Stock Price
async def get_stock_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stock_symbol = update.message.text.strip().upper()

    try:
        # Fetch data from Alpha Vantage API
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params={
            'function': 'GLOBAL_QUOTE',
            'symbol': stock_symbol,
            'apikey': ALPHA_VANTAGE_API_KEY
        })
        data = response.json()

        # Extract stock price
        if "Global Quote" in data and data["Global Quote"]:
            global_quote = data["Global Quote"]
            price = global_quote["05. price"]
            open_price = global_quote["02. open"]
            high_price = global_quote["03. high"]
            low_price = global_quote["04. low"]

            await update.message.reply_text(
                f"**Stock: {stock_symbol}**\n"
                f"Current Price: ${price}\n"
                f"Open Price: ${open_price}\n"
                f"High Price: ${high_price}\n"
                f"Low Price: ${low_price}"
            )
        else:
            await update.message.reply_text(
                f"❌ Sorry, I couldn't find any data for the symbol: {stock_symbol}. Please check the symbol and try again."
            )
    except Exception as e:
        await update.message.reply_text(
            "⚠️ An error occurred while fetching the stock price. Please try again later."
        )
        print(f"Error: {e}")

# Main Function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_stock_price))

    # Start the Bot
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

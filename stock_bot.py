from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import requests

# Thay thế bằng Bot Token của bạn từ BotFather
BOT_TOKEN = '8116406715:AAHHCmvrj0eCqXtQXuqqlogTNzoPpIr_UKY'

# Thay thế bằng API Key của bạn từ Alpha Vantage
ALPHA_VANTAGE_API_KEY = 'ONXHZ78UTFIYA8IM'
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    instructions = (
        "Chào bạn! Đây là bot tra cứu giá cổ phiếu. Dưới đây là các lệnh bạn có thể sử dụng:\n\n"
        "/start - Bắt đầu sử dụng bot và hiển thị hướng dẫn\n"
        "/about - Giới thiệu về bot\n"
        "/help - Hiển thị danh sách các lệnh\n"
        "/contact - Thông tin liên hệ\n"
        "/<mã cổ phiếu> - Lấy giá cổ phiếu (ví dụ: /AAPL)\n\n"
        "Ví dụ: Gửi lệnh như '/AAPL' để nhận thông tin giá cổ phiếu hiện tại."
    )
    await update.message.reply_text(instructions)

# Lệnh /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot này được phát triển để giúp bạn tra cứu giá cổ phiếu nhanh chóng và dễ dàng."
    )

# Lệnh /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = (
        "/start - Bắt đầu sử dụng bot\n"
        "/about - Giới thiệu về bot\n"
        "/help - Hiển thị danh sách các lệnh\n"
        "/contact - Thông tin liên hệ\n"
        "/<mã cổ phiếu> - Lấy giá cổ phiếu (ví dụ: /AAPL)"
    )
    await update.message.reply_text("Danh sách các lệnh:\n" + commands)

# Lệnh /contact
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Nếu bạn cần hỗ trợ, vui lòng liên hệ qua email: support@example.com."
    )

# Lấy giá cổ phiếu
async def get_stock_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kiểm tra nếu tin nhắn bắt đầu bằng '/'
    if update.message.text.startswith('/'):
        stock_symbol = update.message.text.strip()[1:].upper()  # Loại bỏ ký tự '/' và chuyển thành chữ in hoa

        try:
            # Lấy dữ liệu từ Alpha Vantage API
            response = requests.get(ALPHA_VANTAGE_BASE_URL, params={
                'function': 'GLOBAL_QUOTE',
                'symbol': stock_symbol,
                'apikey': ALPHA_VANTAGE_API_KEY
            })
            data = response.json()

            # Trích xuất giá cổ phiếu
            if "Global Quote" in data and data["Global Quote"]:
                global_quote = data["Global Quote"]
                price = global_quote.get("05. price", "N/A")
                open_price = global_quote.get("02. open", "N/A")
                high_price = global_quote.get("03. high", "N/A")
                low_price = global_quote.get("04. low", "N/A")

                await update.message.reply_text(
                    f"**Mã cổ phiếu: {stock_symbol}**\n"
                    f"Giá hiện tại: ${price}\n"
                    f"Giá mở cửa: ${open_price}\n"
                    f"Giá cao nhất: ${high_price}\n"
                    f"Giá thấp nhất: ${low_price}"
                )
            else:
                await update.message.reply_text(
                    f"❌ Xin lỗi, tôi không tìm thấy dữ liệu cho mã cổ phiếu: {stock_symbol}. Vui lòng kiểm tra lại mã và thử lại."
                )
        except Exception as e:
            await update.message.reply_text(
                "⚠️ Đã xảy ra lỗi khi lấy giá cổ phiếu. Vui lòng thử lại sau."
            )
            print(f"Lỗi: {e}")

# Hàm chính
def main():
    # Tạo ứng dụng
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Thêm các trình xử lý
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, get_stock_price))

    # Khởi động bot
    print("Bot đang chạy...")
    app.run_polling()

if __name__ == '__main__':
    main()

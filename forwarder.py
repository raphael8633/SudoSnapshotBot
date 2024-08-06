import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 替換成你的 bot 的 token
TOKEN = '7255790924:AAHAm-MsGLGmzOCjNjQPpzAvgwssdm2it_Q'
CHAT_ID = '@SudoSnapshot'
#CHAT_ID = '5503887671'
ver = "202408060900"

#raph_debug
DEBUG_ID = '5503887671'

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "/help - Show this help message\n"
        "/echo <message> - Echo the message back to you\n"
        "/chatid - Get the current chat ID"
    )
    await update.message.reply_text(help_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 回應收到的訊息
    if context.args:
        message_to_echo = ' '.join(context.args)
        await update.message.reply_text(f'Echo: {message_to_echo}')
    else:
        await update.message.reply_text('Usage: /echo <message>')

async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 回覆當前群組或聊天的 ID
    chat_id = update.message.chat_id
    await update.message.reply_text(f'The current chat ID is: {chat_id}')

async def echo_version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f'current ver: {ver}')

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 回覆當前群組或聊天的 ID
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text='/強行羞辱')

async def snapshot_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if msg.text and '#snapshot' in msg.text:
        # snapshot reply msg
        if msg.reply_to_message:
            reply_msg = msg.reply_to_message
            await context.bot.forward_message(chat_id=CHAT_ID, from_chat_id=reply_msg.chat_id, message_id=reply_msg.message_id)
            debug_message = f"Forwarded reply message with #snapshot from {reply_msg.chat_id} to {CHAT_ID}"
        # direct snapshot
        else:
            await context.bot.forward_message(chat_id=CHAT_ID, from_chat_id=msg.chat_id, message_id=msg.message_id)
            debug_message = f"Forwarded message with #snapshot from {msg.chat_id} to {CHAT_ID}"
        # Send debug information to your account
        await context.bot.send_message(chat_id=DEBUG_ID, text=debug_message)

async def snapshot_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    # 圖片檔的文字 -> msg.caption
    if msg.caption and '#snapshot' in msg.caption:
        # Forward the message to the target channel
        await context.bot.forward_message(chat_id=CHAT_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        # Send debug information to your account
        debug_message = f"Forwarded image with #snapshot from {msg.chat_id} to {CHAT_ID}"
        await context.bot.send_message(chat_id=DEBUG_ID, text=debug_message)

#debug
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await context.bot.send_message(chat_id=DEBUG_ID, text=now)

def main():
    application = Application.builder().token(TOKEN).build()

    # 在 bot 開始時使用 /start 指令
    application.add_handler(CommandHandler("start", start))

    # 添加指令處理器
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("chatid", chat_id))
    application.add_handler(CommandHandler("v", echo_version))
    application.add_handler(CommandHandler("daily", daily))

    # 回應所有文本訊息
    application.add_handler(MessageHandler(filters.TEXT, snapshot_text))
    # 確保處理包含圖片的訊息
    application.add_handler(MessageHandler(filters.PHOTO, snapshot_image))

    # 啟動 bot
    application.run_polling()

if __name__ == '__main__':
    main()


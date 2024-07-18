import pygsheets
import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 替換成你的 bot 的 token
TOKEN = '7255790924:AAFkzH9hVRKNsl1Isu6wGuEFZ1Cb6lSmgJc'
CHAT_ID = '@SudoSnapshot'
#raph_debug
DEBUG_ID = '5503887671'

def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/help - Show this help message\n"
        "/echo <message> - Echo the message back to you\n"
        "/chatid - Get the current chat ID"
    )
    update.message.reply_text(help_text)

def echo(update: Update, context: CallbackContext) -> None:
    # 回應收到的訊息
    if context.args:
        message_to_echo = ' '.join(context.args)
        update.message.reply_text(f'Echo: {message_to_echo}')
    else:
        update.message.reply_text('Usage: /echo <message>')

def chat_id(update: Update, context: CallbackContext) -> None:
    # 回覆當前群組或聊天的 ID
    chat_id = update.message.chat_id
    update.message.reply_text(f'The current chat ID is: {chat_id}')

def snapshot_text(update: Update, context: CallbackContext) -> None:
    msg = update.message
    if '#snapshot' in msg.text:
        # Forward the message to the target channel
        context.bot.forward_message(chat_id=CHAT_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        # Send debug information to your account
        debug_message = f"Forwarded message with #snapshot from {msg.chat_id} to {CHAT_ID}"
        context.bot.send_message(chat_id=DEBUG_ID, text=debug_message)
        
def snapshot_image(update: Update, context: CallbackContext) -> None:
    msg = update.message
    #print(msg.caption)
    # 圖片檔的文字 -> msg.caption  
    if '#snapshot' in msg.caption:
        # Forward the message to the target channel
        context.bot.forward_message(chat_id=CHAT_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        # Send debug information to your account
        debug_message = f"Forwarded image with #snapshot from {msg.chat_id} to {CHAT_ID}"
        context.bot.send_message(chat_id=DEBUG_ID, text=debug_message)

#debug
def start(update: Update, context: CallbackContext) -> None:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.bot.send_message(chat_id=DEBUG_ID,text=now)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # 在 bot 開始時使用 /start 指令
    dispatcher.add_handler(CommandHandler("start", start))

    # 添加指令處理器
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("echo", echo))
    dispatcher.add_handler(CommandHandler("chatid", chat_id))
    # 回應所有文本訊息
    dispatcher.add_handler(MessageHandler(Filters.text, snapshot_text))
    # 確保處理包含圖片的訊息
    dispatcher.add_handler(MessageHandler(Filters.photo, snapshot_image))
    
    # 啟動 bot
    updater.start_polling()

    # 使 bot 保持運行直到你停止它
    updater.idle()

if __name__ == '__main__':
    main()

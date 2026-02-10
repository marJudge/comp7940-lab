'''
Lab3: 集成 ChatGPT 的 Telegram 聊天机器人。
依赖: python-telegram-bot==22.5, urllib3, requests
'''
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from ChatGPT_HKBU import ChatGPT
import configparser
import logging

gpt = None


def main():
    global gpt
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logging.info('INIT: Loading configuration...')
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['TELEGRAM']['ACCESS_TOKEN'].strip()
    if not token or token == '<your_token>':
        logging.error('请在 config.ini 中填入从 @BotFather 获取的 ACCESS_TOKEN 后再运行')
        return
    api_key = config['CHATGPT']['API_KEY'].strip()
    if not api_key or api_key == '<your_api_key>':
        logging.error('请在 config.ini 的 [CHATGPT] 中填入 HKBU GenAI 的 API_KEY 后再运行')
        return

    # 创建 ChatGPT 客户端对象（配置加载之后）
    gpt = ChatGPT(config)

    logging.info('INIT: Connecting the Telegram bot...')
    app = ApplicationBuilder().token(token).build()

    logging.info('INIT: Registering the message handler...')
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback))

    logging.info('INIT: Initialization done!')
    app.run_polling()


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("UPDATE: " + str(update))
    loading_message = await update.message.reply_text('Thinking...')

    # 将用户消息发送到 ChatGPT 客户端
    response = gpt.submit(update.message.text)

    # 将响应发回 Telegram 机器人客户端
    await loading_message.edit_text(response)


if __name__ == '__main__':
    main()

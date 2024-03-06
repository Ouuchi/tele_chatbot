from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,CallbackContext)
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_CHATGPT
global redis1


def equiped_chatgpt(update,context):
    global chatgpt
    reply_message=chatgpt.submit(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id,text=reply_message)



def main():
# Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    redis1=redis.Redis(host=(config['REDIS']['HOST']),
                      password=(config['REDIS']['PASSWORD']),
                       port=(config['REDIS']['REDISPORT']),
                      )
    # You can set this logging module, so you will know when and why things do not work a
#     logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', le)
    # register a dispatcher to handle message: here we register an echo dispatcher
#     echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
#     dispatcher.add_handler(echo_handler)
    
    
    global chatgpt
    chatgpt=HKBU_CHATGPT()
    chatgpt_handler=MessageHandler(Filters.text&(~Filters.command),equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)
    
    
    dispatcher.add_handler(CommandHandler('add',add))
    dispatcher.add_handler(CommandHandler('help',help_command))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()
                        
def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
    
    
def add(update,context):
    try:
        global redis1
        msg=context.args[0]
        redis1.incr(msg)
        
        update.message.reply_text('You have said '+msg+' for '+redis1.get(msg).decode('UTF-8')+' times.')

    except(IndexError,ValueError):
        update.message.reply_text('Usage:/add <keyword>')

def help_command(update,context):
    update.message.reply_text('Helping you helping you.')
    

if __name__ == '__main__':
    main()


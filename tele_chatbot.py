from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,CallbackContext)
import configparser
import logging

from ChatGPT_HKBU import HKBU_CHATGPT
from azure.storage.blob import BlobServiceClient
import io
import uuid
import random
global container_client
user_video_data = {}
def equiped_chatgpt(update,context):
    global chatgpt

    reply_message,flag=chatgpt.submit(update.message.text)

    if flag=='yes':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait a moment! It is generating the answer")
        reply_message2=chatgpt.submit2(reply_message)
        context.bot.send_message(chat_id=update.effective_chat.id,text=reply_message2)



        t_list=[]
        fileExit=False
        for blob in container_client.list_blobs():
            # 检查 Blob 名称是否匹配
            # print(blob.name,reply_message)
            if blob.name.startswith(reply_message):
                v_name=blob.name
                t_list.append(v_name)
                fileExit=True


        if len(t_list):
            v_name=random.choice(t_list)
        if fileExit==True:
            blob_client = container_client.get_blob_client(v_name)
            video_stream = blob_client.download_blob().readall()

            video_io = io.BytesIO(video_stream)
            video_io.name = v_name
            context.bot.send_video(update.effective_chat.id, video_io)
        else:
            temp_text="you can use '/add_video <dishname>' command to add a video"
            context.bot.send_message(chat_id=update.effective_chat.id, text=temp_text)


    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)





def main():
# Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)



    blob_service_client = BlobServiceClient.from_connection_string(config['VIDEODB']['ACCESS_STRING'])
    container_name = "videoblob"
    global container_client
    container_client = blob_service_client.get_container_client(container_name)



    dispatcher = updater.dispatcher


    
    
    global chatgpt

    chatgpt=HKBU_CHATGPT()
    chatgpt_handler=MessageHandler(Filters.text&(~Filters.command),equiped_chatgpt)

    dispatcher.add_handler(chatgpt_handler)


    
    # dispatcher.add_handler(CommandHandler('add',add))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help',help_command))
    dispatcher.add_handler(CommandHandler('add_video',add_video))
    dispatcher.add_handler(MessageHandler(Filters.video, upload_video))



    
    # To start the bot:
    updater.start_polling()
    updater.idle()



def start(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='I am a professional chef, what do you want to ear or learn? I can teach you.')
def add_video(update,context):

    # print(update.message.text)
    command_parts = update.message.text.split(' ')
    # print(command_parts)
    if len(command_parts) >= 2:
        # video_name = command_parts[1:]
        video_name = ' '.join(command_parts[1:])
        video_name = convert_to_lowercase(video_name)
        unique_id = str(uuid.uuid4())
        # 将唯一标识符与视频名字结合作为 Blob 名称
        video_name = f"{video_name}_{unique_id}"
        # print(video_name)
        # video_name=video_name.split('.')[0]
        user_video_data[update.effective_chat.id] = {"video_name": video_name, "video_file_id": None}

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"The video will be saved as '{video_name}'，please upload the video。")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="please input the correct format，like：/add_video <dishname>")

    # user_video_data[update.effective_chat.id] = {"video_name": update.message.text, "video_file_id": None}

def convert_to_lowercase(name):
    if name.isascii():
        return name.lower()
    else:
        return name



# 处理用户上传的视频
def upload_video(update, context):
    # 获取用户上传的视频文件
    file_id = update.message.video.file_id


    # 检查用户是否之前发送了 "/add_video" 命令，并保存了菜名
    if update.message.chat_id in user_video_data:
        video_name = user_video_data[update.message.chat_id]["video_name"]
        video_name =convert_to_lowercase(video_name)
        # print('video_name:',video_name)

        # 更新用户上传的视频文件信息
        user_video_data[update.message.chat_id]["video_file_id"] = file_id

        # 如果菜名和视频文件都已经准备好，就可以上传视频到 Azure Blob 存储中
        if user_video_data[update.message.chat_id]["video_file_id"]:
            # 下载视频文件到内存中的 BytesIO 对象
            video_file = context.bot.get_file(file_id)
            video_stream = io.BytesIO(video_file.download_as_bytearray())

            # 上传视频文件到 Azure Blob 存储，并使用菜名作为 Blob 名称
            # container_name = "your_container_name"
            blob_name = f"{video_name}.mp4"
            blob_client = container_client.get_blob_client(blob=blob_name)
            blob_client.upload_blob(video_stream)

            # 回复用户上传成功的消息
            context.bot.send_message(update.message.chat_id, f"The video has been uploaded to Azure Blob storage，Blob name is：{blob_name}")

            # 上传完成后清除用户数据，以便下次上传新的视频
            del user_video_data[update.message.chat_id]
    else:
        context.bot.send_message(update.message.chat_id, "please use '/add_video <dishname>' first")





def help_command(update,context):
    update.message.reply_text("use '/add_video <dishname>' then to upload a video")





if __name__ == '__main__':
    main()


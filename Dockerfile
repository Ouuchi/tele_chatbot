FROM python
WORKDIR  /app
COPY . /app
RUN pip install update
RUN pip install -r requirements.txt

ENV TLG_ACCESS_TOKEN=6830559685:AAHmyWbtz7Lf5kmDxOZ2xUp-0LQm2w2Ptl0
ENV BASICURL=https://chatgpt.hkbu.edu.hk/general/rest
ENV MODELNAME=gpt-4-turbo
ENV APIVERSION=2023-08-01-preview
ENV GPT_ACCESS_TOKEN =e9a50fff-5db9-4ffa-ba78-f44fc680d86c
ENV ACCESS_STRING=DefaultEndpointsProtocol=https;AccountName=cloudvideoblob;AccountKey=4N9n1DItu3Jw7kqbKOHXTxm2dVmvQSlVBz5ST6DaSjnO22sPo0ZtmznkllLwLSNMj4QwqUzjyFT4+AStB8UlTQ==;EndpointSuffix=core.windows.net

CMD python tele_chatbot.py


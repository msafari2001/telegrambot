import requests
from flask import Flask
from flask import request
from flask import Response
import wikipedia
import wikipediaapi
import random
import warnings
import os
warnings.filterwarnings("ignore")
token = '1635550428:AAH_Fk4jBN8wpi1qVcHWsLSSlPcvPdKmORM'
url = "https://api.telegram.org/bot1635550428:AAH_Fk4jBN8wpi1qVcHWsLSSlPcvPdKmORM/"
app=Flask(__name__)
def get_all_updates():
    response = requests.get(url+'getUpdates')
    return response.json()
def get_last_update(allUpdates):
    return allUpdates['result'][-1]
def get_chat_id(update):
    return update['message']['chat']['id']
def get_text(update):
    return update['message']['text'] 
def sendMessage(chat_id, text):
    sendData = {
    'chat_id': chat_id,
    'text': text,}
    response = requests.post(url + 'sendMessage', sendData)
    return response

@app.route('/',methods=['POST','GET']) 
def index():
    if request.method== 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        text = msg['message'].get('text', '')
        name = msg['message']['from']['first_name']
        if text=='/start':
            sendMessage(chat_id,f'salam {name}\nلطفا به فرمت زیر وارد کنید\nwiki +(fa,en)+topik')
            return Response('ok', status=200)
        elif 'wiki fa' in text:
            m=text.split(maxsplit=2)[2]
            wiki_wiki = wikipediaapi.Wikipedia('fa')
            page_py = wiki_wiki.page(m)
            if page_py.exists()==True:
                wikipedia.set_lang("fa")
                try:
                    c=wikipedia.search(m,3)
                    x=wikipedia.summary(c[0],sentences=5)
                    y=page_py.fullurl
                except wikipedia.exceptions.DisambiguationError as e:
                    s=random.choice(e.options)
                    x=wikipedia.summary(s,sentences=5)
                    y=page_py.fullurl
                sendMessage(chat_id,f'{x}\n{y}')
                return Response('ok', status=200)
            elif page_py.exists()==False:
                sendMessage(chat_id,'This topic was not found')
                return Response('ok', status=200)
        elif 'wiki en' in text:
            m=text.split(maxsplit=2)[2]
            wiki_wiki = wikipediaapi.Wikipedia('en')
            page_py = wiki_wiki.page(m)
            if page_py.exists()==True:
                wikipedia.set_lang("en")
                try:
                    c=wikipedia.search(m,3)
                    x=wikipedia.summary(c[0],sentences=5)
                    y=page_py.fullurl
                except wikipedia.exceptions.DisambiguationError as e:
                    s=random.choice(e.options)
                    x=wikipedia.summary(s,sentences=5)
                    y=page_py.fullurl
                sendMessage(chat_id,f'{x}\n{y}')
                return Response('ok', status=200)
            elif page_py.exists()==False:
                sendMessage(chat_id,'This topic was not found')
                return Response('ok', status=200)    
        else:
            sendMessage(chat_id,f'ببخشید!!\nلطفا به صورت زیر وارد کنید\nwiki +(fa,en)+topic\nبرای مثال: wiki en iran')
            return Response('ok', status=200)
    else:
        return "<h1>salam</h1>"              
app.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))
    

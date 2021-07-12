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
            sendMessage(chat_id,f'salam {name}\nخوش آمدید\nدر این بات می تونید موضوع مورد نظر خود را وارد کنید \nومطالبی در مورد موضوع دریافت کنید و برای مطالعه بیشتر یک لینک می توانید دریافت کنید ')
            return Response('ok', status=200)
            sendMessage(chat_id,f'ابتدا زبان مدنظر را وارد کنید\nبرای فارسیfa\nبرای انگلیسیen\nبا یک فاصله موضوع مدنظر را وارد کنید\nبرای مثال:\nen iran, fa تهران')
            return Response('ok', status=200)
        elif 'fa' in text:
            m=text.split(maxsplit=1)[1]
            wiki_wiki = wikipediaapi.Wikipedia('fa')
            page_py = wiki_wiki.page(m)
            if page_py.exists()==True:
                wikipedia.set_lang("fa")
                try:
                    c=wikipedia.search(m,3)
                    x=wikipedia.summary(c[0],sentences=6)
                    y=page_py.fullurl
                except wikipedia.exceptions.DisambiguationError as e:
                    s=random.choice(e.options)
                    x=wikipedia.summary(s,sentences=6)
                    y=page_py.fullurl
                sendMessage(chat_id,f'{x}\n{y}')
                return Response('ok', status=200)
            elif page_py.exists()==False:
                sendMessage(chat_id,'This topic was not found')
                return Response('ok', status=200)
        elif 'en' in text:
            m=text.split(maxsplit=1)[1]
            wiki_wiki = wikipediaapi.Wikipedia('en')
            page_py = wiki_wiki.page(m)
            if page_py.exists()==True:
                wikipedia.set_lang("en")
                try:
                    c=wikipedia.search(m,3)
                    x=wikipedia.summary(c[0],sentences=6)
                    y=page_py.fullurl
                except wikipedia.exceptions.DisambiguationError as e:
                    s=random.choice(e.options)
                    x=wikipedia.summary(s,sentences=6)
                    y=page_py.fullurl
                sendMessage(chat_id,f'{x}\n{y}')
                return Response('ok', status=200)
            elif page_py.exists()==False:
                sendMessage(chat_id,'This topic was not found')
                return Response('ok', status=200)    
        else:
            sendMessage(chat_id,f'ببخشید!!\nلطفا به صورت زیر وارد کنید\\nبرای مثال: en iran')
            return Response('ok', status=200)
    else:
        return "<h1>salam</h1>"              
app.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))
    

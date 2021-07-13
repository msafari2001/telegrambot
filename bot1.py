import requests
from flask import Flask
from flask import request
from flask import Response
import wikipedia
import wikipediaapi
import random
import warnings
import os
import json
warnings.filterwarnings("ignore")
token = '1715220962:AAFVS0XKf68UOh57hnL_IZiQyDYtg-LE2aM'
url = "https://api.telegram.org/bot1715220962:AAFVS0XKf68UOh57hnL_IZiQyDYtg-LE2aM/"
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
            sendMessage(chat_id,f'salam {name}\nخوش آمدید\nدر این بات می تونید موضوع مورد نظر خود را وارد کنید \nومطالبی در مورد موضوع دریافت کنید و برای مطالعه بیشتر یک لینک می توانید دریافت کنید \nابتدا زبان مدنظر را وارد کنید\nبرای فارسیfa\nبرای انگلیسیen\nبا یک فاصله موضوع مدنظر را وارد کنید\nبرای مثال:\nen iran, fa تهران\nو با وارد کردن کلمهlinksتمام لینک هارا دریافت کنید')
        elif 'fa' in text:
            m=text.split(maxsplit=1)[1]
            wiki_wiki = wikipediaapi.Wikipedia('fa')
            page_py = wiki_wiki.page(m)
            if page_py.exists()==True:
                wikipedia.set_lang("fa")
                try:
                    c=wikipedia.search(m,3)
                    x=wikipedia.summary(c[0],sentences=5)
                    y=page_py.fullurl
                    sendMessage(chat_id,f'{x}\n{y}')
                    links= read_json()
                    username = msg['message']['from']['username']
                    if username not in links.keys():
                        links[username]=[]
                    links[username].append(y)
                    write_json(links)
                except wikipedia.exceptions.DisambiguationError as e:
                    s=random.choice(e.options)
                    x=wikipedia.summary(s,sentences=5)
                    y=page_py.fullurl
                    sendMessage(chat_id,f'{x}\n{y}')
                    links= read_json()
                    username = msg['message']['from']['username']
                    if username not in links.keys():
                        links[username]=[]
                    links[username].append(y)
                    write_json(links)
            elif page_py.exists()==False:
                sendMessage(chat_id,'This topic was not found')
        elif 'en' in text:
            m=text.split(maxsplit=1)[1]
            wiki_wiki = wikipediaapi.Wikipedia('en')
            page_py = wiki_wiki.page(m)
            if page_py.exists()==True:
                wikipedia.set_lang("en")
                try:
                    c=wikipedia.search(m,3)
                    x=wikipedia.summary(c[0],sentences=5)
                    y=page_py.fullurl
                    sendMessage(chat_id,f'{x}\n{y}')
                    links= read_json()
                    username = msg['message']['from']['username']
                    if username not in links.keys():
                        links[username]=[]
                    links[username].append(y)
                    write_json(links)
                except wikipedia.exceptions.DisambiguationError as e:
                    s=random.choice(e.options)
                    x=wikipedia.summary(s,sentences=5)
                    y=page_py.fullurl
                    sendMessage(chat_id,f'{x}\n{y}')
                    links= read_json()
                    username = msg['message']['from']['username']
                    if username not in links.keys():
                        links[username]=[]
                    links[username].append(y)
                    write_json(links)  
            elif page_py.exists()==False:
                sendMessage(chat_id,'This topic was not found')
        elif text=='links':
            links= read_json()
            username = msg['message']['from']['username']
            if username not in links.keys():
                sendMessage(chat_id,'شما لینکی ندارید!!')
            else:
                for y in links[username]:
                    sendMessage(chat_id,y)    
        else:
            sendMessage(chat_id ,f'ببخشید!!\nلطفا به صورت زیر وارد کنید\nبرای مثال: en language')
        return Response('ok', status=200)
    else:
        return "<h1>telegrambot</h1>" 
def write_json(data, filename="contactList.json"):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)
def read_json(filename="contactlist.json"):
    with open(filename, 'r') as target:
        data = json.load(target) 
    return data
try:
    read_json() 
except:
    write_json({})                                    
app.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))
    

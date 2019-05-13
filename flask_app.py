# -*- coding: utf-8 -*-
from flask import Flask, request
import random
import logging
import json

from image_search import upload_to_alisa, find_image, delete_image_from_alisa

app = Flask(__name__)


logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

phrases = ['Вот.', 'Держите.', 'Смотрите.', 'Показываю.', 'Вот что мне удалось найти.']
image_id = ''
last_theme = ''
sessionStorage = {}
cnt = 0

@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    global image_id
    global cnt
    global last_theme
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови своё имя!'
        sessionStorage[user_id] = {
            'first_name': None,
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = f'Приятно познакомиться, {first_name.title()}. Я Алиса. Я могу показать вам любую вещь!'
    else:
        delete_image_from_alisa(image_id)
        city = get_cities(req)
        if True:
            key_word = ''
            text = req['request']['original_utterance']
            if 'мне' in text.lower() and ('покажи' in text.lower() or 'покажите' in text.lower()):
                key_word = 'мне'
            elif 'покажи' in text.lower():
                key_word = 'покажи'
            elif 'покажите' in text.lower():
                key_word = 'покажите'
            elif text.lower() == 'еще' or text.lower() == 'ещё':
                cnt += 1
                if cnt > 7:
                    res['response']['text'] = sessionStorage[user_id]['first_name'] + ', с вас хватит!'
                else:
                    url = find_image(last_theme, cnt)
                    image_id = upload_to_alisa(url)
                    res['response']['card'] = {}
                    res['response']['card']['type'] = 'BigImage'
                    res['response']['card']['image_id'] = image_id
                    res['response']['card']['title'] = random.choice(phrases)
                    res['response']['text'] = 'То что вы искали'
                return
            else:
                res['response']['text'] = sessionStorage[user_id]['first_name'] + ', я не поняла вашу комманду!'
                return
            words = text.split()
            key_word_id = -1
            for i in range(len(words)):
                word = words[i]
                if word == key_word:
                    key_word_id = i
                    break
            theme = ' '.join(words[(key_word_id + 1)::])
            last_theme = theme
            cnt = 1
            url = find_image(theme, cnt)
            image_id = upload_to_alisa(url)
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = image_id
            res['response']['card']['title'] = random.choice(phrases)
            res['response']['text'] = 'То что вы искали'
            return


def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])
    return cities


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    app.run()
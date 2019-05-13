# -*- coding: utf-8 -*-
import requests
import json

api_key = 'AIzaSyA1jushlALDuv4iKuEqBIFtxbafUsL8FTA'
cx = '005180411865622881391:-vcpbmb-lnm'

yandex_token = 'OAuth AQAAAAAetW5AAAT7oxHhSpk8akDUlI4OkmDhvs0'
skill_url = 'https://dialogs.yandex.net/api/v1/skills/e17a6e74-84cc-4866-87b7-cff444c07889/images/'


def upload_to_alisa(image_url):
    print(image_url)
    headers = {
        'Authorization': yandex_token,
        'Content-Type': 'application/json'
    }
    data = {
        'url': image_url
    }
    response = requests.post(skill_url, data=json.dumps(data), headers=headers)
    res_json = response.json()
    print(res_json)
    image_id = res_json['image']['id']
    return image_id



def find_image(theme, cnt):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(theme)
    url = 'https://www.googleapis.com/customsearch/v1?cx=005180411865622881391:-vcpbmb-lnm&q={}&num={}&searchType=image&safe=off&key=AIzaSyA1jushlALDuv4iKuEqBIFtxbafUsL8FTA&alt=json'.format(theme, str(cnt))
    req = requests.get(url)
    req = req.json()
    try:
        return req['items'][-1]['image']['thumbnailLink']
    except Exception:
        return 'https://st2.depositphotos.com/7023650/9863/v/950/depositphotos_98631012-stock-illustration-404-error-page-not-found.jpg'


def delete_image_from_alisa(image_id):
    headers = {
        'Authorization': yandex_token,
    }
    url = skill_url + str(image_id)
    try:
        response = requests.delete(url, headers=headers)
        return 'ok'
    except Exception:
        return 'something went wrong'

#print(find_image('кота'))
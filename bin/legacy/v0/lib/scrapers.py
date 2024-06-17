#!/usr/bin/env 

import json
import os
import requests
import pprint
import subprocess
from bs4 import BeautifulSoup
from icecream import ic
from lxml import etree

from lib.config import Config


GENRES_JSON = json.load(open(Config.JSON+'/library/genres.json'))

COMMON_HEADERS = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
}


## GIANT BOMB
GB_API_KEY = Config.GB_API_KEY
GB_HEADERS = {
        'Host': 'www.giantbomb.com',
    }
GB_HEADERS.update(COMMON_HEADERS)

def gb_query(slug):
    query_url = 'https://'+GB_HEADERS['Host']+'/api/search/?api_key='+GB_API_KEY+'&format=json&query='+slug+'&resources=game&resource_type&field_list=guid,name,original_release_date'

    query_request = requests.get(query_url, headers=GB_HEADERS)

    query_data = query_request.json()['results']

    if len(query_data) > 1:
        for q in query_data:
            print(q['guid'], q['name'], q['original_release_date'])
        guid = input("\nEnter GUID: ")
    else:
        guid = query_data[0]['guid']
    
    return guid

def gb_game(guid):
    game_data = {}
    game_url = 'http://'+GB_HEADERS['Host']+'/api/game/'+str(guid)+'/?api_key='+GB_API_KEY+'&format=json&field_list=deck,developers,franchises,image,genres,name,original_game_rating,original_release_date,publishers,themes'

    game_json = requests.get(game_url, headers=GB_HEADERS).json()

    name = game_json['results']['name']
    game_data.update({'title': name})

    description = game_json['results']['deck']
    game_data.update({'description': description})

    developers = game_json['results']['developers']
    game_data.update({'developer': developers[0]['name']})
    
    publishers = game_json['results']['publishers']
    game_data.update({'publisher': publishers[0]['name']})

    try:
        genres = game_json['results']['genres']
        for G in GENRES_JSON:
            if genres[0]['id'] == G['gb_id']:
                genre_id = G['id']
                genre_name = G['name']
    except UnboundLocalError:
        genre_id = None
        genre_name = None
        game_data.update({'genre_name': genre_name})
        game_data.update({'genre_id': genre_id})

    tag_array = []
    tags = game_json['results']['themes']
    for tag in tags:
        tag_array.append(tag['name'])
    tag_string = ', '.join(tag_array)
    game_data.update({'tags': tag_string})

    release_date = game_json['results']['original_release_date']
    try:
        year = release_date[:4]
    except TypeError:
        year = None

    game_data.update({'year': year})

    try:
        ratings = game_json['results']['original_game_rating']
        for rating in ratings:
            if 'ESRB:' in rating['name']:
                esrb_string = rating['name'].split(': ')
                esrb = esrb_string[1]
                break
    except:
        esrb = None

    game_data.update({'esrb': esrb})

    return game_data

def gb_scraper(slug):
    guid = gb_query(slug)
    gb_data = gb_game(guid)

    return gb_data


## MOBY GAMES
MG_API_KEY = Config.MG_API_KEY
MG_HEADERS = {
    'Host': 'api.mobygames.com',
}
MG_HEADERS.update(COMMON_HEADERS)

def mg_query(slug):
    query_url = 'https://www.mobygames.com/search/?q='+slug
    r = requests.get(query_url)
    a_link = BeautifulSoup(r.text, 'html.parser').select('table')[0].select('tr')[0].select('link')[0].select('a')[0].get_attribute_list('href')[0]
    mg_id = a_link.split('/')[4]

    return mg_id

def mg_game(mg_id):
    game_data = {}
    game_url = 'https://'+MG_HEADERS['Host']+'/v1/games/'+mg_id+'?api_key='+MG_API_KEY+'&format=normal'
    r = requests.get(game_url, headers=MG_HEADERS).json()
    game_data.update({"game_id": r['game_id']})
    game_data.update({"title": r['title']})
    game_data.update({"description": r['description']})
    game_data.update({"genre": r['genres'][0]['genre_name']})
    game_data.update({"genre_id": r['genres'][0]['genre_id']})
    game_data.update({"moby_score": r['moby_score']})
    game_data.update({"official_url": r['official_url']})

    return game_data

def mg_scraper(slug):
    mg_id = mg_query(slug)
    mg_data = mg_game(mg_id)
    return mg_data


## SKY SCRAPER
# def sky_scraper(platform_slug):
#     subprocess.run['skyscraper', '-p', platform_slug, '-s', 'screenscraper']

## METACRITIC SCORE
def mc_score(slug):
    MC_HEADERS = {
        'Host': 'www.metacritic.com'
    }
    MC_HEADERS.update(COMMON_HEADERS)

    game_url = 'http://'+MC_HEADERS['Host']+'/game/'+slug
    r = requests.get(game_url, headers=MC_HEADERS)
    ic(r.status_code)

    if r.status_code == 200:
        try:
            html = BeautifulSoup(r.text, 'html.parser')
            score_number = html.select('div.c-productScoreInfo_scoreNumber')[0]
            review_score_div = score_number.select('.c-siteReviewScore')[0]
            metacritic_score = review_score_div.select('span')[0].get_text()
        except:
            metacritic_score = None
    else:
        metacritic_score = None

    return metacritic_score

## DEBUG
# ic(os.getenv('APP_ID'), os.getenv('APP_TITLE'), os.getenv('EDITOR'), os.getenv('USER'), os.getenv('MG_API_KEY'), os.getenv('GB_API_KEY'))

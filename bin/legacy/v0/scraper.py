#!/usr/bin/env python

import collections
import datetime
import os
import requests
import sqlite3
import sys

from bs4 import BeautifulSoup
from lib.extensions import Config
from icecream import ic

PLATFORM = sys.argv[1]
FILENAME = sys.argv[2]
FILEBASE = os.path.basename(FILENAME)

# Connect to database
try:
    CONNECTION = sqlite3.connect(Config.DB)
    CURSOR = CONNECTION.cursor()
except sqlite3.OperationalError as e:
    ic('Could not find database.', e)
    exit()

# Get  `genre` table
CURSOR.execute('SELECT id, name FROM genre where 1;')
GENRES = CURSOR.fetchall()

# Get  `platform` table
CURSOR.execute('SELECT id, slug FROM platform where 1;')
PLATFORMS = CURSOR.fetchall()

COMMON_HEADERS = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
}

# GIANT BOMB
GB_API_KEY = Config.GB_API_KEY
GB_HEADERS = {
    'Host': 'www.giantbomb.com',
}
GB_HEADERS.update(COMMON_HEADERS)


def check_filename(filename):
    CURSOR.execute('SELECT id, title FROM game WHERE filename == "' + FILEBASE + '"')
    result = CURSOR.fetchone()
    if result:
        print(result[1], 'already in database.')
        exit()
    else:
        print(filename, 'not found. Adding to database.')


def gb_query(slug):
    query_url = 'https://' + GB_HEADERS['Host'] + '/api/search/?api_key=' + GB_API_KEY + '&format=json&query=' \
                + slug + '&resources=game&resource_type&field_list=guid,name,original_release_date'

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
    esrb = None
    game_data = {}
    game_url = 'http://' + GB_HEADERS['Host'] + '/api/game/' + str(guid) + '/?api_key=' + GB_API_KEY \
               + '&format=json&field_list=deck,developers,franchises,image,genres,name,\
               original_game_rating,original_release_date,publishers,themes'

    game_json = requests.get(game_url, headers=GB_HEADERS).json()
    name = game_json['results']['name']
    game_data.update({'title': name})
    description = game_json['results']['deck']
    game_data.update({'description': description})

    try:
        developers = game_json['results']['developers']
        game_data.update({'developer': developers[0]['name']})
    except TypeError as err:
        print(err)
        game_data.update({'developer': None})

    try:
        publishers = game_json['results']['publishers']
        game_data.update({'publisher': publishers[0]['name']})
    except TypeError as err:
        print(err)
        game_data.update({'publisher': None})

    try:
        genres = game_json['results']['genres']
    except KeyError as err:
        print(err)
        genres = None
        game_data.update({'genre_id': None})

    if genres:
        for G in GENRES:
            if genres[0]['id'] == G[0]:
                genre_id = G[0]
                game_data.update({'genre_id': genre_id})
                break

    try:
        tag_array = []
        tags = game_json['results']['themes']
        for tag in tags:
            tag_array.append(tag['name'])
        tag_string = ', '.join(tag_array)
        game_data.update({'tags': tag_string})
    except KeyError:
        game_data.update({'tags': None})

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
    except Exception as err:
        print(err)
        esrb = None

    try:
        game_data.update({'esrb': esrb})
    except UnboundLocalError as err:
        print(err)
        print('Could not get esrb rating.')
        game_data.update({'esrb': None})

    return game_data


def gb_scraper(slug):
    guid = gb_query(slug)
    scraper_data = gb_game(guid)

    return scraper_data


# MOBY GAMES
MG_API_KEY = Config.MG_API_KEY
MG_HEADERS = {
    'Host': 'api.mobygames.com',
}
MG_HEADERS.update(COMMON_HEADERS)


def mg_query(filename):
    file_query = 'SELECT filename from game WHERE filename == "' + filename + '"'
    CURSOR.execute(file_query)
    file_query = CURSOR.fetchone()
    ic(file_query)
    if file_query:
        print(file_query[0] + ' is already in the database.')
        exit()

    print('Scraping data for ' + filename)
    slug = filename.split('.')[0]
    query_url = 'https://www.mobygames.com/search/?q=' + slug
    r = requests.get(query_url)
    a_link = BeautifulSoup(r.text, 'html.parser').select('table')[0].select('tr')[0].select('link')[0].select('a')[
        0].get_attribute_list('href')[0]
    mg_id = a_link.split('/')[4]

    return mg_id


def mg_game(mg_id):
    game_data = {}

    game_data.update({"filename": FILEBASE})

    for id, slug in PLATFORMS:
        if PLATFORM == slug:
            print(id, slug)
            game_data.update({"platform_id": id})
            break

    game_url = 'https://' + MG_HEADERS['Host'] + '/v1/games/' + mg_id + '?api_key=' + MG_API_KEY + '&format=normal'
    r = requests.get(game_url, headers=MG_HEADERS).json()
    try:
        game_data.update({"title": r['title']})
        game_data.update({"genre_id": r['genres'][0]['genre_id']})
    except KeyError as err:
        print('URL query failed.', err)
        tmp_title = FILEBASE.split('.')[0].replace('-', ' ').title()
        game_data.update({"title": tmp_title})
        game_data.update({"genre_id": None})

    return game_data


def mg_scraper(filename):
    mg_id = mg_query(filename)
    scraper_data = mg_game(mg_id)
    return scraper_data


# SKY SCRAPER
# def sky_scraper(platform_slug):
#     subprocess.run['skyscraper', '-p', platform_slug, '-s', 'screenscraper']

# METACRITIC SCORE
def mc_score(slug):
    mc_headers = {
        'Host': 'www.metacritic.com'
    }
    mc_headers.update(COMMON_HEADERS)

    game_url = 'http://' + mc_headers['Host'] + '/game/' + slug
    r = requests.get(game_url, headers=mc_headers)
    ic(r.status_code)

    if r.status_code == 200:
        try:
            html = BeautifulSoup(r.text, 'html.parser')
            score_number = html.select('div.c-productScoreInfo_scoreNumber')[0]
            review_score_div = score_number.select('.c-siteReviewScore')[0]
            metacritic_score = review_score_div.select('span')[0].get_text()
        except Exception as err:
            print(err)
            metacritic_score = None
    else:
        metacritic_score = None

    return metacritic_score



check_filename(FILEBASE)

search_string = FILEBASE.split('.')[0].replace('-', ' ')

mg_data = mg_scraper(search_string)
gb_data = gb_scraper(search_string)
mg_data.update({
    "id": None,
    "alt_title": None,
    "archived": None,
    "co_op": None,
    "collection_id": None,
    "controller_support": 1,
    "date_added": datetime.datetime.now(),
    "date_modified": datetime.datetime.now(),
    "description": gb_data['description'],
    "developer": gb_data['developer'],
    "esrb": gb_data['esrb'],
    "favorite": None,
    "gpu": None,
    "hdd": None,
    "last_played": None,
    "mod": None,
    "notes": None,
    "online_multiplayer": None,
    "operating_system": None,
    "play_count": None,
    "players": 1,
    "processor": None,
    "publisher": gb_data['publisher'],
    "ram": None,
    "region": "NA",
    "save_path": None,
    "steam_id": None,
    "store": None,
    "tags": gb_data['tags'],
    "translation": None,
    "year": gb_data['year']
})

mg_data_ordered = collections.OrderedDict(sorted(mg_data.items()))

query = "INSERT INTO game ('alt_title', 'archived', 'co_op', 'collection_id', 'controller_support', 'date_added',\
    'date_modified', 'description', 'developer', 'esrb', 'favorite', 'filename', 'genre_id', 'gpu', 'hdd', 'id', \
    'last_played', 'mod', 'notes', 'online_multiplayer', 'operating_system', 'platform_id', 'play_count', \
    'players', 'processor', 'publisher', 'ram', 'region', 'save_path', 'steam_id', 'store', 'tags', 'title', \
    'translation', 'year') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

values = tuple(mg_data_ordered.values())

CURSOR.execute(query, values)
CONNECTION.commit()
CONNECTION.close()

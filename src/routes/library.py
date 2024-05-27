import base64
import datetime
import markdown
import os
import requests
import subprocess
from io import BytesIO

from flask import Blueprint, flash, render_template, request, redirect, url_for
from wand.image import Image

from lib.extensions import db, Config, Utils
from forms.library import CollectionForm, GameForm
from models.library import Collection, Game, Genre, Platform

library_bp = Blueprint('library', __name__)


def get_css(file):
    with open(file, 'r') as f:
        print(file)
        css = f.read()
    return css


def mm_to_px(mm):
    pixels = mm * 3.7795275591
    pixels = round(pixels, 0)
    pixels = int(pixels)
    return pixels


# CONTEXT PROCESSORS
@library_bp.context_processor
def utility_processor():
    def debug_info():
        if Config.DEBUG:
            info = {}
            info.update({'app_title': Config.APP_TITLE})
            info.update({'debug': Config.DEBUG})
        else:
            info = None
        return info

    return {'debug_info': debug_info}


# ROUTES
@library_bp.route('/')
def home():
    # page = request.args.get('page', 1, type=int)
    pagination = Game.query.order_by(
        Game.date_added.desc()
    ).paginate(per_page=50, max_per_page=100)
    return render_template('library/home/index.html', pagination=pagination)


# GAMES
@library_bp.route('/library/game/new', methods=('GET', 'POST'))
def game_add():
    ga_collections = [
        (c.name, c.id) for c in Collection.query.order_by('name')]
    ga_genres = [(g.name, g.id) for g in Genre.query.order_by('name')]
    ga_platforms = [(p.name, p.id) for p in Platform.query.order_by('name')]
    form = GameForm()
    game = None
    if request.method == 'POST' and form.validate_on_submit():
        game = Game(
            archived=form.archived.data,
            co_op=form.co_op.data,
            collection_id=form.collection_id.data,
            controller_support=form.controller_support.data,
            description=form.description.data,
            developer=form.developer.data,
            esrb=form.esrb.data,
            favorite=form.favorite.data,
            filename=form.filename.data,
            genre_id=form.genre_id.data,
            gpu=form.gpu.data,
            hdd=form.hdd.data,
            mod=form.mod.data,
            notes=form.notes.data,
            online_multiplayer=form.online_multiplayer.data,
            operating_system=form.operating_system.data,
            platform_id=form.platform_id.data,
            players=form.players.data,
            processor=form.processor.data,
            publisher=form.publisher.data,
            ram=form.ram.data,
            region=form.region.data,
            save_path=form.save_path.data,
            steam_id=form.steam_id.data,
            store=form.store.data,
            tags=form.tags.data,
            title=form.title.data,
            translation=form.translation.data,
            year=form.year.data,
            date_added=datetime.datetime.now(),
            date_modified=datetime.datetime.now()
        )
        db.session.add(game)
        db.session.commit()
        flash('Game saved.')
    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Could not save game.')
    return render_template(
        'library/game/add.html',
        collections=ga_collections,
        form=form,
        genres=ga_genres,
        game=game,
        platforms=ga_platforms)


@library_bp.route('/library/game/delete/<int:game_id>')
def game_delete(game_id):
    '''Remove game from database.

    Args:
        game_id (integer): Game ID
    '''
    try:
        # Game.query.filter(Game.id == game_id).delete()
        game = Game.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        flash('Game successfully deleted.')
    except Exception as e:
        flash('Error: game *not* deleted.')
        print(e)
    return redirect(url_for('library.home'))


@library_bp.route('/library/game/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)

    try:
        desc = markdown.markdown(game.description)
    except AttributeError:
        desc = None

    try:
        notes = markdown.markdown(game.notes)
    except AttributeError:
        notes = None

    platform = Platform.query.get_or_404(game.platform_id)
    file_path = Utils.get_filepath(platform.slug, game.filename)
    if os.path.exists(file_path):
        installed = True
    else:
        installed = False
    boxart_dir = Config.MEDIA + '/games/' + game.platform.slug + '/boxart/'
    boxart_file = game.slug() + '.jpg'
    boxart_url = boxart_dir + '/' + boxart_file
    if os.path.exists(boxart_url):
        boxart = boxart_url
    else:
        boxart = None

    return render_template(
        'library/game/detail.html',
        theme='print',
        boxart=boxart,
        boxart_url=boxart_url,
        desc=desc,
        game=game,
        file_path=file_path,
        installed=installed,
        notes=notes)


@library_bp.route('/library/game/edit/<int:game_id>', methods=('GET', 'POST'))
def game_edit(game_id):
    game = Game.query.get_or_404(game_id)
    ge_collections = [
        (c.name, c.id) for c in Collection.query.order_by('name')]
    ge_genres = [(g.name, g.id) for g in Genre.query.order_by('name')]
    ge_platforms = [(p.name, p.id) for p in Platform.query.order_by('name')]

    form = GameForm()

    if request.method == 'POST' and form.validate_on_submit():
        if form.alt_title.data == 'None' or form.alt_title.data == '':
            game.alt_title = None
        else:
            game.alt_title = form.alt_title.data

        game.archived = form.archived.data
        game.co_op = form.co_op.data

        if form.collection_id.data == 0:
            game.collection_id = None
        else:
            game.collection_id = form.collection_id.data

        game.controller_support = form.controller_support.data

        if form.description.data == 'None':
            game.description = None
        else:
            game.description = form.description.data

        if game.developer == 'None':
            game.developer = None
        else:
            game.developer = form.developer.data

        if form.esrb.data == 'None':
            game.esrb = None
        else:
            game.esrb = form.esrb.data

        game.favorite = form.favorite.data
        game.filename = form.filename.data
        game.genre_id = form.genre_id.data

        if form.gpu.data == 'None':
            game.gpu = None
        else:
            game.gpu = form.gpu.data

        if form.hdd.data == 'None':
            game.hdd = None
        else:
            game.hdd = form.hdd.data

        if form.mod.data == 'None':
            game.mod = None
        else:
            game.mod = form.mod.data

        if form.notes.data == 'None':
            game.notes = None
        else:
            game.notes = form.notes.data

        game.online_multiplayer = form.online_multiplayer.data

        if form.operating_system.data == 'None':
            game.operating_system = None
        else:
            game.operating_system = form.operating_system.data

        game.platform_id = form.platform_id.data
        game.players = form.players.data

        if form.processor.data == 'None':
            game.processor = None
        else:
            game.processor = form.processor.data

        if form.publisher.data == 'None':
            game.publisher = None
        else:
            game.publisher = form.publisher.data

        if form.ram.data == 'None':
            game.ram = None
        else:
            game.ram = form.ram.data

        game.region = form.region.data

        if form.save_path.data == 'None':
            game.save_path = None
        else:
            game.save_path = form.save_path.data

        if form.steam_id.data == 'None':
            game.steam_id = None
        else:
            game.steam_id = form.steam_id.data

        if form.store.data == '':
            game.store = None
        else:
            game.store = form.store.data

        game.tags = form.tags.data
        game.title = form.title.data
        game.translation = form.translation.data
        game.year = form.year.data

        game.date_modified = datetime.datetime.now()

        db.session.commit()
        flash("Game data was saved.")
        return redirect(url_for('library.game_detail', game_id=game.id))
    elif request.method == 'POST' and not form.validate_on_submit():
        flash("Game data was *not* saved. Please check the log for errors.")
    return render_template('library/game/edit.html',
                           game=game,
                           collections=ge_collections,
                           genres=ge_genres,
                           form=form,
                           platforms=ge_platforms)


# @library_bp.route('/library/game/<int:game_id>/readme')
# def game_readme(game_id):
#     game = Game.query.get_or_404(game_id)
#     if game.description:
#         description = markdown.markdown(game.description)
#     else:
#         description = None

#     if game.notes:
#         notes = markdown.markdown(game.notes)
#     else:
#         notes = None

#     logo_dir = os.path.join(Config.MEDIA, 'games')
#     logo_dir = os.path.join(logo_dir, game.platform.slug)
#     logo_dir = os.path.join(logo_dir, 'logo')
#     logo_file = game.slug() + '.png'
#     logo_url = os.path.join(logo_dir, logo_file)

#     if os.path.exists(logo_url):
#         with open(logo_url, 'rb') as logo_file:
#             logo_data = base64.b64encode(logo_file.read())
#             logo = logo_data.decode('utf-8')
#     else:
#         logo = None

#     return render_template(
#         '/library/game/readme.html',
#         game=game,
#         description=description,
#         logo=logo,
#         notes=notes)

@library_bp.route('/library/game/<int:game_id>/readme')
def game_readme(game_id):
    game = Game.query.get_or_404(game_id)

    # Make large text fields HTML safe
    if game.description:
        description = markdown.markdown(game.description)
    else:
        description = None

    if game.notes:
        notes = markdown.markdown(game.notes)
    else:
        notes = None

    # Search for hero or box art
    game_art_url = None
    media_dir = os.path.join(Config.MEDIA, 'games', game.platform.slug)
    boxart_img = os.path.join(media_dir, 'boxart', game.slug() + '.jpg')
    hero_img = os.path.join(media_dir, 'hero', game.slug() + '.jpg')

    # Set page dimensions
    page_width = mm_to_px(216)
    fig_max_width = mm_to_px(89)
    fig_max_height = mm_to_px(108)

    if os.path.exists(hero_img):
        game_art_url = hero_img
        game_art_type = 'hero'
    elif os.path.exists(boxart_img):
        game_art_url = boxart_img
        game_art_type = 'boxart'

    # Convert game art to data and resize
    if game_art_url:
        game_art_data = BytesIO()
        with Image(filename=game_art_url) as img:
            with img.clone() as i:
                if game_art_type == 'hero':
                    i.transform(resize=str(page_width) + 'x')
                elif game_art_type == 'boxart':
                    if i.width >= i.height:
                        i.transform(resize=str(fig_max_width) + 'x')
                        game_art_type = 'landscape'
                    else:
                        i.transform(resize='x' + str(fig_max_height))
                        game_art_type = 'portrait'
                i.save(game_art_data)

                game_art_data = base64.b64encode(game_art_data.getvalue())
                game_art = game_art_data.decode('utf-8')

    # Get inline css content
    css_path = os.path.join(
        Config.APP_DIR,
        'static',
        'assets',
        'css',
        'themes',
        'print.min.css'
    )
    css = get_css(css_path)

    return render_template(
        '/library/game/readme.html',
        theme='print',
        css=css,
        game=game,
        description=description,
        game_art=game_art,
        game_art_type=game_art_type,
        notes=notes)


@library_bp.route('/library/game/favorites')
def favorites():
    pagination = Game.query.filter(Game.favorite).paginate(
        per_page=25,
        max_per_page=100)
    return render_template(
        '/library/game/favorites.html', pagination=pagination)


# Collections
@library_bp.route('/library/collections')
def collections():
    collections_index = Collection.query.order_by(Collection.name)
    return render_template(
        'library/collection/index.html', collections=collections_index)


@library_bp.route('/library/collections/new', methods=('GET', 'POST'))
def collection_add():
    form = CollectionForm()
    if request.method == 'POST' and form.validate_on_submit():
        collection = Collection(
            name=form.name.data,
            description=form.description.data)
        db.session.add(collection)
        db.session.commit()
        flash('Collection saved.')
        return redirect(url_for('library.collections'))
    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Could not save collection.')
    return render_template('library/collection/add.html', form=form)


@library_bp.route('/library/collection_detail/<int:collection_id>')
def collection_detail(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    pagination = Game.query.filter(
        Game.collection_id == collection.id).order_by(Game.year).paginate(
            per_page=50,
            max_per_page=100)
    return render_template(
        'library/collection/detail.html',
        collection=collection,
        pagination=pagination)


@library_bp.route(
    '/library/collection/edit/<int:collection_id>', methods=('GET', 'POST'))
def collection_edit(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    form = CollectionForm()
    if request.method == 'POST' and form.validate_on_submit():
        collection.name = form.name.data
        collection.description = form.description.data
        db.session.commit()
        flash('Collection saved.')
        return redirect(
            url_for(
                'library.collection_detail',
                collection_id=collection_id))
    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Could not save collection.')
    return render_template(
        'library/collection/edit.html', collection=collection, form=form)


@library_bp.route('/library/genres')
def genres():
    genres_index = Genre.query.all()
    return render_template('library/genre/index.html', genres=genres_index)


@library_bp.route('/library/platforms')
def platforms():
    platforms_index = Platform.query.order_by('name')
    return render_template(
        'library/platform/index.html',
        platforms=platforms_index)


@library_bp.route('/library/platform/<int:platform_id>')
def platform_detail(platform_id):
    platform = Platform.query.get_or_404(platform_id)
    pagination = (Game.query.filter(Game.platform_id == platform_id)
                  .order_by(Game.title)
                  .paginate(per_page=50, max_per_page=100))
    return render_template(
        'library/platform/detail.html',
        platform=platform,
        pagination=pagination)


@library_bp.route('/library/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        pagination = Game.query.filter(
            (Game.title.like('%' + query + '%')) |
            (Game.alt_title.like('%' + query + '%')) |
            (Game.developer.like('%' + query + '%')) |
            (Game.publisher.like('%' + query + '%')) |
            (Game.tags.like('%' + query + '%'))).paginate(
                per_page=25, max_per_page=100)
    else:
        pagination = None
    return render_template(
        'library/search.html',
        query=query,
        pagination=pagination)


# TAGS
@library_bp.route('/library/tags')
def tags():
    tags_api = request.host_url + url_for('api.tags')
    tags_index = requests.get(tags_api).json()
    return render_template('library/tags/index.html', tags=tags_index)


@library_bp.route('/library/tags/detail', methods=['GET'])
def tag_detail():
    query = request.args.get('query')
    if query:
        pagination = Game.query\
            .filter(Game.tags.like('%' + query + '%'))\
            .paginate(per_page=25, max_per_page=100)
    else:
        pagination = None
    return render_template(
        'library/tags/detail.html',
        query=query,
        pagination=pagination)


@library_bp.route('/launch/game/<string:platform_slug>/<string:filename>')
def launch_game(platform_slug, filename):
    try:
        subprocess.run([
            'game-launcher',
            platform_slug,
            Utils.get_filepath(platform_slug, filename)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        launch_message = 'Game launched successfully.'
    except Exception as e:
        launch_message = 'Error launching game.'
        print(e)
    return launch_message

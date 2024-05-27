from datetime import datetime
from lib.extensions import db


class Collection(db.Model):
    '''Group games by collection. Related to Game.collection_id.

    Attributes:
        id (int): Collection ID
        name (str): Collection name
        description (txt): Brief description of Collection
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text(1024))
    games = db.relationship('Game', backref='collection')

    def __repr__(self):
        return f'{self.name}'


class Genre(db.Model):
    '''Related to Game.genre_id

    Attributes:
        id (int): Genre ID
        name (str): Genre name
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    games = db.relationship('Game', backref='genre')
    legacy_id = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return f'{self.name}'


class Platform(db.Model):
    '''Related to Game.platform_id

    Attributes:
        id (int): Platform ID
        slug: Platform slug ID
        core: Retroarch core (optional)
        launcher (str): Platform executable (optional)
        name: Platform full name
    '''
    id = db.Column(db.Integer, primary_key=True)
    launcher = db.Column(db.String(128))
    name = db.Column(db.String(128), unique=True)
    slug = db.Column(db.String(128), unique=True)
    core = db.Column(db.String(128))
    games = db.relationship('Game', backref='platform')

    def __repr__(self):
        return f'{self.name}'


class Game(db.Model):
    '''Game Model

    Attributes:
        id (str): Game ID
        alt_title (str): Alternative game title
        archived (bool): Game has been backed up to physical media
        co_op (bool): Co-op multiplayer
        collection_id (int): Collection ID
        controller_support (int): Controller/gamepad support
        date_added (date): Date added to database
        date_modified (date): Date game was last modified in database
        description (txt): Game description
        developer (str): Developer
        esrb (str): ESRB rating
        favorite (bool): Add game to `Favorites` collection
        file_name (str): File name and main identifier for game
        genre_id (int): Genre ID
        gpu (str): GPU requirement
        hdd (str): Hard disk space requirement
        last_played (date): Date game was last launched
        mod (str): Mod or engine
        notes (txt): Add'l notes
        online_multiplayer (bool): Online Multiplayer
        operating_system (str): Operating system requirement
        platform_id (int): Platform ID
        play_count (int): No. of times game has been launched
        players (int): No. of players
        processor (str): Processor requirement
        publisher (str): Publisher
        ram (str): RAM requirement
        region (str): Game region
        save_path (str): Save path
        steam_id (int): Steam ID
        store (str): Where game was purchased
        tags (arr): Game descriptors
        title (str): Game title
        translation (bool): Game has been translated from native version.
        year (int): Release date
    '''
    id = db.Column(db.Integer, primary_key=True)
    alt_title = db.Column(db.String(128), unique=True)
    archived = db.Column(db.Boolean, default=0)
    co_op = db.Column(db.Boolean, default=0)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    controller_support = db.Column(db.Boolean, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text(8192))
    developer = db.Column(db.String(128))
    esrb = db.Column(db.String(4))
    favorite = db.Column(db.Boolean, default=0)
    filename = db.Column(db.String(128), nullable=False, unique=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    gpu = db.Column(db.String(64))
    hdd = db.Column(db.String(64))
    last_played = db.Column(db.DateTime)
    mod = db.Column(db.String(64))
    notes = db.Column(db.Text(8192))
    online_multiplayer = db.Column(db.Boolean, default=0)
    operating_system = db.Column(db.String(64))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    play_count = db.Column(db.Integer, default=0)
    players = db.Column(
        db.Integer,
        db.CheckConstraint('players >= 1 AND players <= 64'),
        default=1)
    processor = db.Column(db.String(64))
    publisher = db.Column(db.String(128))
    ram = db.Column(db.String(64))
    region = db.Column(db.String(2))
    save_path = db.Column(db.String(256))
    steam_id = db.Column(db.Integer)
    store = db.Column(db.String(32))
    tags = db.Column(db.String(128))
    title = db.Column(db.String(128), nullable=False)
    translation = db.Column(db.Boolean, default=0)
    year = db.Column(
        db.Integer,
        db.CheckConstraint('year >= 1948 AND players < 9999'))

    def __repr__(self):
        return f'{self.title}'

    def slug(self):
        slug = self.filename.split('.')[0]
        return slug

    def sort_title(self):
        if self.title.endswith(', The') or self.title.endswith(', A'):
            x, y = self.title.split(', ')
            sort_title = str(y + ' ' + x)
        else:
            sort_title = self.title
        return sort_title

    def tag_array(self):
        tag_array = []
        tag_string = self.tags.split(',')
        for t in tag_string:
            tag_array.append(t)
        return tag_array


# class Device(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False, unique=True)
#     mnt_path = db.Column(db.String(128), unique=True)
#     games_path = db.Column(db.String(128), nullable=True, unique=True)

#     def __repr__(self):
#         return f'{self.name}'

#     def device_slug(self):
#         slug = slugify(self.name)
#         return slug

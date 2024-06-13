import os
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import gamedex.settings as settings

ESRB_RATINGS = [
    ('E', 'Everyone'),
    ('E10', 'Everyone 10+'),
    ('T', 'Teen'),
    ('M', 'Mature'),
    ('AO', 'Adults Only')
]

REGIONS = [
    ('NA', 'North America'),
    ('EU', 'Europe'),
    ('JP', 'Japan'),
    ('WO', 'World')
]

STORES = [
    ('BLIZZARD', 'Blizzard'),
    ('EA', 'Eletronic Arts'),
    ('EPIC', 'Epic Games Store'),
    ('GOG', 'GOG.com'),
    ('HUMBLE', 'Humble Bundle'),
    ('ITCH', 'itch.io'),
    ('MSOFT', 'Microsoft Store'),
    ('NINTENDO', 'Nintendo'),
    ('PSN', 'PlayStation Network'),
    ('STEAM', 'Steam'),
    ('OTHER', 'Other')
]

GAME_MEDIA = [
    {'img': 'banner', 'ext': 'jpg'},
    {'img': 'boxart', 'ext': 'jpg'},
    {'img': 'grid', 'ext': 'jpg'},
    {'img': 'hero', 'ext': 'jpg'},
    {'img': 'icon', 'ext': 'png'},
    {'img': 'logo', 'ext': 'png'},
    {'img': 'screenshot', 'ext': 'jpg'},
    {'img': 'wallpaper', 'ext': 'jpg'}
]

SC_FAIL = 'Value entered failed the sanity check'


class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Platform(models.Model):
    core = models.CharField(max_length=200, null=True)
    launcher = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=False)
    slug = models.CharField(max_length=32, null=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Game(models.Model):
    alt_title = models.CharField(blank=True, max_length=200, null=True)
    archived = models.BooleanField(default=False)
    co_op = models.BooleanField(default=False)
    collection = models.ForeignKey('Collection', blank=True, null=True, on_delete=models.SET_NULL,)
    controller_support = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, max_length=8192, null=True)
    developer = models.CharField(blank=True, max_length=200, null=True)
    esrb = models.CharField(blank=True, max_length=3, choices=ESRB_RATINGS, null=True)
    favorite = models.BooleanField(default=False)
    filename = models.CharField(max_length=200, null=False, unique=True)
    game_id = models.CharField(blank=True, max_length=200, null=True)
    genre = models.ForeignKey('Genre', blank=True, null=True, on_delete=models.SET_NULL)
    gpu = models.CharField(blank=True, max_length=200, null=True)
    hdd = models.CharField(blank=True, max_length=64, null=True)
    last_played = models.IntegerField(blank=True, null=True)
    mod = models.CharField(blank=True, max_length=64, null=True)
    notes = models.TextField(blank=True, max_length=8192, null=True)
    online_multiplayer = models.BooleanField(default=False)
    operating_system = models.CharField(blank=True, max_length=64, null=True)
    platform = models.ForeignKey('Platform', on_delete=models.SET_NULL, null=True)
    play_count = models.IntegerField(blank=True, default=0, null=True)
    play_time = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=17)
    players = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message=SC_FAIL),
            MaxValueValidator(256, message=SC_FAIL)])
    processor = models.CharField(blank=True, max_length=200, null=True)
    product_id = models.CharField(blank=True, max_length=200, null=True)
    publisher = models.CharField(blank=True, max_length=200, null=True)
    ram = models.CharField(blank=True, max_length=64, null=True)
    region = models.CharField(blank=True, max_length=3, choices=REGIONS, default='NA', null=True)
    save_path = models.CharField(blank=True, max_length=200, null=True)
    store = models.CharField(blank=True, max_length=8, choices=STORES, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(blank=True, max_length=200, null=False)
    translation = models.BooleanField(default=False)
    year = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1940, message=SC_FAIL),
            MaxValueValidator(2999, message=SC_FAIL)])

    def __str__(self):
        return self.title

    def display_title(self):
        if self.title.endswith(', The') or self.title.endswith(', A'):
            x, y = self.title.split(', ')
            t = str(y + ' ' + x)
        else:
            t = self.title
        return t

    def slug(self):
        f = self.filename.split('.')
        s = f[0]
        return s

    def get_game_media(self):
        platform_root = os.path.join(settings.MEDIA_ROOT, 'games', self.platform.slug)
        platform_url = settings.MEDIA_URL + 'games/' + self.platform.slug
        game_art = []

        for i in GAME_MEDIA:
            path = os.path.join(platform_root, i['img'], self.slug() + '.' + i['ext'])
            if os.path.exists(path):
                img_url = platform_url + '/' + i['img'] + '/' + self.slug() + '.' + i['ext']
                game_art.append({'img': i['img'], 'url': img_url})

        return game_art

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

ESRB_RATINGS = [
    (None, 'None'),
    ('E', 'Everyone'),
    ('E10', 'Everyone 10+'),
    ('T', 'Teen'),
    ('M', 'Mature'),
    ('AO', 'Adults Only')
]

REGIONS = [
    ('NA', 'North America'),
    ('EU', 'Europe'),
    ('JP', 'Japan')
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

SC_FAIL = 'Value entered failed the sanity check'


class Game(models.Model):
    archived = models.BooleanField(default=False)
    co_op = models.BooleanField(default=False)
    collection = models.ForeignKey('Collection', on_delete=models.SET_NULL, null=True)
    controller_support = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=8192, null=True)
    developer = models.CharField(max_length=200, null=True)
    esrb = models.CharField(max_length=3, choices=ESRB_RATINGS, default=None)
    favorite = models.BooleanField(default=False)
    filename = models.CharField(max_length=200, null=False, unique=True)
    game_id = models.CharField(max_length=200, null=True)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    gpu = models.CharField(max_length=200, null=True)
    hdd = models.CharField(max_length=64, null=True)
    last_played = models.DateTimeField(default=timezone.now)
    mod = models.CharField(max_length=64, null=True)
    notes = models.TextField(max_length=8192, null=True)
    online_multiplayer = models.BooleanField(default=False)
    operating_system = models.CharField(max_length=64, null=True)
    platform = models.ForeignKey('Platform', on_delete=models.SET_NULL, null=True)
    play_count = models.IntegerField(default=0)
    players = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message=SC_FAIL),
            MaxValueValidator(256, message=SC_FAIL)])
    processor = models.CharField(max_length=200, null=True)
    product_id = models.CharField(max_length=200, null=True)
    publisher = models.CharField(max_length=200, null=True)
    ram = models.CharField(max_length=64, null=True)
    region = models.CharField(max_length=3, choices=REGIONS, default='NA')
    save_path = models.CharField(max_length=200, null=True)
    store = models.CharField(max_length=8, choices=STORES, default='NA')
    tags = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=False)
    translation = models.BooleanField(default=False)
    year = models.IntegerField(
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


class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class Genre(models.Model):
    name = models.CharField(max_length=200)


class Platform(models.Model):
    core = models.CharField(max_length=200, null=True)
    launcher = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=False)
    slug = models.CharField(max_length=32, null=False)
    description = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=200)
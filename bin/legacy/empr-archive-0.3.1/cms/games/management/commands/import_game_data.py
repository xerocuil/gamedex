from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from games.models import Game

class Command(BaseCommand):
    help = 'Import game data from a csv file.'

    def handle(self, *args, **options):
        for row in DictReader(open('/opt/empr/docs/csv/import_game_data.csv')):
            game=Game(
                title=row['title'],
                sort_title=row['sort_title'],
                controller_support=row['controller_support'],
                date_added=row['date_added'],
                description=row['description'],
                developer=row['developer'],
                esrb=row['esrb'],
                hidden=row['hidden'],
                notes=row['notes'],
                player=row['player'],
                online_multiplayer=row['online_multiplayer'],
                publisher=row['publisher'],
                region=row['region'],
                release_date=row['release_date'],
                store=row['store'],
                genre_id=row['genre_id'],
                platform_id=row['platform_id'],
                boxart=row['boxart'],
                wallpaper=row['wallpaper'],
                favorite=row['favorite'],
                co_op=row['co_op'],
                steam_id=row['steam_id'],
                required_files=row['required_files'],
                gpu=row['gpu'],
                hdd=row['hdd'],
                operating_system=row['operating_system'],
                processor=row['processor'],
                ram=row['ram'],
                archived=row['archived'],
                collection_id=row['collection_id'],
                icon=row['icon'],
                title_image=row['title_image'],
                manual=row['manual'],
                perspective=row['perspective'],
                kid_game=row['kid_game'],
                screenshot=row['screenshot'],
                display=row['display'],
                path=row['path']
            )
            try:
                obj, created = Game.objects.update_or_create(
                    path=game.path,
                    defaults={
                        'title': game.title,
                        'sort_title': game.sort_title,
                        'controller_support': game.controller_support,
                        'date_added': game.date_added,
                        'date_modified': game.date_modified,
                        'description': game.description,
                        'developer': game.developer,
                        'esrb': game.esrb,
                        'hidden': game.hidden,
                        'notes': game.notes,
                        'player': game.player,
                        'online_multiplayer': game.online_multiplayer,
                        'publisher': game.publisher,
                        'region': game.region,
                        'release_date': game.release_date,
                        'store': game.store,
                        'genre_id': game.genre_id,
                        'platform_id': game.platform_id,
                        'boxart': game.boxart,
                        'wallpaper': game.wallpaper,
                        'favorite': game.favorite,
                        'co_op': game.co_op,
                        'required_files': game.required_files,
                        'gpu': game.gpu,
                        'hdd': game.hdd,
                        'operating_system': game.operating_system,
                        'processor': game.processor,
                        'ram': game.ram,
                        'archived': game.archived,
                        'collection_id': game.collection_id,
                        'icon': game.icon,
                        'title_image': game.title_image,
                        'manual': game.manual,
                        'perspective': game.perspective,
                        'kid_game': game.kid_game,
                        'screenshot': game.screenshot,
                        'display': game.display,
                        'path': game.path,

                    },
                )
            except Exception as e:
                print("Update error for" + str(row))
                print(e)

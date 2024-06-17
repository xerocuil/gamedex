from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from games.models import Game

class Command(BaseCommand):
    help = 'Import game data from a csv file.'

    def handle(self, *args, **options):
        for row in DictReader(open('/opt/empr/docs/csv/import_display.csv')):
            game=Game(
                path=row['path'],
                display=row['display'],
            )
            try:
                obj, created = Game.objects.update_or_create(
                    path=game.path,
                    defaults={
                        'path': game.path,
                        'display': game.display,

                    },
                )
            except Exception as e:
                print("Update error for" + str(row))
                print(e)

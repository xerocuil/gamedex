import os
import subprocess
import extensions.config as config
import gamedex.settings as settings

APP_CFG = config.cfg['APP']
APP_DIR = config.APP_DIR


def check_for_dir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def check_installation():
    if not os.path.exists(APP_CFG['db']):
        print('Initializing configuration...')

        # Create application directories
        profile_dir = settings.PROFILE_DIR
        check_for_dir(profile_dir)

        media_dir = os.path.join(profile_dir, 'media')
        check_for_dir(media_dir)

        sys_dir = os.path.join(profile_dir, 'sys')
        check_for_dir(sys_dir)

        db_dir = os.path.join(sys_dir, 'db')
        check_for_dir(db_dir)

        # Migrate database/collect static files
        curr_dir = os.getcwd()
        os.chdir(APP_DIR)
        migrate_db('library')
        collect_static()
        os.chdir(curr_dir)


def collect_static():
    subprocess.run(['python', 'manage.py', 'collectstatic',  '--noinput'])


def migrate_db(app):
    curr_dir = os.getcwd()
    os.chdir(APP_DIR)
    subprocess.run(['python3', 'manage.py', 'makemigrations', app])
    subprocess.run(['python3', 'manage.py', 'migrate'])
    os.chdir(curr_dir)

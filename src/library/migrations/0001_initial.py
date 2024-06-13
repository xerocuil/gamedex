# Generated by Django 5.0.6 on 2024-05-31 04:28

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('core', models.CharField(max_length=200, null=True)),
                ('launcher', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_title', models.CharField(blank=True, max_length=200, null=True)),
                ('archived', models.BooleanField(default=False)),
                ('co_op', models.BooleanField(default=False)),
                ('controller_support', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, max_length=8192, null=True)),
                ('developer', models.CharField(blank=True, max_length=200, null=True)),
                ('esrb', models.CharField(blank=True, choices=[('E', 'Everyone'), ('E10', 'Everyone 10+'), ('T', 'Teen'), ('M', 'Mature'), ('AO', 'Adults Only')], max_length=3, null=True)),
                ('favorite', models.BooleanField(default=False)),
                ('filename', models.CharField(max_length=200, unique=True)),
                ('game_id', models.CharField(blank=True, max_length=200, null=True)),
                ('gpu', models.CharField(blank=True, max_length=200, null=True)),
                ('hdd', models.CharField(blank=True, max_length=64, null=True)),
                ('last_played', models.DateTimeField(blank=True, null=True)),
                ('mod', models.CharField(blank=True, max_length=64, null=True)),
                ('notes', models.TextField(blank=True, max_length=8192, null=True)),
                ('online_multiplayer', models.BooleanField(default=False)),
                ('operating_system', models.CharField(blank=True, max_length=64, null=True)),
                ('play_count', models.IntegerField(blank=True, default=0, null=True)),
                ('players', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Value entered failed the sanity check'), django.core.validators.MaxValueValidator(256, message='Value entered failed the sanity check')])),
                ('processor', models.CharField(blank=True, max_length=200, null=True)),
                ('product_id', models.CharField(blank=True, max_length=200, null=True)),
                ('publisher', models.CharField(blank=True, max_length=200, null=True)),
                ('ram', models.CharField(blank=True, max_length=64, null=True)),
                ('region', models.CharField(blank=True, choices=[('NA', 'North America'), ('EU', 'Europe'), ('JP', 'Japan'), ('WO', 'World')], default='NA', max_length=3, null=True)),
                ('save_path', models.CharField(blank=True, max_length=200, null=True)),
                ('store', models.CharField(blank=True, choices=[('BLIZZARD', 'Blizzard'), ('EA', 'Eletronic Arts'), ('EPIC', 'Epic Games Store'), ('GOG', 'GOG.com'), ('HUMBLE', 'Humble Bundle'), ('ITCH', 'itch.io'), ('MSOFT', 'Microsoft Store'), ('NINTENDO', 'Nintendo'), ('PSN', 'PlayStation Network'), ('STEAM', 'Steam'), ('OTHER', 'Other')], max_length=8, null=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('translation', models.BooleanField(default=False)),
                ('year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1940, message='Value entered failed the sanity check'), django.core.validators.MaxValueValidator(2999, message='Value entered failed the sanity check')])),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.collection')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.genre')),
                ('platform', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.platform')),
                ('tags', models.ManyToManyField(blank=True, to='library.tag')),
            ],
        ),
    ]
# Generated by Django 4.2.2 on 2023-06-27 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_gameid_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='number_of_players',
        ),
    ]

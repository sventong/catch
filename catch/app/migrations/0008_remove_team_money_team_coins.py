# Generated by Django 4.2.2 on 2023-07-03 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_transporttype_javascript_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='money',
        ),
        migrations.AddField(
            model_name='team',
            name='coins',
            field=models.IntegerField(default=500, null=True),
        ),
    ]

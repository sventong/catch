# Generated by Django 4.2.2 on 2023-07-20 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_timestamp_challengedonebyteam_timestamp_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengedonebyteam',
            name='open',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='challengedonebyteam',
            name='successful',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='challengedonebyteam',
            name='timestamp_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='challengedonebyteam',
            name='timestamp_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='role',
            field=models.CharField(choices=[('CHASER', 'Chaser'), ('RUNNER', 'Runner')], max_length=20, null=True),
        ),
    ]

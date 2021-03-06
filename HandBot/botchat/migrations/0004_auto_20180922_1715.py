# Generated by Django 2.1 on 2018-09-22 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botchat', '0003_auto_20180922_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal',
            name='location_published',
        ),
        migrations.RemoveField(
            model_name='document',
            name='description',
        ),
        migrations.AddField(
            model_name='animal',
            name='latitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='animal',
            name='longitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='latitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='longitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]

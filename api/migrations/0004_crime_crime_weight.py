# Generated by Django 2.2.1 on 2019-08-10 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190602_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='crime',
            name='crime_weight',
            field=models.FloatField(default=1),
        ),
    ]
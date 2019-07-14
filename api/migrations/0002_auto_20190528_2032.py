# Generated by Django 2.2.1 on 2019-05-28 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crime',
            name='location',
        ),
        migrations.AddField(
            model_name='crime',
            name='arrest',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='community_areas',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='distrct',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='domestic',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='location_description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='occured_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='crime',
            name='year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='crime',
            name='primary_type',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
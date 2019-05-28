# <project>/<app>/management/commands/seed.py
from api.models import Crime
from datetime import datetime
from django.core.management.base import BaseCommand
import random
import logging
import csv

logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete Crime instances")
    Crime.objects.all().delete()


def create_crime(attributes):
    """Creates all crimes object"""
    logger.info("Creating crime")

    crime = Crime(
        occured_at = attributes['occured_at'],
        primary_type = attributes['primary_type'],
        description = attributes['description'],
        location_description = attributes['location_description'],
        arrest = attributes['arrest'],
        domestic = attributes['domestic'],
        distrct = attributes['distrct'],
        community_areas = attributes['community_areas'],
        year = attributes['year'],
        latitude = attributes['latitude'],
        longitude = attributes['longitude'])
    crime.save()
    logger.info("{} crime created.".format(crime))
    return crime

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    with open('data\Chicago_Crimes_2005.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        for row in csv_reader:
            if first:
                first = False
            else:
                latitude = row[20]
                longitude = row[21]
                if latitude and longitude:
                    attributes = {
                        'occured_at': datetime.strptime(row[3], '%m/%d/%Y %H:%M:%S %p'),
                        'primary_type': row[6],
                        'description': row[7],
                        'location_description': row[8],
                        'arrest': bool(row[9]),
                        'domestic': bool(row[10]),
                        'distrct': int(row[12]),
                        'community_areas': int(row[14]),
                        'year': int(row[18]),
                        'latitude': float(latitude),
                        'longitude': float(longitude)
                    }
                    create_crime(attributes)               

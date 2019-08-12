# <project>/<app>/management/commands/seed.py
from api.models import Crime
from datetime import datetime
from django.core.management.base import BaseCommand
import random
import logging
import csv

logger = logging.getLogger(__name__)

CRIME_WEIGHT = {
    'THEFT': 2,
    'BATTERY': 10,
    'CRIMINAL DAMAGE': 2,
    'NARCOTICS': 10,
    'ASSAULT': 3,
    'OTHER OFFENSE': 1,
    'BURGLARY': 2,
    'MOTOR VEHICLE THEFT': 2,
    'DECEPTIVE PRACTICE': 2,
    'ROBBERY': 3,
    'CRIMINAL TRESPASS': 1,
    'WEAPONS VIOLATION': 3,
    'PROSTITUTION': 2,
    'PUBLIC PEACE VIOLATION': 2,
    'OFFENSE INVOLVING CHILDREN': 10,
    'CRIM SEXUAL ASSAULT': 20,
    'SEX OFFENSE': 3,
    'INTERFERENCE WITH PUBLIC OFFICER': 2,
    'GAMBLING': 1,
    'LIQUOR LAW VIOLATION': 1,
    'ARSON': 10,
    'HOMICIDE': 20,
    'KIDNAPPING': 20,
    'INTIMIDATION': 2,
    'STALKING': 2,
    'OBSCENITY': 2,
    'CONCEALED CARRY LICENSE VIOLATION': 3,
    'NON-CRIMINAL': 1,
    'PUBLIC INDECENCY': 2,
    'OTHER NARCOTIC VIOLATION': 10,
    'HUMAN TRAFFICKING': 20,
    'NON - CRIMINAL': 1,
    'RITUALISM': 1,
    'NON-CRIMINAL (SUBJECT SPECIFIED)': 1,
    'DOMESTIC VIOLENCE': 3
}

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

def get_crime_weigth(primary_type):
    crime_weight = 1
    if primary_type in CRIME_WEIGHT:
        crime_weight = CRIME_WEIGHT[primary_type]
    return crime_weight


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
        longitude = attributes['longitude'],
        crime_weight = get_crime_weigth(attributes['primary_type']))
    crime.save()
    logger.info("{} crime created.".format(crime))
    return crime

def isDigit(str):
    str.isdigit()

def validateDate(date_text):
    try:
        datetime.strptime(date_text, '%m/%d/%Y %H:%M:%S %p')
        return True
    except ValueError:
        return False

def run_seed(self, mode):
    """ Seed database based on mode
    :param mode: refresh / clear
    :return:
    """
    with open('data/Chicago_Crimes_2005_to_2007.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        cant = 0
        for row in csv_reader:
            cant = cant + 1
            if cant < 50000:
                if first:
                    first = False
                else:
                    latitude = row[20]
                    longitude = row[21]
                    if latitude and longitude:
                        attributes = {
                            'occured_at': datetime.strptime(row[3], '%m/%d/%Y %H:%M:%S %p') if validateDate(row[3]) else None,
                            'primary_type': row[6],
                            'description': row[7],
                            'location_description': row[8],
                            'arrest': bool(row[9]),
                            'domestic': bool(row[10]),
                            'distrct': int(row[12]) if isDigit(row[12]) else None,
                            'community_areas': int(row[14]) if isDigit(row[14]) else None,
                            'year': int(row[18]) if isDigit(row[18]) else None,
                            'latitude': float(latitude),
                            'longitude': float(longitude)
                        }
                        create_crime(attributes)

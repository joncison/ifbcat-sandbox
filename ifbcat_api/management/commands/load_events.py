import csv
import datetime
import logging
import os
import pandas as pd

import pytz
from django.core.management import BaseCommand
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model

from tqdm import tqdm

from ifbcat_api.model.event import *
from ifbcat_api.model.organisation import Organisation
from ifbcat_api.model.team import Team
from ifbcat_api.model.bioinformaticsTeam import BioinformaticsTeam

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--events",
            default="import_data/events.csv",
            type=str,
            help="Path to the CSV source file",
        )
        parser.add_argument(
            "--mapping-organisations",
            default="import_data/manual_curation/mapping_organisations.csv",
            type=str,
            help="Path to the CSV file containing mapping for organisations between Drupal names and Ifbcat ones.",
        )
        parser.add_argument(
            "--mapping-teams",
            default="import_data/manual_curation/mapping_teams.csv",
            type=str,
            help="Path to the CSV file containing mapping for teams between Drupal names and Ifbcat ones.",
        )

    def handle(self, *args, **options):
        mapping_organisations = pd.read_csv(options["mapping_organisations"], sep=",")
        mapping_teams = pd.read_csv(options["mapping_teams"], sep=",")

        with open(os.path.join(options["events"]), encoding='utf-8') as data_file:
            data = csv.reader(data_file)
            # skip first line as there is always a header
            next(data)
            # count number of lines
            data_len = len(list(data))
            data_file.seek(0)
            next(data)
            # do the work
            type_mapping_drupal_to_api = {
                'Formation': 'Training course',
                'Réunion': 'Meeting',
                'Atelier': 'Workshop',
                'Conférence': 'Conference',
                'Autre': 'Other',
                '': 'Other',
            }

            for data_object in tqdm(data, total=data_len):
                if data_object == []:
                    continue  # Check for empty lines
                event_name = data_object[0]
                event_type = type_mapping_drupal_to_api[data_object[1]]
                event_description = data_object[2]
                if data_object[3]:
                    if "to" in data_object[3]:
                        event_start_date = datetime.datetime.strptime(
                            data_object[3].split(" to ")[0], "%d-%m-%Y"
                        )  # .strftime("%Y-%m-%d")
                        event_start_date = make_aware(event_start_date, timezone=pytz.timezone('Europe/Paris'))
                        event_end_date = datetime.datetime.strptime(data_object[3].split(" to ")[1], "%d-%m-%Y")
                        event_end_date = make_aware(event_end_date, timezone=pytz.timezone('Europe/Paris'))
                    else:
                        event_start_date = datetime.datetime.strptime(
                            data_object[3], "%d-%m-%Y"
                        )  # .strftime("%Y-%m-%d")
                        event_start_date = make_aware(event_start_date, timezone=pytz.timezone('Europe/Paris'))
                        event_end_date = None
                else:
                    event_start_date = None
                    event_end_date = None

                event_location = data_object[4]
                event_link = data_object[5]
                event_organizer = data_object[6]
                event_sponsors = data_object[7]
                event_logo = data_object[8]

                print(get_user_model().objects.filter(is_superuser=True).first())

                try:
                    event, created = Event.objects.get_or_create(
                        name=event_name,
                        logo_url=event_logo,
                        type=event_type,
                        description=event_description,
                        # city is only a subset of event_location for the moment
                        city=event_location,
                        homepage=event_link,
                        accessibility='Public',
                    )

                    dates = EventDate.objects.create(dateStart=event_start_date, dateEnd=event_end_date)

                    event.dates.add(dates)

                    for organizer in event_organizer.split(','):
                        organizer = organizer.strip()
                        if organizer == '':
                            logger.debug(f'No organizer for {event_name}')
                        elif Organisation.objects.filter(name=organizer).exists():
                            organisation = Organisation.objects.get(name=organizer)
                            event.organisedByOrganisations.add(organisation)
                        elif organizer in mapping_organisations['drupal_name'].tolist():
                            organizer_row = mapping_organisations[mapping_organisations['drupal_name'] == organizer]
                            if not organizer_row['orgid'].isna().iloc[0]:
                                print(organizer_row['orgid'])
                                organisation = Organisation.objects.get(orgid=organizer_row['orgid'].iloc[0])
                            elif not organizer_row['ifbcat_name'].isna().iloc[0]:
                                print(organizer_row['orgid'])
                                organisation = Organisation.objects.get(name=organizer_row['ifbcat_name'].iloc[0])
                            event.organisedByOrganisations.add(organisation)

                        # elif BioinformaticsTeam.objects.filter(name=organizer).exists():
                        #    team = BioinformaticsTeam.objects.get(name=organizer)
                        #    event.organisedByBioinformaticsTeams.add(team)

                        elif Team.objects.filter(name=organizer).exists():
                            team = Team.objects.get(name=organizer)
                            event.organisedByTeams.add(team)
                        elif organizer in mapping_teams['drupal_name'].tolist():
                            organizer_row = mapping_teams[mapping_teams['drupal_name'] == organizer]
                            team = Team.objects.get(name=organizer_row['ifbcat_name'].iloc[0])
                            event.organisedByTeams.add(team)

                        else:
                            logger.error(f'{organizer} is not an organisation in the DB.')

                    # EventSponsors should be created before to be able to add them here to events
                    # for sponsor in event_sponsors.split(','):
                    #    sponsor=sponsor.strip()

                    #    if sponsor == '':
                    #        logger.debug(f'No sponsor for {sponsor}')

                    #    elif EventSponsor.objects.filter(name=sponsor).exists():
                    #        organisation=EventSponsor.objects.get(name=sponsor)
                    #        event.sponsoredBy.add(organisation)
                    #

                    # TODO: Fill required field using
                    # get_user_model().objects.filter(is_superuser=True).first()
                    # then uncomment validation below:
                    # event.full_clean()
                    event.save()

                except Exception as e:
                    logger.error(data_object)
                    raise e

import datetime
import os
import csv
from tqdm import tqdm

import pytz
from django.core.management import BaseCommand
from django.db.transaction import atomic
from django.utils.timezone import make_aware

from ifbcat_api.models import Tool
from ifbcat_api.models import ToolType
from ifbcat_api.models import Keyword
from ifbcat_api.models import Team


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Path to the CSV source file")

    @atomic
    def handle(self, *args, **options):
        with open(os.path.join(options["file"]), encoding='utf-8') as data_file:
            data = csv.reader(data_file)
            # skip first line as there is always a header
            next(data)
            # count number of lines
            data_len = len(list(data))
            data_file.seek(0)
            next(data)
            # do the work
            for data_object in tqdm(data, total=data_len):
                if data_object == []:
                    continue  # Check for empty lines
                database_name = data_object[0]
                database_logo = data_object[1]
                database_description = data_object[2]
                database_access_conditions = data_object[3]
                database_citations = data_object[4]
                database_citations = int(database_citations) if database_citations != '' else None
                database_link_data = data_object[5]
                database_keywords = [x.strip() for x in data_object[6].split(",")]
                database_keywords_list = []
                database_keyword = ""
                for keyword in database_keywords:
                    if len(keyword) > 2:

                        try:
                            print(keyword)

                            database_keyword, created = Keyword.objects.get_or_create(
                                keyword=keyword,
                            )
                            database_keyword.save()
                            database_keywords_list.append(database_keyword)
                            display_format = "\nKeyword, {}, has been saved."
                            # (display_format.format(database_keyword))
                        except Exception as ex:
                            print(str(ex))
                            msg = "\n\nSomething went wrong saving this keyword: {}\n{}".format(
                                database_keyword, str(ex)
                            )
                            print(msg)

                database_annual_visits = data_object[7].split(" ")[0]
                database_annual_visits = int(database_annual_visits) if database_annual_visits != '' else None
                database_unique_visits = data_object[8].split(" ")[0]
                database_unique_visits = int(database_unique_visits) if database_unique_visits != '' else None
                if data_object[9]:
                    database_last_update = datetime.datetime.strptime(
                        data_object[9], "%d-%m-%Y"
                    )  # .strftime("%Y-%m-%d")
                    database_last_update = make_aware(database_last_update, timezone=pytz.timezone('Europe/Paris'))
                else:
                    database_last_update = None
                database_increase_last_update = data_object[10]
                database_platform = data_object[11]

                database = ""

                try:
                    object_platform = Team.objects.get(
                        name=database_platform,
                    )
                except Team.DoesNotExist:
                    object_platform = None

                try:
                    print(database_link_data)
                    database, created = Tool.objects.update_or_create(
                        name=database_name,
                        defaults={
                            'logo': database_logo,
                            'description': database_description,
                            'access_condition': database_access_conditions,
                            'citations': database_citations,
                            'homepage': database_link_data,
                            'annual_visits': database_annual_visits,
                            'unique_visits': database_unique_visits,
                            'last_update': database_last_update,
                            # 'increase_last_update' is not in Tool model.
                            # Maybe we could create a Database model inheriting from Tool
                            # with this additionnal field?
                            #'increase_last_update': database_increase_last_update
                        },
                    )

                except Exception as e:
                    print(data_object)
                    raise e

                # if object_platform:
                #    database.platform.add(object_platform)

                display_format = "\nDatabase, {}, has been saved."
                # print(display_format.format(database))
                for keyword in database_keywords_list:
                    database.keywords.add(keyword)

                # biotoolsCURIE and biotoolsID are missing for validation
                # database.full_clean()
                database.save()

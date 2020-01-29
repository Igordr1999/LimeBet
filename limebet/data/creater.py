from .models import BookmakerTeamName, Team, Bookmaker, Country
import csv
from django.core.files.temp import NamedTemporaryFile
import shutil
import requests
import uuid


class Creater(object):
    def transliteration_to_latin(self, text):
        cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        latin = 'a|b|v|g|d|e|e|zh|z|i|i|k|l|m|n|o|p|r|s|t|u|f|kh|ts|ch|sh|shch|ie|y||e|iu|ia|A|B|V|G|D|E|E|Zh|Z|' \
                'I|I|K|L|M|N|O|P|R|S|T|U|F|Kh|Ts|Ch|Sh|Shch|Ie|Y||E|Iu|Ia'.split('|')
        return text.translate({ord(k): v for k, v in zip(cyrillic, latin)})

    def create_team(self, sport_id):
        with open('data/static_data/teams2.csv', encoding="cp1251") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = Country.objects.get(id=int(row['Страна']))
                for b_id in [1, 2, 3, 4, 5, 6, 7]:
                    if len(row[str(b_id)]) < 1:
                        continue
                    bookmaker_team_name, created = BookmakerTeamName.objects.get_or_create(team_name=row[str(b_id)],
                                                                                           bookmaker_id=b_id)

                    rus_name = row["4"]
                    translate_name = self.transliteration_to_latin(rus_name)
                    if len(row['Лого']) > 7:
                        logo_url = row['Лого']
                    else:
                        logo_url = "https://i-love-png.com/images/nologo_7311.png"
                    team, created = Team.objects.get_or_create(name_en=translate_name,
                                                               name_ru=rus_name,
                                                               sport_id=sport_id,
                                                               country=country,
                                                               logo_url=logo_url)

                    team.bookmaker_names.add(bookmaker_team_name)

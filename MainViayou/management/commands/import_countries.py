import requests
from bs4 import BeautifulSoup as bs
from MainViayou import models
from django.core.management.base import BaseCommand, CommandError


def get_cities():
    res = requests.get(
        'https://raw.githubusercontent.com/yosoyadri/GeoNames-XML-Builder/master/continents-countries-statesprovinces.xml')
    return bs(res.text, 'xml')


def parse_xml_cites(tree):
    continents = tree.SimpleGeoName.Children.find_all('SimpleGeoName', recursive=False)
    for continent in continents:
        for country in continent.Children.find_all('SimpleGeoName', recursive=False):
            c = models.Countries.objects.create(language_code='en', name=country.Name.string,
                                                code=country.CountryCode.string)
            c.set_current_language('es')
            c.name = country.LocalNameEs.string
            c.save()
            # for cities in country.Children.find_all('SimpleGeoName', recursive=False):
            #    yield country.Name.string, cities.Name.string


class Command(BaseCommand):
    help = "Import all countries with their cities"

    def handle(self, *args, **options):

        try:
            file = get_cities()
            parse_xml_cites(file)
        except Exception as e:
            raise CommandError('Something went wrong "%s"' % e)
        self.stdout.write(self.style.SUCCESS('Successfully countries import'))

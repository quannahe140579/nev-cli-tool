from django.test import TestCase
from .models import Region
from . import models


class TestModel(TestCase):
    def test_update_cli(self):
        location = Region()
        location.region_name = 'japaneast'
        rg_name = 'MyResourceGroup'
        create_cli_temp = 'az group create --location rg_location --name rg_name'

        district = {
            "rg_location": location.region_name,
            "rg_name": rg_name,
        }
        result = models.update_cli(create_cli_temp, district)
        expected = 'az group create --location japaneast --name MyResourceGroup'
        self.assertEqual(result, expected)

from django.test import TestCase
from api.helpers import md5_string
import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class MD5Test(TestCase):

    def setUp(self):
        self.google_earth_kml_file = "{TEST_DIR}/../data/google_earth_kml.xml".format(TEST_DIR=TEST_DIR)
        self.google_earth_kml = open(self.google_earth_kml_file, 'r')
        print(self.google_earth_kml)

    def test_md5(self):
        str1 = "Y023hAJK#@)(#<><>"
        str2 = "Y023hAJK#@)(#<><>"
        str3 = "Y023"
        self.assertEqual(md5_string(str1), md5_string(str2))
        self.assertNotEqual(md5_string(str1), md5_string(str3))

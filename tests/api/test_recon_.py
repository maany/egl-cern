from django.test import TestCase
from egl_rest.api.helpers import md5_string, get_country, get_geo_cords
from egl_rest.api.recon_chewbacca import ReconChewbacca
import os
from shutil import copyfile

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class MD5Test(TestCase):

    def setUp(self):
        self.google_earth_kml_file = "{TEST_DIR}/../data/google_earth_recon_test_kml.xml".format(TEST_DIR=TEST_DIR)
        self.cric_federations_file = "{TEST_DIR}/../data/cric_federations_recon_test_json.json".format(TEST_DIR=TEST_DIR)
        self.cric_sites_file = "{TEST_DIR}/../data/cric_sites_recon_test_json.json".format(TEST_DIR=TEST_DIR)
        self.ref_kml = "{TEST_DIR}/../data/google_earth_recon_test_kml_ref.xml".format(TEST_DIR=TEST_DIR)
        self.ref_cric_federations = "{TEST_DIR}/../data/cric_federations_recon_test_json_ref.json".format(TEST_DIR=TEST_DIR)
        self.ref_cric_sites = "{TEST_DIR}/../data/cric_sites_recon_test_json_ref.json".format(TEST_DIR=TEST_DIR)
        if os.path.isfile(self.google_earth_kml_file):
            os.remove(self.google_earth_kml_file)
        copyfile(self.ref_kml, self.google_earth_kml_file)

        self.recon_chewbacca = ReconChewbacca()
        self.recon_chewbacca.google_earth_kml = self.google_earth_kml_file
        self.recon_chewbacca.cric_federations_file = self.cric_federations_file
        self.recon_chewbacca.cric_sites_file = self.cric_sites_file

    def test_md5(self):
        str1 = "Y023hAJK#@)(#<><>"
        str2 = "Y023hAJK#@)(#<><>"
        str3 = "Y023"
        self.assertEqual(md5_string(str1), md5_string(str2))
        self.assertNotEqual(md5_string(str1), md5_string(str3))

    def test_get_country(self):
        country = get_country(41.947239, -87.655636)
        self.assertEquals(country.official_name, "United States of America")

    def test_get_gro_cords(self):
        geo_cords = get_geo_cords("CERN")
        latitude = geo_cords['latitude']
        longitude = geo_cords['longitude']
        self.assertEquals(latitude, 46.2338702)
        self.assertEquals(longitude, 6.04698691754795)

    def test_chewbacca_hunt_for_updates(self):
        output = self.recon_chewbacca.hunt_for_updates()
        kml_message = output['kml_message']
        cric_federations = output['cric_federations_message']
        cric_sites = output['cric_sites_message']
        self.assertIsNotNone(kml_message)
        self.assertIsNotNone(cric_federations)
        self.assertIsNotNone(cric_sites)

    def tearDown(self) -> None:
        super().tearDown()
        if os.path.isfile(self.cric_federations_file):
            copyfile(self.cric_federations_file, self.ref_cric_federations)
            os.remove(self.cric_federations_file)

        os.remove(self.google_earth_kml_file)

        if os.path.isfile(self.cric_sites_file):
            copyfile(self.cric_sites_file, self.ref_cric_sites)
            os.remove(self.cric_sites_file)



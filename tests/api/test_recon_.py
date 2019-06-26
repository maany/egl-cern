from django.test import TestCase
from egl_rest.api.helpers import md5_string
from egl_rest.api.recon_chewbacca import ReconChewbacca
import os
from shutil import copyfile

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class MD5Test(TestCase):

    def setUp(self):
        self.google_earth_kml_file = "{TEST_DIR}/../data/google_earth_recon_test_kml.xml".format(TEST_DIR=TEST_DIR)
        self.ref_kml = "{TEST_DIR}/../data/google_earth_recon_test_kml_ref.xml".format(TEST_DIR=TEST_DIR)
        if os.path.isfile(self.google_earth_kml_file):
            os.remove(self.google_earth_kml_file)
        copyfile(self.ref_kml, self.google_earth_kml_file)
        self.recon_chewbacca = ReconChewbacca()
        self.recon_chewbacca.google_earth_kml = self.google_earth_kml_file

    def test_md5(self):
        str1 = "Y023hAJK#@)(#<><>"
        str2 = "Y023hAJK#@)(#<><>"
        str3 = "Y023"
        self.assertEqual(md5_string(str1), md5_string(str2))
        self.assertNotEqual(md5_string(str1), md5_string(str3))

    def test_chewbacca_hunt_for_updates(self):
        kml_message = self.recon_chewbacca.hunt_for_updates()
        self.assertIsNotNone(kml_message)

    def tearDown(self) -> None:
        super().tearDown()
        os.remove(self.google_earth_kml_file)



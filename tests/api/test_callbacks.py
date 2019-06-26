from django.test import TestCase
from egl_rest.api.egl import EGL
from egl_rest.api.recon_chewbacca import ReconChewbacca
import os
from unittest.mock import patch
from egl_rest.api.services.cric_service import CRICService
from egl_rest.api.services.google_earth_service import GoogleEarthService

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestApiLoad(TestCase):

    def setUp(self):
        self.egl = EGL()
        self.recon_chewbacca = ReconChewbacca()
        self.recon_chewbacca.google_earth_kml = "{TEST_DIR}/../data/google_earth_api_load_test_kml.xml".format(TEST_DIR=TEST_DIR)
        self.recon_chewbacca.cric_federations_file = "{TEST_DIR}/../data/cric_federations_recon_test_json.json".format(TEST_DIR=TEST_DIR)
        self.recon_chewbacca.cric_sites_file = "{TEST_DIR}/../data/cric_sites_recon_test_json.json".format(TEST_DIR=TEST_DIR)
        if os.path.isfile(self.recon_chewbacca.google_earth_kml):
            os.remove(self.recon_chewbacca.google_earth_kml)

        if os.path.isfile(self.recon_chewbacca.cric_federations_file):
            os.remove(self.recon_chewbacca.cric_federations_file)

        if os.path.isfile(self.recon_chewbacca.cric_sites_file):
            os.remove(self.recon_chewbacca.cric_sites_file)


    @patch.object(GoogleEarthService, 'process_kml')
    @patch.object(CRICService, 'process_cric_sites')
    @patch.object(CRICService, 'process_cric_federations')
    def test_service_callbacks(self, cric_federations_callback, cric_sites_callback, google_earth_callback):
        self.recon_chewbacca.hunt_for_updates()
        google_earth_callback.assert_called_once()
        cric_sites_callback.assert_called_once()
        cric_federations_callback.assert_called_once()

    def tearDown(self) -> None:
        super().tearDown()
        os.remove(self.recon_chewbacca.google_earth_kml)
        os.remove(self.recon_chewbacca.cric_federations_file)
        os.remove(self.recon_chewbacca.cric_sites_file)


from django.test import TestCase
from egl_rest.api.egl import EGL_API
from egl_rest.api.recon_chewbacca import ReconChewbacca
import os
from unittest.mock import patch
from egl_rest.api.services.cric_service import CRICService
from egl_rest.api.services.rebus_service import RebusService

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestApiLoad(TestCase):
    pass
    # def setUp(self):
    #     self.egl = EGL_API()
    #     self.recon_chewbacca = ReconChewbacca()
    #     self.recon_chewbacca.google_earth_kml = "{TEST_DIR}/../data/google_earth_api_load_test_kml.xml".format(TEST_DIR=TEST_DIR)
    #     self.recon_chewbacca.cric_federations_file = "{TEST_DIR}/../data/cric_federations_recon_test_json.json".format(TEST_DIR=TEST_DIR)
    #     self.recon_chewbacca.cric_sites_file = "{TEST_DIR}/../data/cric_sites_recon_test_json.json".format(TEST_DIR=TEST_DIR)
    #     self.recon_chewbacca.rebus_sites_file = "{TEST_DIR}/../data/rebus_sites_recon_test_json.json".format(TEST_DIR=TEST_DIR)
    #     if os.path.isfile(self.recon_chewbacca.google_earth_kml):
    #         os.remove(self.recon_chewbacca.google_earth_kml)
    #
    #     if os.path.isfile(self.recon_chewbacca.cric_federations_file):
    #         os.remove(self.recon_chewbacca.cric_federations_file)
    #
    #     if os.path.isfile(self.recon_chewbacca.cric_sites_file):
    #         os.remove(self.recon_chewbacca.cric_sites_file)
    #
    #     if os.path.isfile(self.recon_chewbacca.rebus_sites_file):
    #         os.remove(self.recon_chewbacca.rebus_sites_file)
    #
    # @patch.object(CRICService, 'process_cric_sites')
    # @patch.object(CRICService, 'process_cric_federations')
    # @patch.object(RebusService, 'process_rebus_sites')
    # def test_service_callbacks_are_called(self, rebus_callback, cric_federations_callback, cric_sites_callback):
    #     self.recon_chewbacca.hunt_for_updates()
    #     cric_sites_callback.assert_called_once()
    #     cric_federations_callback.assert_called_once()
    #     rebus_callback.assert_called_once()
    #
    # def tearDown(self) -> None:
    #     super().tearDown()
    #     os.remove(self.recon_chewbacca.google_earth_kml)
    #     os.remove(self.recon_chewbacca.cric_federations_file)
    #     os.remove(self.recon_chewbacca.cric_sites_file)
    #     os.remove(self.recon_chewbacca.rebus_sites_file)


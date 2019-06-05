from django.test import TestCase
from api.egl import EGL
from api.recon_chewbacca import ReconChewbacca
import os
from unittest.mock import MagicMock
from unittest.mock import patch

from api.services.google_earth_service import GoogleEarthService

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

class TestApiLoad(TestCase):

    def setUp(self):
        self.egl = EGL()
        self.recon_chewbacca = ReconChewbacca()
        self.recon_chewbacca.google_earth_kml = "{TEST_DIR}/../data/google_earth_api_load_test_kml.xml".format(TEST_DIR=TEST_DIR)
        if os.path.isfile(self.recon_chewbacca.google_earth_kml):
            os.remove(self.recon_chewbacca.google_earth_kml)
        #self.mock_google_earth_service = GoogleEarthService()
        #self.mock_google_earth_service.notify = MagicMock(return_value=True)

    def test_api_load(self):
        kml_message = self.recon_chewbacca.hunt_for_updates()
        print(kml_message)
        #self.mock_google_earth_service.notify.assert_called()

    def tearDown(self) -> None:
        super().tearDown()



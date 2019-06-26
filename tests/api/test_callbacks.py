from django.test import TestCase
from egl_rest.api.egl import EGL
from egl_rest.api.recon_chewbacca import ReconChewbacca
import os
from unittest.mock import patch

from egl_rest.api.services.google_earth_service import GoogleEarthService

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestApiLoad(TestCase):

    def setUp(self):
        self.egl = EGL()
        self.recon_chewbacca = ReconChewbacca()
        self.recon_chewbacca.google_earth_kml = "{TEST_DIR}/../data/google_earth_api_load_test_kml.xml".format(TEST_DIR=TEST_DIR)
        if os.path.isfile(self.recon_chewbacca.google_earth_kml):
            os.remove(self.recon_chewbacca.google_earth_kml)

    @patch.object(GoogleEarthService, 'notify')
    def test_google_earth_service_callback(self, google_earth_callback):
        kml_message = self.recon_chewbacca.hunt_for_updates()
        print(kml_message)
        google_earth_callback.assert_called_once()

    def tearDown(self) -> None:
        super().tearDown()
        os.remove(self.recon_chewbacca.google_earth_kml)


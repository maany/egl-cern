import os
from shutil import copyfile

from django.test import TestCase

from egl_rest.api.recon_chewbacca import ReconChewbacca
from egl_rest.api.services.alice_service import AliceService
from egl_rest.api.services.atlas_service import AtlasService
from egl_rest.api.egl import EGL_API
from egl_rest.api.services.cms_service import CMSService

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestGridStatisticsServices(TestCase):

    def setUp(self):
        self.egl = EGL_API()
        self.atlas_service = AtlasService()

        self.google_earth_kml_file = "{TEST_DIR}/../data/google_earth_recon_test_kml.xml".format(TEST_DIR=TEST_DIR)
        self.cric_federations_file = "{TEST_DIR}/../data/cric_federations_recon_test_json.json".format(
            TEST_DIR=TEST_DIR)
        self.cric_sites_file = "{TEST_DIR}/../data/cric_sites_recon_test_json.json".format(TEST_DIR=TEST_DIR)
        self.rebus_sites_file = "{TEST_DIR}/../data/rebus_sites_recon_test_json.json".format(TEST_DIR=TEST_DIR)
        self.ref_kml = "{TEST_DIR}/../data/google_earth_recon_test_kml_ref.xml".format(TEST_DIR=TEST_DIR)
        self.ref_cric_federations = "{TEST_DIR}/../data/cric_federations_recon_test_json_ref.json".format(
            TEST_DIR=TEST_DIR)
        self.ref_cric_sites = "{TEST_DIR}/../data/cric_sites_recon_test_json_ref.json".format(TEST_DIR=TEST_DIR)
        self.ref_rebus_sites = "{TEST_DIR}/../data/rebus_sites_recon_test_json_ref.json".format(TEST_DIR=TEST_DIR)
        if os.path.isfile(self.google_earth_kml_file):
            os.remove(self.google_earth_kml_file)
        copyfile(self.ref_kml, self.google_earth_kml_file)

        if os.path.isfile(self.rebus_sites_file):
            os.remove(self.rebus_sites_file)
        copyfile(self.ref_rebus_sites, self.rebus_sites_file)

        self.recon_chewbacca = ReconChewbacca()
        self.recon_chewbacca.google_earth_kml = self.google_earth_kml_file
        self.recon_chewbacca.cric_federations_file = self.cric_federations_file
        self.recon_chewbacca.cric_sites_file = self.cric_sites_file
        self.recon_chewbacca.rebus_sites_file = self.rebus_sites_file
        self.egl.recon_chewbacca = self.recon_chewbacca
        try:
            self.recon_chewbacca.hunt_for_updates()
        except Exception as e:
            print(e)

    # def test_atlas_collect_global_running_job_stats(self):
    #
    #     global_job_stats = AtlasService.fetch_all_stats(time_interval_start="2019-09-10 00:00",
    #                                                     time_interval_end="2019-09-11 00:00")
    #     print(global_job_stats)
    #
    # def test_cms_collect_global_running_job_stats_cms(self):
    #     cms_global_job_stats = CMSService.fetch_all_stats(time_interval_start="2019-09-10 00:00",
    #                                                     time_interval_end="2019-09-11 00:00")
    #     print(cms_global_job_stats)

    def test_alice_download_files(self):
        stats = AliceService.download_alice_files("{TEST_DIR}/../data".format(TEST_DIR=TEST_DIR))
        AliceService.collect_running_job_stats(time_interval_start="2019-09-10 00:00",
                                                         time_interval_end="2019-09-11 00:00",
                                                         data_dir="{TEST_DIR}/../data".format(TEST_DIR=TEST_DIR))
    def tearDown(self) -> None:
        super().tearDown()
        if os.path.isfile(self.cric_federations_file):
            copyfile(self.cric_federations_file, self.ref_cric_federations)
            os.remove(self.cric_federations_file)

        os.remove(self.google_earth_kml_file)
        os.remove(self.rebus_sites_file)
        if os.path.isfile(self.cric_sites_file):
            copyfile(self.cric_sites_file, self.ref_cric_sites)
            os.remove(self.cric_sites_file)

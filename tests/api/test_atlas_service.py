from django.test import TestCase

from egl_rest.api.services.atlas_service import AtlasService
from egl_rest.api.helpers import datetime_timestamp

class TestAtlasService(TestCase):

    def setUp(self):
        self.atlas_service = AtlasService()
        pass

    def test_collect_global_running_job_stats(self):
        global_job_stats = AtlasService.fetch_all_stats(time_interval_start="2019-09-10 00:00",
                                                        time_interval_end="2019-09-11 00:00")
        print(global_job_stats)

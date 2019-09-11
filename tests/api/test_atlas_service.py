from django.test import TestCase

from egl_rest.api.services.atlas_service import AtlasService


class TestAtlasService(TestCase):

    def setUp(self):
        self.atlas_service = AtlasService()
        pass

    def test_collect_global_running_job_stats(self):
        global_job_stats = AtlasService.collect_global_running_job_stats()
        print(global_job_stats)

from egl_rest.models import Pledge, Site, Federation,  VO
from egl_rest.api.services.federations_service import FederationsService
from egl_rest.api.services.site_service import SiteService
from egl_rest.api.services.pledge_service import PledgeService
from egl_rest.api.services.vo_service import VOService

from django.test import TestCase


class TestServiceModels(TestCase):

    def setUp(self):
        self.federation = FederationsService.get_or_create("TestFed")
        VOService.get_or_create("alice")
        VOService.get_or_create("alice")
        VOService.get_or_create("atlas")

    def test_get_federation_by_name(self):
        federation = FederationsService.get("TestFed")
        alice_vo = VOService.get("alice")
        pledge = PledgeService.get_or_create(federation, alice_vo)
        federation.pledge_set.add(pledge)
        FederationsService.save(federation)
        self.assertIsNotNone(federation)

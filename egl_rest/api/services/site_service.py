from egl_rest.api.event_hub import EventHub
from egl_rest.api.event_hub.event_managers import IEGLEventListener
from egl_rest.api.event_hub.events.data_fetch_parse_events import OfflineParsingAllSitesCompletionEvent
from egl_rest.api.helpers import Singleton
from egl_rest.api.models import Site
from egl_rest.api.services.federations_service import FederationsService


class SiteService(Singleton, IEGLEventListener):

    def __init__(self):
        Singleton.__init__(self)
        EventHub.register_listener(self, OfflineParsingAllSitesCompletionEvent)

    @staticmethod
    def get_or_create(site_name):
        return Site.objects.get_or_create(
            name=site_name,
        )[0]

    @staticmethod
    def get(site_name):
        return Site.objects.get(
            name=site_name
        )

    @staticmethod
    def save(site):
        return site.save()

    @staticmethod
    def get_all():
        return Site.objects.all()

    @staticmethod
    def get_by_name(name):
        return Site.objects.get(name=name)

    @staticmethod
    def get_active_sites():
        return Site.objects.filter(active=True)

    @staticmethod
    def get_inactive_sites():
        return Site.objects.filter(active=False)

    @staticmethod
    def deactivate(site):
        site.active = False

    @staticmethod
    def activate(site):
        if site.latitude is not 0 \
            and site.longitude is not 0 \
            and site.tier is not -1 \
            and site.country is not None \
                and len(site.supported_vos.all())is not 0:
                    site.active = True
                    site.save()
                    return True
        else:
            return False

    @staticmethod
    def get_by_federation(federation_name):
        return FederationsService.get_sites(FederationsService.get(federation_name))

    @staticmethod
    def get_by_country(country_code):
        return Site.objects.filter(
            country_code=country_code
        )

    @staticmethod
    def analyse():
        # tier_neg1_sites = Site.objects.get(tier=-1)
        tier0_sites = Site.objects.filter(tier=0)
        tier1_sites = Site.objects.filter(tier=1)
        tier2_sites = Site.objects.filter(tier=2)
        tier3_sites = Site.objects.filter(tier=3)
        # print(tier_neg1_sites)
        print(tier0_sites)
        print(tier1_sites)
        print(tier2_sites)
        print(tier3_sites)

    @staticmethod
    def post_process():
        print("Ready to Post Process!!")
        sites = SiteService.get_all()
        for site in sites:
            if site.federation is None:
                site.tier = 3
            SiteService.activate(site)
            SiteService.save(site)
        SiteService.analyse()


    def notify(self, egl_event):
        from egl_rest.api.services.cric_service import CRICService
        if egl_event.created_by is CRICService.__name__:
            SiteService.post_process()

from egl_rest.api.helpers import Singleton
from egl_rest.api.models import Site
from egl_rest.api.services.federations_service import FederationsService


class SiteService(Singleton):

    @staticmethod
    def get_or_create(site_name):
        return Site.objects.get_or_create(
            name=site_name
        )

    @staticmethod
    def get(site_name):
        return Site.objects.get(
            name=site_name
        )

    @staticmethod
    def save(site):
        return site.save()

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
    def analyse(self, google_earth_sites, cric_sites):
        pass

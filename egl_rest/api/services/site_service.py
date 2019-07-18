from egl_rest.api.helpers import Singleton
from egl_rest.api.models import Site
from egl_rest.api.services.federations_service import FederationsService
from egl_rest.api.render.site_data import SiteData
import json


class SiteService(Singleton):

    def __init__(self):
        Singleton.__init__(self)

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
    def get_by_id(id):
        return Site.objects.filter(id=id)

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
            and site.country_code is not "" \
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
    def generate_site_data(sites, version):
        if version not in SiteData.supported_schemas:
            return "Schema version {version} is not supported. Try one of {supported_schemas}".format(
                version=version,
                supported_schemas=SiteData.supported_schemas
            )
        output = {'sites': {}, 'meta': [], 'current_schema_version': version,
                  'latest_schema_version': SiteData.get_latest_schema()}
        for site in sites:
            output['sites'][site.name] = SiteData.render(site, version)
        output['meta'] = SiteService.analyse(sites)
        return json.dumps(output)

    @staticmethod
    def analyse(sites):
        tier0_sites = sites.filter(tier=0)
        tier1_sites = sites.filter(tier=1)
        tier2_sites = sites.filter(tier=2)
        tier3_sites = sites.filter(tier=3)
        atlantic_sites = sites.filter(latitude=0.0, active=True)
        storage_info_available_sites = sites.exclude(total_online_storage__in=[0, -1])
        return{
            "total_sites": len(sites),
            "active_sites": len(sites.filter(active=True)),
            "tier_0": len(tier0_sites),
            "tier_1": len(tier1_sites),
            "tier_2": len(tier2_sites),
            "tier_3": len(tier3_sites),
            "atlantic_sites": len(atlantic_sites),
            "storage_info_available": len(storage_info_available_sites)
        }

    @staticmethod
    def post_process():
        sites = SiteService.get_all()
        for site in sites:
            if site.federation is None:
                site.tier = 3
            SiteService.activate(site)
            SiteService.save(site)

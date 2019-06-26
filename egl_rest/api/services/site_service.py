from egl_rest.api import Singleton
from egl_rest.api import Site


class SiteService(Singleton):
    sites = []

    def create(self, name, latitude, longitude, federation, country, tier, supported_vos, capacity) -> Site:
        pass

    def get_by_name(self, name) -> Site:
        pass

    def get_by_federation(self, federation_name) -> [Site]:
        pass

    def get_by_country(self, country_code):
        pass

    def analyse(self, google_earth_sites, cric_sites):
        pass
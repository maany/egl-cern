from api.helpers import Singleton
from api.models import Site


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

    def analyse(self):
        pass
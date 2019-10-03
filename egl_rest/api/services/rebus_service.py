from egl_rest.api.helpers import Singleton
import json
import logging
from egl_rest.api.services.site_service import SiteService

logger = logging.getLogger(__name__)


class RebusService(Singleton):
    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def process_rebus_sites(rebus_sites_file):
        with open(rebus_sites_file, 'r') as file:
            sites = json.load(file)
            for site in sites:
                site_name = site["Site"]
                try:
                    site_obj = SiteService.get(site_name)
                except:
                    logger.error("{site_name} not found in database. Cannot update storage info from REBUS".format(site_name=site_name))
                    continue
                site_obj.total_online_storage = site['TotalNearlineSize']
                site_obj.total_online_storage = site['TotalOnlineSize']
                if site_name == "T2_Estonia":
                    return
                SiteService.save(site_obj)


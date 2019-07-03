from egl_rest.api.helpers import Singleton
from egl_rest.api.models import SiteVO

class SiteVOService(Singleton):
    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def get_or_create(site_vo_name, site, vo):
        return SiteVO.objects.get_or_create(
            name=site_vo_name,
            site=site,
            vo=vo
        )[0]

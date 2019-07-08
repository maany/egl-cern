from egl_rest.api.helpers import Singleton
from egl_rest.api.models import Site
import json


class SiteData(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def generate_v1_0():
        sites = Site.objects.filter(active=True)
        sites_dict = {}
        for site in sites:
            site_vo_set = site.sitevo_set.all()
            site_vo_array = []
            for site_vo_obj in site_vo_set:
                site_vo_array.append({
                    "site": site_vo_obj.site.name,
                    "vo": site_vo_obj.vo.name
                })
            if site.federation is None:
                federation = "None"
            else:
                federation = site.federation.name

            if site.total_nearline_storage is -1:
                total_nearline_storage = "Not Available"
            elif site.total_nearline_storage is 0:
                total_nearline_storage = "Not Specified"
            else:
                total_nearline_storage = site.total_nearline_storage

            if site.total_online_storage is -1:
                total_online_storage = "Not Available"
            elif site.total_online_storage is 0:
                total_online_storage = "Not Specified"
            else:
                total_online_storage = site.total_online_storage

            if site.cores is 0:
                cores = "Not Specified"
            else:
                cores = site.cores

            if site.hepspec06 is 0:
                hepspec06 = "Not Specified"
            else:
                hepspec06 = site.hepspec06

            sites_dict[site.name] = {
                "latitude": site.latitude,
                "longitude": site.longitude,
                "tier": site.tier,
                "supported_vos": site_vo_array,
                "country": site.country,
                "country_code": site.country_code,
                "hepspec06": hepspec06,
                "cores": cores,
                "total_online_storage": total_online_storage,
                "total_nearline_storage": total_nearline_storage,
                "federation": federation
            }

        json_rep = json.dumps(sites_dict)
        return json_rep


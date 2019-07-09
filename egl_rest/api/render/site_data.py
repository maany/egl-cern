from egl_rest.api.helpers import Singleton


class SiteData(Singleton):
    supported_schemas = [1.0]

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def render(site, version):
        if version == 1.0:
            return SiteData.generate_v1_0(site)
        else:
            raise Exception("Schema version {version} not supported for sites.".format(version=version))

    @staticmethod
    def get_latest_schema():
        SiteData.supported_schemas.sort()
        return SiteData.supported_schemas[-1]

    @staticmethod
    def generate_v1_0(site):
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

        site_dict = {
            "id": site.id,
            "name": site.name,
            "latitude": site.latitude,
            "longitude": site.longitude,
            "tier": site.tier,
            "supported_vos_and_site_name": site_vo_array,
            "country": site.country,
            "country_code": site.country_code,
            "hepspec06": hepspec06,
            "cores": cores,
            "total_online_storage": total_online_storage,
            "total_nearline_storage": total_nearline_storage,
            "federation": federation
        }
        return site_dict


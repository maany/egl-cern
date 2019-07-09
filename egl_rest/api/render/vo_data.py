from egl_rest.api.helpers import Singleton


class VOData(Singleton):
    supported_schemas = [1.0]

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def render(vo, version):
        if version == 1.0:
            return VOData.generate_v1_0(vo)
        else:
            raise Exception("Schema version {version} not supported for VOs.".format(version=version))

    @staticmethod
    def get_latest_schema():
        VOData.supported_schemas.sort()
        return  VOData.supported_schemas[-1]

    @staticmethod
    def generate_v1_0(vo):
        sites = []
        federations = []
        for site in vo.sitevo_set.all():
            sites.append(site.name)
        for federation in vo.federation_set.all():
            federations.append(federation.name)
        vo_dict = {
            "name": vo.name,
            "sites": sites,
            "federations": federations
        }
        return vo_dict

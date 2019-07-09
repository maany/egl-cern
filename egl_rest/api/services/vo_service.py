import json

from egl_rest.api.helpers import Singleton
from egl_rest.api.models import VO, Federation, Site
from egl_rest.api.render.vo_data import VOData
import json


class VOService(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def get_or_create(name):
        return VO.objects.get_or_create(
            name=name
        )[0]

    @staticmethod
    def get(name):
        return VO.objects.get(name=name)

    @staticmethod
    def get_all():
        return VO.objects.all()

    @staticmethod
    def generate_vo_data(vos, version):
        if version not in VOData.supported_schemas:
            return "Schema version {version} is not supported. Try one of {supported_schemas}".format(
                version=version,
                supported_schemas=VOData.supported_schemas
            )
        output = {'vos': {}, 'meta': [], 'current_schema_version': version,
                  'latest_schema_version': VOData.get_latest_schema()}
        for vo in vos:
            output['vos'][vo.name] = VOData.render(vo, version)
        output['meta'] = VOService.analyse(vos)
        return json.dumps(output)

    @staticmethod
    def analyse(vos):
        return {
            'vos': len(vos)
        }

    @staticmethod
    def get_federations(vo):
        return vo.federation_set.all()

    @staticmethod
    def get_sites(vo):
        return Site.objects.filter(supported_vos__in=[vo])

    @staticmethod
    def save(vo):
        return vo.save()

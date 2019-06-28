from egl_rest.api.helpers import Singleton
from egl_rest.api.models import VO, Federation, Site


class VOService(Singleton):

    @staticmethod
    def get_or_create(name):
        return VO.objects.get_or_create(
            name=name
        )[0]

    @staticmethod
    def get(name):
        return VO.objects.get(name=name)

    @staticmethod
    def get_federations(vo):
        return vo.federation_set.all()

    @staticmethod
    def get_sites(vo):
        return Site.objects.filter(supported_vos__in=[vo])

    @staticmethod
    def save(vo):
        return vo.save()

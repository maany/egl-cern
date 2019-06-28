from egl_rest.api.helpers import Singleton
from egl_rest.api.models import Federation


class FederationsService(Singleton):

    @staticmethod
    def get_or_create(federation_name):
        return Federation.objects.get_or_create(
            name=federation_name
        )[0]

    @staticmethod
    def get(federation_name):
        return Federation.objects.get(name=federation_name)

    @staticmethod
    def save(federation):
        return federation.save()

    @staticmethod
    def get_sites(federation):
        return federation.site_set.all()


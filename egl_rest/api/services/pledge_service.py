from egl_rest.api.helpers import Singleton
from egl_rest.api.models import Pledge


class PledgeService(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def get_or_create(federation, vo):
        return Pledge.objects.get_or_create(
            federation=federation,
            vo=vo
        )[0]

    @staticmethod
    def save(pledge):
        return pledge.save()

    @staticmethod
    def update(pledge):
        return pledge.update()

    @staticmethod
    def get_by_federation(federation):
        return Pledge.objects.get(federation=federation)


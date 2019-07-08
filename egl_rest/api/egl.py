from egl_rest.api.event_hub import EventHub
from egl_rest.api.recon_chewbacca import ReconChewbacca
from egl_rest.api.services.sequence_service import SequenceService
from egl_rest.api.services.cric_service import CRICService
from egl_rest.api.services.google_earth_service import GoogleEarthService
from egl_rest.api.services.rebus_service import RebusService
from egl_rest.api.services.site_service import SiteService
from egl_rest.api.helpers import Singleton
### Service loading and Event Hub loading ###


class EGL_API(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.event_hub = EventHub()
        self.google_earth_service = GoogleEarthService()
        self.cric_service = CRICService()
        self.site_service = SiteService()
        self.rebus_service = RebusService()
        self.sequence_service = SequenceService()
        self.recon_chewbacca = ReconChewbacca()

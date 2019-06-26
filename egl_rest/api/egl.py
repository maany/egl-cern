from egl_rest.api.event_hub import EventHub
from egl_rest.api.services.cric_service import CRICService
from egl_rest.api.services.google_earth_service import GoogleEarthService
from egl_rest.api.helpers import Singleton

### Service loading and Event Hub loading ###
class EGL(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.event_hub = EventHub()
        self.google_earth_service = GoogleEarthService()
        self.cric_service = CRICService()

from api.event_hub.event_managers import IEGLEventListener
from api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent
from api.event_hub import EventHub
from api.helpers import Singleton
from api.recon_chewbacca import ReconChewbacca
from xml.etree import ElementTree as ET
from api.models import Site

class GoogleEarthService(Singleton, IEGLEventListener):

    def __init__(self):
        Singleton.__init__(self)
        EventHub.register_listener(self, NewDataAvailableOnlineEvent)

    def process_kml(self, google_earth_file):
        print("Processing KML")
        root = ET.parse(google_earth_file).getroot()
        document = root.find('Document')
        folders = document.findall('Folder')
        sites = None
        for folder in folders:
            if folder.find('name').text == "Sites":
                sites = folder.findall('Placemark')
        for site in sites:
            print(site.find('name').text)


    def notify(self, egl_event):
        if egl_event.created_by is ReconChewbacca.__name__ and egl_event.data['source'] is "google_earth":
            self.process_kml(egl_event.data['data'])

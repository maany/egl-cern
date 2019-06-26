from egl_rest.api import IEGLEventListener
from egl_rest.api import NewDataAvailableOnlineEvent
from egl_rest.api import EventHub
from egl_rest.api import Singleton
from egl_rest.api import ReconChewbacca
from xml.etree import ElementTree as ET


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

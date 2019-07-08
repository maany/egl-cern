from egl_rest.api.helpers import Singleton
from xml.etree import ElementTree as ET


class GoogleEarthService(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def process_kml(google_earth_file):
        print("Processing KML")
        root = ET.parse(google_earth_file).getroot()
        document = root.find('Document')
        folders = document.findall('Folder')
        sites = None
        for folder in folders:
            if folder.find('name').text == "Sites":
                sites = folder.findall('Placemark')
        for site in sites:
            pass#print(site.find('name').text)

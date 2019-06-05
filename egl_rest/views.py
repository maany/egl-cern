from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import xml.etree.ElementTree as ET

cms_cric_url = "https://cms-cric.cern.ch/api/core/rcsite/query/?json"
wlcg_cric_url = "https://wlcg-cric.cern.ch/api/core/rcsite/query/?json"

# Create your views here.
def sites(request):
    output = requests.get(cms_cric_url, verify = False)
    #data = json.loads(output.text)
    #print(data)
    return HttpResponse(output.text)

def data_links(request):
    #kml_url = "http://dashb-earth.cern.ch/dashboard/dashb-earth-all.kml"
    #output = requests.get(kml_url)
    #with open("google_earth_recon_test_kml.xml", "w") as file:
    #    file.write(output.text)

    parsed = ET.parse('google_earth_recon_test_kml.xml')
    root = parsed.getroot()
    document = root.find('Document')
    folders = document.findall('Folder')
    placemarks = []
    all_links = []
    for folder in folders:
        print(folder.find('name').text)
        if folder.find('name').text == "Data Links":
            placemarks = folder.findall('Placemark')

    for placemark in placemarks:
        styleUrl = placemark.find('styleUrl').text
        link = {}
        if styleUrl == "#dataLinkOk":
            link['status'] = True
        else:
            link['status'] = False
        link['altitudeMode'] = placemark.find('./LineString/altitudeMode').text
        coordinates = placemark.find('./LineString/coordinates').text.split(' ')
        begin_coordinates = coordinates[0].split(',')
        end_coordinates = coordinates[-2].split(',')
        link['begin'] = {}
        link['end'] = {}
        link['begin']['longitude'] = float(begin_coordinates[0])
        link['begin']['latitude'] = float(begin_coordinates[1])
        link['begin']['altitude'] = float(begin_coordinates[2])
        link['end']['longitude'] = float(end_coordinates[0])
        link['end']['latitude'] = float(end_coordinates[1])
        link['end']['altitude'] = float(end_coordinates[2])
        all_links.append(link)

    return HttpResponse(json.dumps(all_links))

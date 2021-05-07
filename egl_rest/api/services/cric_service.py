from egl_rest.api.helpers import Singleton
import json
from egl_rest.api.services.federations_service import FederationsService
from egl_rest.api.services.pledge_service import PledgeService
from egl_rest.api.services.site_service import SiteService
from egl_rest.api.services.vo_service import VOService
from egl_rest.api.services.site_vo_service import SiteVOService
from egl_rest.api.helpers import get_country, get_geo_coords
from unittest.mock import patch

class CRICService(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def process_cric_sites(cric_sites_file):
        with open(cric_sites_file) as file:
            sites = json.load(file)
            for site_name, site in sites.items():
                if site_name == "NULL":
                    continue
                # print(site_name)
                site = CRICService.cric_sites_location_patch(site_name, site)
                site_obj = SiteService.get_or_create(site_name)
                site_obj.sources.append('cric_sites')
                site_obj.latitude = site['latitude']
                site_obj.longitude = site['longitude']
                site_obj.hepspec06 = site['cpu_capacity']
                site_obj.cores = site['cores']
                for site_vo in site['sites']:
                    vo_obj = VOService.get_or_create(site_vo['vo_name'])
                    site_vo_obj = SiteVOService.get_or_create(site_vo['name'], site_obj, vo_obj)

                    site_obj.supported_vos.add(vo_obj)
                    site_obj.sitevo_set.add(site_vo_obj)

                    vo_obj.sitevo_set.add(site_vo_obj)
                    vo_obj.site_set.add(site_obj)
                if site['country'] == "NULL":
                    if "KISTI" in site_name:
                        site_obj.country = "South Korea"
                    else:
                        site_obj.country = get_country(site['latitude'], site['longitude']).name
                else:
                    site_obj.country = site['country']
                if site['country_code'] is not None or len(site['country_code']) > 0:
                    site_obj.country_code = site['country_code']
                else:
                    if "KISTI" in site_name:
                        site_obj.country_code = "KR"
                    else:
                        site_obj.country = get_country(site['latitude'], site['longitude']).alpha_2
                SiteService.save(site_obj)


    def get_geo_coords(self):
        return {"latitude": 10.0, "longitude": 10.0}


    @staticmethod
    @patch('egl_rest.api.helpers.get_geo_coords', side_effect=get_geo_coords, autospec=True)
    def cric_sites_location_patch(site_name, site, get_geo_coords=None):
        if site["latitude"]!= 0.0 and site['longitude'] != 0.0:
            return site
        if "CERN" in site_name:
            geo_cords = get_geo_coords("CERN")
        if "WIGNER" in site_name:
            geo_cords = get_geo_coords("Wigner Datacenter")
        elif "CIEMAT-TIC" in site_name:
            geo_cords = get_geo_coords("CIEMAT")
        elif "FZU" in site_name:
            geo_cords = {
                "latitude": 50.123489,
                "longitude": 14.469153
            }
        elif site_name == "GR-05-DEMOKRITOS":
            geo_cords = {
                "latitude": 37.999229,
                "longitude": 23.819099
            }
        elif site_name == "GROW-PROD":
            geo_cords = get_geo_coords("University of Iowa")
        elif site_name == "IN2P3-LPSC":
            geo_cords = get_geo_coords(" Centre de calcul IN2P3")
        elif site_name == "INFN-FIRENZE":
            geo_cords = get_geo_coords("INFN florence")
        elif site_name == "NYSGRID-CCR-U2":
            geo_cords = get_geo_coords("University at Buffalo")
        elif site_name == "NYSGRID_CORNELL_NYS1":
            geo_cords = get_geo_coords("Cornell University")
        elif site_name == "ORNL-T2":
            geo_cords = get_geo_coords("oak ridge national laboratory")
        elif site_name == "Oslo":
            geo_cords = get_geo_coords("University of Oslo")
        elif site_name == "UB-LCG2":
            geo_cords = get_geo_coords("University of Barcelona")
        elif "USTC" in site_name:
            geo_cords = get_geo_coords("USTC China")
        elif site_name == "ru-Moscow-SINP-LCG2":
            geo_cords = get_geo_coords("Moscow State University")
        elif site_name == "ucsb-cms":
            geo_cords = get_geo_coords("University of California Santa Barbara")
        elif site_name == "FSU-HEP":
            geo_cords = get_geo_coords("University of Florida")
        elif site_name == "T3_US_OSG":
            return site #virtual site
        
        site['latitude'] = geo_cords['latitude']
        site['longitude'] = geo_cords['longitude']
        return site

    @staticmethod
    def process_cric_federations(cric_federations_file):
        with open(cric_federations_file) as file:
            federations = json.load(file)
            for federation_name, federation in federations.items():
                if federation_name == "NULL":
                    continue
                fed_obj = FederationsService.get_or_create(federation_name)
                fed_obj.accounting_name = federation['accounting_name']
                fed_obj.tier = federation['tier_level']
                for vo_name in federation['vos']:
                    vo = VOService.get_or_create(vo_name)
                    fed_obj.supported_vos.add(vo)
                pledges = federation['pledges']
                if federation['rcsites'] is not None:
                    for site in federation['rcsites']:
                        site_obj = SiteService.get_or_create(site)
                        site_obj.federation = fed_obj
                        site_obj.sources.append('cric-federations')
                        site_obj.tier = federation['tier_level']
                        SiteService.save(site_obj)
                        fed_obj.site_set.add(site_obj)
                for year, vos in pledges.items():
                    for vo, pledge in vos.items():
                        vo_obj = VOService.get_or_create(vo)
                        pledge_obj = PledgeService.get_or_create(fed_obj, vo_obj)
                        pledge_obj.year = year
                        if 'CPU' in pledge:
                            pledge_obj.cpu = pledge['CPU']
                        if 'Disk' in pledge:
                            pledge_obj.disk = pledge['Disk']
                        if 'Tape' in pledge:
                            pledge_obj.tape = pledge['Tape']
                        PledgeService.save(pledge_obj)
                        fed_obj.pledge_set.add(pledge_obj)
                FederationsService.save(fed_obj)

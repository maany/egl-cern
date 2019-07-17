import multiprocessing

import requests
from django.conf import settings
from time import time
from queue import Queue
from threading import Thread

from egl_rest.api.models import Transfer, Site, VO
from egl_rest.api.services.site_service import SiteService
from egl_rest.api.services.vo_service import VOService
import logging


logger = logging.getLogger(__name__)


class GrafanaServiceWorker(Thread):
    def __init__(self, queue, transfers):
        Thread.__init__(self)
        self.queue = queue
        self.transfers = transfers
    def run(self):
        while True:
            transfer_list_array = self.queue.get()
            transfer_list = self.process_transfer_data(transfer_list_array)
            self.transfers = self.transfers + transfer_list
            self.queue.task_done()

    def process_transfer_data(self, transfers_string_array):
        transfers_list = []
        for transfer_string in transfers_string_array:
            unknown_sites = []
            transfer_info = transfer_string.split(',')
            transfer = Transfer()
            transfer.end = int(int(transfer_info[2]) / 1000000000)
            try:
                site_name = GrafanaService.cric_influx_name_map(transfer_info[3])
                transfer.source = SiteService.get(site_name)
            except Site.DoesNotExist:
                unknown_sites.append(site_name)
                # logger.error("{source} source site was not found in database".format(source=site_name))
                continue
            try:
                site_name = GrafanaService.cric_influx_name_map(transfer_info[4])
                transfer.destination = SiteService.get(site_name)
            except Site.DoesNotExist:
                unknown_sites.append(site_name)
                # logger.error("{destination} destination was not found in database".format(destination=site_name))
                continue
            try:
                transfer.vo = VOService.get(transfer_info[5])
            except VO.DoesNotExist:
                logger.error("{vo} was not found in database".format(vo=transfer_info[5]))
                continue
            transfer.technology = transfer_info[6]
            transfer.transferred_volume = float(transfer_info[7])
            transfer.average_file_size = float(transfer_info[8])
            transfer.count = int(transfer_info[9])
            transfer.average_operation_time = float(transfer_info[10])
            transfer.total_operation_time = transfer.count * transfer.average_operation_time
            transfer.begin = int(transfer.end - transfer.total_operation_time)

            transfers_list.append(transfer)

        return transfers_list


def worker(transfers_string_array):
    transfers_list = []
    for transfer_string in transfers_string_array:
        unknown_sites = []
        transfer_info = transfer_string.split(',')
        transfer = Transfer()
        transfer.end = int(int(transfer_info[2]) / 1000000000)
        try:
            site_name = GrafanaService.cric_influx_name_map(transfer_info[3])
            transfer.source = SiteService.get(site_name)
        except Site.DoesNotExist:
            unknown_sites.append(site_name)
            # logger.error("{source} source site was not found in database".format(source=site_name))
            continue
        try:
            site_name = GrafanaService.cric_influx_name_map(transfer_info[4])
            transfer.destination = SiteService.get(site_name)
        except Site.DoesNotExist:
            unknown_sites.append(site_name)
            logger.error("{destination} destination was not found in database".format(destination=site_name))
            continue
        try:
            transfer.vo = VOService.get(transfer_info[5])
        except VO.DoesNotExist:
            logger.error("{vo} was not found in database".format(vo=transfer_info[5]))
            continue
        transfer.technology = transfer_info[6]
        transfer.transferred_volume = float(transfer_info[7])
        transfer.average_file_size = float(transfer_info[8])
        transfer.count = int(transfer_info[9])
        transfer.average_operation_time = float(transfer_info[10])
        transfer.total_operation_time = transfer.count * transfer.average_operation_time
        transfer.begin = int(transfer.end - transfer.total_operation_time)

        transfers_list.append(transfer)

    return transfers_list



class GrafanaService:
    api_key = settings.GRAFANA_API_KEY

    @staticmethod
    def fetch_influx_db_transfers_raw(filters):
        ts = time()
        transfers_string_array = GrafanaService.query_db("transfer_xrootd", filters) + GrafanaService.query_db(
            "transfer_fts", filters)
        query_time = time() - ts
        output = []
        for transfer_info_string in transfers_string_array:
            transfer_info = transfer_info_string.split(',')
            transfer_obj = {}
            try:
                site_name = GrafanaService.cric_influx_name_map(transfer_info[3])
                transfer_obj['source'] = SiteService.get(site_name).name
            except Site.DoesNotExist:
                # logger.error("{source} source site was not found in database".format(source=site_name))
                continue
            try:
                site_name = GrafanaService.cric_influx_name_map(transfer_info[4])
                transfer_obj['destination'] = SiteService.get(site_name).name
            except Site.DoesNotExist:
                # unknown_sites.append(site_name)
                logger.error("{destination} destination was not found in database".format(destination=site_name))
                continue
            try:
                transfer_obj['vo'] = VOService.get(transfer_info[5]).name
            except VO.DoesNotExist:
                logger.error("{vo} was not found in database".format(vo=transfer_info[5]))
                continue
            transfer_obj['end'] = int(int(transfer_info[2]) / 1000000000)
            transfer_obj['technology'] = transfer_info[6]
            transfer_obj['transferred_volume'] = float(transfer_info[7])
            transfer_obj['average_file_size'] = float(transfer_info[8])
            transfer_obj['count'] = int(transfer_info[9])
            transfer_obj['average_operation_time'] = float(transfer_info[10])
            transfer_obj['total_operation_time'] = float(transfer_obj['count']) * float(transfer_obj['average_operation_time'])
            transfer_obj['begin'] = float(transfer_obj['end']) - float(transfer_obj['total_operation_time'])
            output.append(transfer_obj)
        operation_time = time() - ts - query_time
        print("Query Time: {query_time}, Processing Time: {time}s".format(time=operation_time, query_time=query_time))
        return output

    @staticmethod
    def fetch_influx_db_transfers(filters):
        ts = time()
        transfers = []
        thread_count = 4
        process_count = thread_count
        transfers_string_array = GrafanaService.query_db("transfer_xrootd", filters) + GrafanaService.query_db("transfer_fts", filters)
        query_time = time() - ts
        len_per_thread_transfer_string_array = int(len(transfers_string_array)/thread_count)
        f = lambda transfer_string_arr, n=len_per_thread_transfer_string_array: [transfer_string_arr[i:i+n] for i in range(0, len(transfer_string_arr), n)]
        per_thread_transfer_string_array = f(transfers_string_array)
        ## THREADING
        queue = Queue()
        # for x in range(thread_count):
        #     worker = GrafanaServiceWorker(queue, transfers)
        #     worker.daemon = True
        #     worker.start()
        #
        # for data in per_thread_transfer_string_array:
        #     queue.put(data)
        #
        # queue.join()
        ## MULTIPROCESSING
        # jobs = []
        # for i in range(process_count):
        #     p = multiprocessing.Process(target=worker, args=(per_thread_transfer_string_array[i],))
        #     jobs.append(p)
        #     p.start()
        # for job in jobs:
        #     job.join()
        ## REGULAR
        transfers = GrafanaServiceWorker(queue, transfers).process_transfer_data(transfers_string_array)
        operation_time = time() - ts
        logger.info("Took {time}s".format(time=operation_time))
        print("Query Time: {query_time}, Processing Time: {time}s".format(time=operation_time, query_time=query_time))
        return transfers

    @staticmethod
    def cric_influx_name_map(influx_name):
        if influx_name == "CERN":
            return "CERN-PROD"
        if influx_name == "IN2P3":
            return "IN2P3-CC"
        if influx_name == "GRIF-LAL":
            return "GRIF"
        if influx_name == "su-cms":
            return "osu-cms"
        if influx_name == "LCG_KNU":
            return "KR-KNU-T3"
        if influx_name == "Baylor-Tier3":
            return "Baylor-Kodiak"
        if influx_name == "INFN_Napoli":
            return "INFN-NAPOLI-ATLAS"
        if influx_name == "JINR":
            return "JINR-T1"
        if influx_name == "UMD-CMS":
            return "umd-cms"
        if influx_name == "BU":
            return "BU_ATLAS_Tier2"
        return influx_name

    @staticmethod
    def query_db(db_name, filters):
        GRAFANA_URL = 'https://monit-grafana.cern.ch/api/datasources/proxy/7794/query'
        query = "SELECT src_site, dst_site, vo, technology, transferred_volume, avg_file_size, count, avg_operation_time FROM {database_name} WHERE count>0 AND avg_operation_time>0"

        if "starts_between" in filters and "ends_between" not in filters:
            starts_between = filters['starts_between'].split(',')
            start = int(starts_between[0])
            end = int(starts_between[-1])
            query = "{query} time - count * avg_operation_time >= {start} AND time - count * avg_operation_time " \
                    "<= {end}".format(
                query=query,
                start=start,
                end=end
            )
        if "ends_between" in filters:
            ends_between = filters['ends_between'].split(',')
            start = ends_between[0]
            end = ends_between[1]
            query = "{query} AND time > {start} AND time < {end}".format(
                query=query,
                start=start,
                end=end
            )

        if "vo" in filters:
            # for vo in filters['vos']:
            query = "{query} AND vo={vo}".format(query=query, vo=filters['vo'])

        if "minimum_transferred_volume" in filters:
            query = "{query} AND transferred_volume>{minimum_transferred_volume}".format(
                query=query, minimum_transferred_volume=filters['minimum_transferred_volume'])
        if "technology" in filters:
            query = "{query} AND technology={technology}".format(query=query, technology=filters['technology'])
        if "source" in filters:
            query = "{query} AND src_site={source}".format(query=query, source=filters['source'])
        if "destination" in filters:
            query = "{query} AND dst_site={destination}".format(query=query, destination=filters['destination'])
        if "limit" in filters:
            query = "{query} LIMIT {limit}".format(query=query, limit=filters['limit'])
        else:
            query = "{query} LIMIT {limit}".format(query=query, limit=50000)
        query = query.format(database_name=db_name)
        parameters = {
            'db': 'monit_production_transfer',
            'q': ' '.join(query.split()),
        }
        headers = {
            'Accept': 'application/csv',
            'Authorization': 'Bearer ' + GrafanaService.api_key,
        }
        response = requests.get(GRAFANA_URL, params=parameters, headers=headers)
        transfers_string_array = response.text.split('\n')[1:-2]
        return transfers_string_array

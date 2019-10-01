from egl_rest.api.helpers import Singleton, timestamp_datetime, datetime_timestamp
from egl_rest.api.render.atlas_data import AtlasData
from egl_rest.api.services.grafana_service import GrafanaService
from egl_rest.api.services.site_service import SiteService


class AtlasService(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def collect_running_job_stats(time_interval_start="now() -3h", time_interval_end="now()", dst_site="~ /^.*$/"):

        datasource_number = '9023'
        api_key = 'eyJrIjoidG5xUFBFdmxFMTJqM1lUNGdJSGRnVDdXREFjdjllc2YiLCJuIjoicHVibGljX3Zpc3VhbGlzYXRpb24iLCJpZCI6MTd9'
        db_name = 'monit_production_atlasjm_running'
        query = 'SELECT sum("wavg_count") / 1 FROM "long_1h"."atlasjm_current_1h" WHERE  ' \
                'time >= {time_interval_start} ' \
                'and time <= {time_interval_end} ' \
                'AND ("jobstatus" = \'running\' ' \
                'AND "dst_experiment_site" ={dst_site} ' \
                'AND "dst_cloud" =~ /^.*$/ ' \
                'AND "dst_country" =~ /^.*$/ ' \
                'AND "dst_federation" =~ /^.*$/ ' \
                'AND "adcactivity" =~ /^.*$/ ' \
                'AND "resourcesreporting" =~ /^.*$/ ' \
                'AND "actualcorecount" =~ /^.*$/ ' \
                'AND "resource_type" =~ /^.*$/ ' \
                'AND "workinggroup" =~ /^.*$/ ' \
                'AND "inputfiletype" =~ /^.*$/ ' \
                'AND "eventservice" =~ /^.*$/ ' \
                'AND "inputfileproject" =~ /^.*$/ ' \
                'AND "outputproject" =~ /^.*$/ ' \
                'AND "jobstatus" =~ /^.*$/ ' \
                'AND "computingsite" =~ /^.*$/ ' \
                'AND "gshare" =~ /^.*$/ ' \
                'AND "dst_tier" =~ /^.*$/ ' \
                'AND "processingtype" =~ /^.*$/ ' \
                'AND "nucleus" =~ /^.*$/ ' \
                'AND "error_category" =~ /^.*$/ ) ' \
                'GROUP BY time(1h), "adcactivity"'.format(
                time_interval_start=time_interval_start,
                time_interval_end=time_interval_end,
                dst_site=dst_site
                )
        output = GrafanaService.query_db(datasource_number, api_key, db_name, query)
        output = output.split("\n")[1:-1]
        objects = {}
        for object in output:
            values = object.split(',')
            time = timestamp_datetime(int(values[2]))
            activity = values[1].split('=')[-1].replace('\\', ' ')
            value = values[3]
            if time in objects.keys():
                objects[time][activity] = value
            else:
                objects[time] = {
                    activity: value
                }
        return objects

    @staticmethod
    def fetch_all_stats(time_interval_start, time_interval_end):
        if type(time_interval_start) == type(""):
            if "now" not in time_interval_start:
                time_interval_start = datetime_timestamp(time_interval_start)

        if type(time_interval_end) == type(""):
            if "now" not in time_interval_end:
                time_interval_end = datetime_timestamp(time_interval_end)
        global_running_jobs = AtlasService.collect_running_job_stats(time_interval_start=time_interval_start,
                                               time_interval_end=time_interval_end)
        # site_level_stats = []
        # active_sites = SiteService.get_active_sites()
        # for site in active_sites:
        #     running_jobs = AtlasService.collect_running_job_stats(time_interval_start=time_interval_start,
        #                                                           time_interval_end=time_interval_end,
        #                                                           dst_site=site.name)
        #     site_level_stats.append({
        #         "site": site.name,
        #         "running_jobs": running_jobs
        #     })
        output_dict = {
            "global_statistics": {
                "running_jobs": global_running_jobs
            }
        }
        return AtlasData.generate_v1_0(output_dict)
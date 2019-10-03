from django.conf import settings

from egl_rest.api.helpers import datetime_timestamp, timestamp_datetime
from egl_rest.api.render.cms_data import CMSData
from egl_rest.api.services.grafana_service import GrafanaService
from egl_rest.api.services.site_service import SiteService


class CMSService():

    @staticmethod
    def collect_running_job_stats(time_interval_start="now() -3h", time_interval_end="now()", dst_site=".*"):

        datasource_number = '7731'
        api_key = settings.GRAFANA_CMS_API_KEY
        db_name = 'monit_production_cmsjm'
        query = 'SELECT SUM(wavg_count) FROM "long"."condor_1h" WHERE ' \
                '"CMS_JobType" =~ /^.*$/ AND ' \
                '"Site" =~ /^{dst_site}$/ AND ' \
                '"Tier" =~ /^.*$/ AND ' \
                '"Type" =~ /^.*$/ AND ' \
                '"CMSPrimaryDataTier" =~ /^.*$/ AND ' \
                '"Status" = \'Running\' AND ' \
                'time >= {time_interval_start} and time <= {time_interval_end} ' \
                'GROUP BY time(1h), "CMS_JobType"'.format(
            time_interval_start=time_interval_start,
            time_interval_end=time_interval_end,
            dst_site=dst_site
        )

        output = GrafanaService.query_db(datasource_number, api_key, db_name, query)
        output = output.split("\n")[1:-1]
        objects = {}
        for object in output:
            values = object.split(',')
            time = timestamp_datetime(int(values[2])).strftime("%Y-%m-%d %H:%M:%S")
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

        global_running_jobs = CMSService.collect_running_job_stats(time_interval_start=time_interval_start,
                                                                   time_interval_end=time_interval_end)

        site_level_stats = []
        active_cms_sites = SiteService.get_active_sites().filter(supported_vos__name__contains="cms")
        for site in active_cms_sites:
            running_jobs =None
            for site_vo in site.sitevo_set.filter(vo__name="cms"):
                temp_running_jobs = CMSService.collect_running_job_stats(time_interval_start=time_interval_start,
                                                                time_interval_end=time_interval_end,
                                                                dst_site=site_vo.name)
                if running_jobs is None:
                    running_jobs = temp_running_jobs
                else:
                    for time in temp_running_jobs.keys():
                        for activity in temp_running_jobs[time].keys():
                            if time in running_jobs:
                                if activity in running_jobs:
                                    running_jobs[time][activity] = temp_running_jobs[time][activity]
                                else:
                                    running_jobs[time][activity] = temp_running_jobs[time][activity]
                            else:
                                running_jobs[time] = {
                                    activity: temp_running_jobs[time][activity]
                                }

            site_level_stats.append({
                "site": site.name,
                "running_jobs": running_jobs
            })

        output_dict = {
            "global_statistics": {
                "running_jobs": global_running_jobs,
            },
            "site_level_stats": site_level_stats
        }
        return CMSData.generate_v1_0(output_dict)

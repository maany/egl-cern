from egl_rest.api.helpers import Singleton
from egl_rest.api.services.grafana_service import GrafanaService


class AtlasService(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def collect_global_running_job_stats(time_interval_start="now() -3h", time_interval_end="now()", dst_site="~ /^.*$/"):

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
        output.split()[1:-1]

        return output

    @staticmethod
    def collect_site_stats():
        pass

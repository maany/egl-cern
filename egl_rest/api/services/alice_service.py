import json

import requests
from os import walk
import os
from django.conf import settings
from egl_rest.api.helpers import datetime_timestamp, timestamp_datetime
from egl_rest.api.services.site_service import SiteService
from egl_rest.api.models import Site
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class AliceService:

    @staticmethod
    def collect_running_job_stats(time_interval_start, time_interval_end, data_dir):
        time_interval_start = datetime_timestamp(time_interval_start)/1000000000
        time_interval_end = datetime_timestamp(time_interval_end)/1000000000
        combined_data = AliceService.get_combined_data_for_time_interval(time_interval_start, time_interval_end, data_dir)
        site_level_stats = []
        cric_alice_sites = SiteService.get_active_sites().filter(supported_vos__name__contains="alice")
        global_running_jobs = 0
        for site in cric_alice_sites:
            running_jobs = {}
            for site_vo in site.sitevo_set.filter(vo__name="alice"):
                alice_name = site_vo.name
                if alice_name in AliceService.generate_file_dict_template(data_dir).keys():
                    for timestamp in combined_data.keys():
                        running_jobs[int(timestamp)] = int(combined_data[timestamp][alice_name]['parallel_jobs'])
                        global_running_jobs += running_jobs[timestamp]
                else:
                    logger.error("Site {site_name} does not exist in combined data for alice job statistics".format(site_name=alice_name))

            site_level_stats.append({
                'site': site.name,
                'running_jobs': running_jobs
            })
        output_dict = {
            "global_statistics": {
                "running_jobs": global_running_jobs
            },
            "site_level_stats": site_level_stats
        }

        return output_dict

    @staticmethod
    def get_combined_data_for_time_interval(time_interval_start, time_interval_end, data_dir):
        output = {}
        filenames = []
        template_dict = AliceService.generate_file_dict_template(data_dir)
        duration_in_hours = int((time_interval_end - time_interval_start)/(60*60))
        time_checkpoints = [time_interval_end]
        for i in range(0, duration_in_hours):
            time_checkpoints.append(time_interval_end - i*60*60)
        time_checkpoints.sort()

        for (dirpath, dirnames, files) in walk("{data_dir}/alice".format(data_dir=data_dir)):
            filenames.extend(files)

        for timestamp in time_checkpoints:
            files_to_parse = []
            for file in filenames:
                # file_start_time = int(file.split("-")[1])
                file_end_time = int(file.split("-")[2])
                if file_end_time <= timestamp:
                    files_to_parse.append(file)
            if len(files_to_parse) == 0:
                logger.error("Alice jon statistics data not available for {timestamp} i.e {datetime}".format(
                    timestamp = timestamp,
                    datetime = timestamp_datetime(timestamp)
                ))
                output[timestamp] = template_dict
                continue
            files_to_parse.sort(key=AliceService.cmp_key, reverse=True)
            file_to_parse = files_to_parse[0]
            with open("{data_dir}/alice/{file}".format(data_dir=data_dir, file=file_to_parse), 'r') as f:
                file_data = json.load(f)
                output[timestamp] = file_data
        return output
        # for index, file in enumerate(files_to_parse):
        #     delta_minutes = int(file.split('_')[-1])
        #     delta_seconds = delta_minutes * 60
        #     timestamp = time_interval_end - delta_seconds
        #     timestamp_str = timestamp_datetime(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        #     output[timestamp_str] = delta_minutes
        #
        # cron_interval = int(settings.ALICE_CRON_INTERVAL_MINUTES)
        # requested_duration = int((time_interval_end - time_interval_start)/60000000000)
        # files_per_hour = int(60/cron_interval)
        #
        #
        # if not os.path.exists("{data_dir}/alice".format(data_dir=data_dir)):
        #     AliceService.download_alice_files(data_dir)
        # number_of_files_to_read = int(requested_duration/cron_interval)
        # filenames = []
        # for (dirpath, dirnames, files) in walk("{data_dir}/alice".format(data_dir=data_dir)):
        #     filenames.extend(files)
        # number_of_files_available = len(filenames)
        # num_files = min(number_of_files_to_read, number_of_files_available)
        # filenames.sort(key=AliceService.cmp_key)
        # hourly_files = filenames[::files_per_hour]
        # combined_data = {}
        # for file in hourly_files:
        #     minutes_delta = int(file.split('_')[-1])
        #     timestamp = time_interval_start + timedelta(minutes=minutes_delta)
        #     formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        #
        # current_file = 0
        # for file in filenames[::files_per_hour]:
        #     current_file = current_file + files_per_hour
        #     if current_file > num_files:
        #         break
        #     with open("{data_dir}/alice/{file}".format(data_dir=data_dir, file=file), 'r') as f:
        #         file_data = json.load(f)
        #         combined_data[time_interval_start + timedelta(minutes=int(file.split['_'][-1]))] = AliceService.combine_files(combined_data, file_data)
        # return combined_data

    @staticmethod
    def generate_file_dict_template(data_dir):
        filenames = []
        path = "{data_dir}/alice".format(data_dir=data_dir)
        for (dirpath, dirnames, files) in walk(path):
            filenames.extend(files)
        if len(filenames) == 0:
            logger.error("Could not generate a template for Alice job statistics dictionary. "
                         "There needs to be at lease one file present in {path}".format(path=path))
            return {}
        with open("{path}/{file}".format(path=path, file=filenames[0]), 'r') as f:
            dict = json.load(f)
            for site in dict.keys():
                dict[site]["CPU_time"] = 0
                dict[site]["CPU_time_KSI2K"] = 0
                dict[site]["completed_jobs"] = 0
                dict[site]["parallel_jobs"] = 0
                dict[site]["successfully_completed_jobs"] = 0
                dict[site]["wall_time"] = 0
                dict[site]["wall_time_KSI2Ks"] = 0
            return dict

    @staticmethod
    def combine_files(combined_data, file_data):
        if combined_data == {}:
            combined_data = file_data
            return combined_data
        for site in file_data.keys():
            combined_data[site]["CPU_time"] = int(combined_data[site]["CPU_time"]) + int(file_data[site]["CPU_time"])
            combined_data[site]["CPU_time_KSI2K"] = int(combined_data[site]["CPU_time_KSI2K"]) + int(file_data[site]["CPU_time_KSI2K"])
            combined_data[site]["completed_jobs"] = int(combined_data[site]["completed_jobs"]) + int(file_data[site]["completed_jobs"])
            combined_data[site]["parallel_jobs"] = int(combined_data[site]["parallel_jobs"]) + int(file_data[site]["parallel_jobs"])
            combined_data[site]["successfully_completed_jobs"] = int(combined_data[site]["successfully_completed_jobs"]) + int(file_data[site]["successfully_completed_jobs"])
            combined_data[site]["wall_time"] = int(combined_data[site]["wall_time"]) + int(file_data[site]["wall_time"])
            combined_data[site]["wall_time_KSI2Ks"] = int(combined_data[site]["wall_time_KSI2K"]) + int(file_data[site]["wall_time_KSI2K"])

        return combined_data

    @staticmethod
    def format_file(filedata):
        formatted_data = {}
        lines = filedata.split("\n")[1:-1]
        for line in lines:
            data = line.split(',')
            parameter = data[2]
            value = data[3]
            site_name = data[0]
            if parameter in ["CPU_time", "CPU_time_KSI2K", "completed_jobs", "parallel_jobs", "successfully_completed_jobs", "wall_time", "wall_time_KSI2Ks"]:
                if int(value) == -1:
                    value = 0
            if site_name not in formatted_data.keys():
                formatted_data[site_name] = {parameter: value}
            else:
                formatted_data[site_name][parameter] = value
        return formatted_data

    @staticmethod
    def cmp_key(file1):
        file1 = int(file1.split('_')[-1])
        return file1

    @staticmethod
    def download_alice_files(data_dir):
        if not os.path.exists("{data_dir}/alice".format(data_dir=data_dir)):
            os.makedirs("{data_dir}/alice".format(data_dir=data_dir))

        response = requests.get("http://pcalimonitor.cern.ch/export/jobs2.jsp")
        # rename all files
        filenames = []
        for (dirpath, dirnames, files) in walk("{data_dir}/alice".format(data_dir=data_dir)):
            filenames.extend(files)
        filenames.sort(key=AliceService.cmp_key, reverse=True)
        if len(filenames)>(60*48/int(settings.ALICE_CRON_INTERVAL_MINUTES)): # Cron runs every 10 minutes, so 6 files saved per hour, 288 in 48 hours
            os.remove("{data_dir}/alice/{last_file}".format(data_dir=data_dir, last_file=filenames[0]))
        for file in filenames:
            split = file.split('_')
            prefix = split[0]
            postfix = split[-1]
            new_postfix = int(postfix) + int(settings.ALICE_CRON_INTERVAL_MINUTES)
            os.rename("{data_dir}/alice/{file}".format(data_dir=data_dir, file=file),
                      "{data_dir}/alice/{prefix}_{new_postfix}".format(data_dir=data_dir, prefix=prefix,
                                                                       new_postfix=new_postfix))
            sample_line = response.text.split("\n")[2].split(',')
            start_timestamp = sample_line[6]
            end_timestamp = sample_line[7]
        with open("{data_dir}/alice/{prefix}-{start_timestamp}-{end_timestamp}-_{time_interval}".format(data_dir=data_dir,
                                                                                                       prefix="alice",
                                                                                                       start_timestamp=start_timestamp,
                                                                                                       end_timestamp=end_timestamp,
                                                                                                       time_interval=settings.ALICE_CRON_INTERVAL_MINUTES), 'w') as f:
            formatted_data = AliceService.format_file(response.text)
            f.write(json.dumps(formatted_data, indent=4, sort_keys=True))

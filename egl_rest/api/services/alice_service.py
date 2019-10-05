import json

import requests
from os import walk
import os
from django.conf import settings
from egl_rest.api.helpers import datetime_timestamp


class AliceService:

    @staticmethod
    def collect_running_job_stats(time_interval_start, time_interval_end, data_dir):
        time_interval_start = datetime_timestamp(time_interval_start)
        time_interval_end = datetime_timestamp(time_interval_end)
        combined_data = AliceService.get_combined_data_for_time_interval(time_interval_start, time_interval_end, data_dir)
        global_running_jobs = 0
        site_level_stats = []
        for site in combined_data:
            site_level_stats.append({
                'site': combined_data[site]["MLname"],
                'running_jobs': combined_data[site]['parallel_jobs']
            })
            global_running_jobs += combined_data[site]['parallel_jobs']

        output_dict = {
            "global_statistics": {
                "running_jobs": global_running_jobs
            },
            "site_level_stats": site_level_stats
        }

        return output_dict

    @staticmethod
    def get_combined_data_for_time_interval(time_interval_start, time_interval_end, data_dir):
        cron_interval = int(settings.ALICE_CRON_INTERVAL_MINUTES)
        requested_duration = int((time_interval_end - time_interval_start)/60000000000)

        if not os.path.exists("{data_dir}/alice".format(data_dir=data_dir)):
            AliceService.download_alice_files(data_dir)
        number_of_files_to_read = int(requested_duration/cron_interval)

        filenames = []
        for (dirpath, dirnames, files) in walk("{data_dir}/alice".format(data_dir=data_dir)):
            filenames.extend(files)
        number_of_files_available = len(filenames)
        num_files = min(number_of_files_to_read, number_of_files_available)
        filenames.sort(key=AliceService.cmp_key)
        combined_data = {}
        current_file = 0
        for file in filenames:
            current_file = current_file + 1
            if current_file > num_files:
                break
            with open("{data_dir}/alice/{file}".format(data_dir=data_dir, file=file), 'r') as file:
                file_data = json.load(file)
                combined_data = AliceService.combine_files(combined_data, file_data)
        return combined_data

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
        with open("{data_dir}/alice/{prefix}_{time_interval}".format(data_dir=data_dir, prefix="alice", time_interval=settings.ALICE_CRON_INTERVAL_MINUTES), 'w') as f:
            formatted_data = AliceService.format_file(response.text)
            f.write(json.dumps(formatted_data, indent=4, sort_keys=True))

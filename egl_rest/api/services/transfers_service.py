from egl_rest.api.render.transfer_data import TransferData
from egl_rest.api.services.grafana_service import GrafanaService
import statistics
import json

class TransfersService:


    @staticmethod
    def fetch_raw_transfers(filters):
        return GrafanaService.fetch_influx_db_transfers_raw(filters)

    @staticmethod
    def fetch_transfers(filters):
        return GrafanaService.fetch_influx_db_transfers(filters)

    @staticmethod
    def generate_raw_transfer_data(transfers, version):
        if version not in TransferData.supported_schemas:
            return "Schema version {version} is not supported. Try one of {supported_schemas}".format(
                version=version,
                supported_schemas=TransferData.supported_schemas
            )
        output = {'transfers': [], 'meta': [], 'current_schema_version': version,
                  'latest_schema_version': TransferData.get_latest_schema()}

        output['transfers'] = transfers
        output['meta'] = TransfersService.analyse_raw(transfers)
        return json.dumps(output)

    @staticmethod
    def generate_transfer_data(transfers, version):
        if version not in TransferData.supported_schemas:
            return "Schema version {version} is not supported. Try one of {supported_schemas}".format(
                version=version,
                supported_schemas=TransferData.supported_schemas
            )
        output = {'transfers': [], 'meta': [], 'current_schema_version': version,
                      'latest_schema_version': TransferData.get_latest_schema()}

        for transfer in transfers:
            output['transfers'].append(TransferData.render(transfer, version))

        output['meta'] = TransfersService.analyse(transfers)
        return json.dumps(output)

    @staticmethod
    def analyse(transfers):
        op_time_arr = []
        for transfer in transfers:
            op_time_arr.append(transfer.total_operation_time)
        try:
            mode = statistics.mode(op_time_arr)
        except:
            mode = "could not find unique mode"
        return {
            "count": len(op_time_arr),
            "mean_total_operation_time": statistics.mean(op_time_arr),
            "mode_total_operation_time": mode,
            "max_total_operation_time": max(op_time_arr),
            "min_total_operation_time": min(op_time_arr)
        }

    @staticmethod
    def analyse_raw(transfers):
        return {
            "mean": "tbc"
        }

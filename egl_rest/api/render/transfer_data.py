class TransferData:
    supported_schemas = [1.0]

    @staticmethod
    def render(transfer, version):
        if version == 1.0:
            return TransferData.generate_v1_0(transfer)
        else:
            raise Exception("Schema version {version} not supported for data transfers.".format(version=version))

    @staticmethod
    def get_latest_schema():
        TransferData.supported_schemas.sort()
        return TransferData.supported_schemas[-1]

    @staticmethod
    def generate_v1_0(transfer):
        transfer_dict = {
            "source": {
                "name": transfer.source.name,
                "geo_coordinates": {
                    "latitude": transfer.source.latitude,
                    "longitude": transfer.source.longitude
                }
            },
            "destination": {
                "name": transfer.destination.name,
                "geo_coordinates": {
                    "latitude": transfer.destination.latitude,
                    "longitude": transfer.destination.longitude
                }
            },
            "vo": transfer.vo.name,
            "begin": transfer.begin,
            "end": transfer.end,
            "technology": transfer.technology,
            "average_file_size": transfer.average_file_size,
            "total_file_size": transfer.count * transfer.average_file_size,
            "average_operation_time": transfer.average_operation_time,
            "total_operation_time": transfer.count * transfer.average_operation_time,
            "count": transfer.count
        }
        return transfer_dict

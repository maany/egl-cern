import json


class CMSData:
    supported_schemas = [1.0]

    @staticmethod
    def get_latest_schema():
        CMSData.supported_schemas.sort()
        return CMSData.supported_schemas[-1]

    @staticmethod
    def render(cms_data, version):
        if version == 1.0:
            return CMSData.generate_v1_0(cms_data)

    @staticmethod
    def generate_v1_0(cms_data):
        return json.dumps(cms_data)

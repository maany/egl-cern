import json

class AtlasData:
    supported_schemas = [1.0]

    @staticmethod
    def get_latest_schema():
        AtlasData.supported_schemas.sort()
        return AtlasData.supported_schemas[-1]

    @staticmethod
    def render(atlas_data, version):
        if version == 1.0:
            return AtlasData.generate_v1_0(atlas_data)
        else:
            Exception("Schema version {version} not supported for atlas running jobs.".format(version=version))

    @staticmethod
    def generate_v1_0(atlas_data):
        return json.dump(atlas_data)

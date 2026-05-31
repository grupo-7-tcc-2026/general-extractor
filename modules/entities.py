from enum import Enum, auto
from custom_io.bucket import Bucket, EnumBuckets

class EnumDataFormats(Enum):
    PANDAS = auto()
    GEOPANDAS = auto()

class Entity:
    key: str
    date_format: EnumDataFormats
    bucket: Bucket
    params: dict

    def __init__(self, key: str, date_format: EnumDataFormats, bucket: Bucket, params: dict | None = None):
        self.key = key
        self.date_format = date_format
        self.bucket = bucket
        self.params = params if params is not None else {}

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return self.key

class EnumEntities(Enum):

    RAW_DISTRICTS = Entity(
        "geoportal_distrito_municipal_v2.geojson", EnumDataFormats.GEOPANDAS, EnumBuckets.RAW
    )
    RAW_TRASH = Entity(
        "geoportal_sac_remocao_entulho.geojson", EnumDataFormats.GEOPANDAS, EnumBuckets.RAW
    )

    TREATED_DISTRICTS = Entity(
        "trusted_district.geojson", EnumDataFormats.GEOPANDAS, EnumBuckets.TREATED
    )
    TREATED_TRASH = Entity(
        "trusted_trash.geojson", EnumDataFormats.GEOPANDAS, EnumBuckets.TREATED
    )
    TREATED_CLIMATE = Entity(
        "trusted_climate.csv", EnumDataFormats.PANDAS, EnumBuckets.TREATED
    )

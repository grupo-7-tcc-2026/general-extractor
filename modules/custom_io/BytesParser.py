import pandas as pd
import geopandas as gpd
from abc import ABC
from io import BytesIO
from entities import Entity, EnumDataFormats

class BytesParser(ABC):

    @staticmethod
    def parse_content(entity: Entity, byte_content: bytes) -> pd.DataFrame | dict:
        match entity.date_format:
            case EnumDataFormats.PANDAS:
                return BytesParser._bytes_to_pandas(byte_content, entity.params)
            case EnumDataFormats.GEOPANDAS:
                return BytesParser._bytes_to_geopandas(byte_content, entity.params)
            case _:
                raise NotImplementedError("Formato de dados não implementado.")

    @staticmethod
    def _bytes_to_pandas(byte_content: bytes, params: dict) -> pd.DataFrame:
        return pd.read_csv(BytesIO(byte_content), **params)

    @staticmethod
    def _bytes_to_geopandas(byte_content: bytes, params: dict) -> gpd.GeoDataFrame:
        return gpd.read_file(BytesIO(byte_content), **params)

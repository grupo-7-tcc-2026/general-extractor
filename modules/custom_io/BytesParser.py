import pandas as pd
import geopandas as gpd
from abc import ABC
from io import BytesIO, StringIO

from shapely.geometry import geo

from entities import Entity, EnumDataFormats

class BytesParser(ABC):

    @staticmethod
    def parse_read_content(entity: Entity, byte_content: bytes) -> pd.DataFrame | dict:
        match entity.date_format:
            case EnumDataFormats.PANDAS:
                return BytesParser._read_pandas(byte_content, entity.params)

            case EnumDataFormats.GEOPANDAS:
                return BytesParser._read_geopandas(byte_content, entity.params)
            case _:
                raise NotImplementedError("Formato de dados não implementado.")

    @staticmethod
    def _read_pandas(byte_content: bytes, params: dict) -> pd.DataFrame:
        return pd.read_csv(BytesIO(byte_content), **params)

    @staticmethod
    def _read_geopandas(byte_content: bytes, params: dict) -> gpd.GeoDataFrame:
        return gpd.read_file(BytesIO(byte_content), **params)

    @staticmethod
    def parse_write_content(entity: Entity, df: pd.DataFrame) -> bytes:
        match entity.date_format:
            case EnumDataFormats.PANDAS:
                return BytesParser._write_pandas(df, entity.params)
            case EnumDataFormats.GEOPANDAS:
                return BytesParser._write_geopandas(df, entity.params)
            case _:
                raise NotImplementedError("Formato de dados não implementado.")

    @staticmethod
    def _write_pandas(df: pd.DataFrame, params: dict) -> bytes:
        buffer = BytesIO()
        df.to_csv(buffer, index=False, **params)
        return buffer.getvalue()

    @staticmethod
    def _write_geopandas(gdf: gpd.GeoDataFrame, params: dict) -> bytes:
        return bytes(gdf.to_json(**params).encode("utf-8"))

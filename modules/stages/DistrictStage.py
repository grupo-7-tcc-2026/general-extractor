import pandas as pd
from modules.entities import EnumEntities
from modules.stages.IStage import IStage

class DistrictStage(IStage):

    required_entities = {EnumEntities.RAW_DISTRICTS.value}
    generated_entity = EnumEntities.TREATED_DISTRICTS.value

    def _model_data(self) -> pd.DataFrame:
        df_dist_raw = self.data_heap[EnumEntities.RAW_DISTRICTS.value.key]
        df_dist_raw = df_dist_raw.to_crs(epsg=4326)

        df_dist_treated = df_dist_raw.drop(columns="id").rename(columns={
            "cd_identificador_distrito": "id", "nm_distrito_municipal": "nome", "nm_regiao_05": "região"
        })[["id", "nome", "região", "geometry"]].copy()
        df_dist_treated["lat"] = df_dist_treated.centroid.x
        df_dist_treated["long"] = df_dist_treated.centroid.y
        return df_dist_treated

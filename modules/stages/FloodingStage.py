from datetime import timedelta

import pandas as pd
from modules.entities import EnumEntities
from modules.stages.IStage import IStage


class FloodingStage(IStage):
    required_entities = {EnumEntities.RAW_CGE_FLOODING.value, EnumEntities.TREATED_DISTRICTS.value}
    generated_entity = EnumEntities.TREATED_CGE_FLOODING.value

    def _model_data(self) -> pd.DataFrame:
        df_cge_alagamentos_raw = self.data_heap[EnumEntities.RAW_CGE_FLOODING.value.key]
        distr_df = self.data_heap[EnumEntities.TREATED_DISTRICTS.value.key]

        df_cge_alagamentos = df_cge_alagamentos_raw[["distrito", "dt_hr_inicio", "dt_hr_fim"]].copy()

        df_cge_alagamentos["dt_hr_inicio"] = pd.to_datetime(df_cge_alagamentos["dt_hr_inicio"]).dt.floor("h")
        df_cge_alagamentos["dt_hr_fim"] = pd.to_datetime(df_cge_alagamentos["dt_hr_fim"]).dt.floor("h") + timedelta(hours=1)

        df_cge_alagamentos["data_hora"] = df_cge_alagamentos.apply(
            lambda x: pd.date_range(x["dt_hr_inicio"], x["dt_hr_fim"], freq="h").to_list(),
            axis=1
        )
        df_cge_alagamentos = df_cge_alagamentos[["distrito", "data_hora"]].explode("data_hora", ignore_index=True)
        df_cge_alagamentos["data_hora"] = df_cge_alagamentos["data_hora"].dt.strftime("%Y-%m-%dT%H:%M")

        distr_df = distr_df[["id", "nome"]].rename(columns={"nome": "distrito"})
        return df_cge_alagamentos.merge(distr_df, how="left")

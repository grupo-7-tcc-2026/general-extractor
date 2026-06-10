import pandas as pd
from modules.entities import EnumEntities
from modules.stages.IStage import IStage

class DrainageStage(IStage):

    required_entities = {EnumEntities.RAW_DRAINAGE.value, EnumEntities.TREATED_DISTRICTS.value}
    generated_entity = EnumEntities.TREATED_DRAINAGE.value

    def _model_data(self) -> pd.DataFrame:
        df_drenagem_raw = self.data_heap[EnumEntities.RAW_DRAINAGE.value.key]
        distr_df = self.data_heap[EnumEntities.TREATED_DISTRICTS.value.key]

        df_drenagem = df_drenagem_raw[[
            "nm_distrito_municipal", "tem_drenagem", "qt_trechos_drenagem", "extensao_total_m"
        ]].rename(columns={"nm_distrito_municipal": "distrito"}).copy()

        distr_df = distr_df[["id", "nome"]].rename(columns={"nome": "distrito"}).copy()
        return df_drenagem.merge(distr_df, how="left", on="distrito")

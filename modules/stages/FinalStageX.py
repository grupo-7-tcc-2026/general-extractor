import pandas as pd
from entities import EnumEntities
from stages.IStage import IStage

class FinalStageX(IStage):

    required_entities = {
        EnumEntities.TREATED_DISTRICTS.value, EnumEntities.TREATED_TRASH.value, EnumEntities.TREATED_CLIMATE.value
    }
    generated_entity = EnumEntities.FINAL_TABLE_X.value

    def _model_data(self) -> pd.DataFrame:
        distr_df = self.data_heap[EnumEntities.TREATED_DISTRICTS.value.key]
        entulho_df = self.data_heap[EnumEntities.TREATED_TRASH.value.key]
        climate_df = self.data_heap[EnumEntities.TREATED_CLIMATE.value.key]

        amostra_distr = distr_df[["nome", "região"]].rename(columns={"nome": "distrito"})
        amostra_entulho = entulho_df["nome_distrito"].value_counts().rename("qtd_lixo").rename_axis("distrito").reset_index()
        amostra_clima = climate_df.rename(columns={"nome_distrito": "distrito"})[["distrito", "data_hora", "mm_chuva"]]

        return amostra_distr.merge(amostra_entulho).merge(amostra_clima)

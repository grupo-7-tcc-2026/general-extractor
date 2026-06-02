import pandas as pd
from modules.entities import EnumEntities
from modules.stages.IStage import IStage

class FinalStageX(IStage):

    required_entities = {
        EnumEntities.TREATED_DISTRICTS.value, EnumEntities.TREATED_TRASH.value, EnumEntities.TREATED_CLIMATE.value,
        EnumEntities.TREATED_CGE_FLOODING.value, EnumEntities.TREATED_DRAINAGE.value

    }
    generated_entity = EnumEntities.FINAL_TABLE_X.value

    def _model_data(self) -> pd.DataFrame:
        distr_df = self.data_heap[EnumEntities.TREATED_DISTRICTS.value.key]
        entulho_df = self.data_heap[EnumEntities.TREATED_TRASH.value.key]
        climate_df = self.data_heap[EnumEntities.TREATED_CLIMATE.value.key]
        flooding_df = self.data_heap[EnumEntities.TREATED_CGE_FLOODING.value.key]
        drainage_df = self.data_heap[EnumEntities.TREATED_DRAINAGE.value.key]

        amostra_distr = distr_df[["nome", "região"]].rename(columns={"nome": "distrito"})
        amostra_entulho = entulho_df["nome_distrito"].value_counts().rename("qtd_lixo").rename_axis("distrito").reset_index()
        amostra_clima = climate_df.rename(columns={"nome_distrito": "distrito"})[["distrito", "data_hora", "mm_chuva"]]

        return amostra_distr.merge(amostra_entulho).merge(amostra_clima)

        # amostra_distr = distr_df[["nome","região"]].rename(columns={ "nome": "distrito","região": "regiao"})
        # amostra_entulho = (entulho_df["nome_distrito"].value_counts().rename("qtd_lixo").rename_axis("distrito").reset_index())
        # amostra_clima = climate_df.rename(columns={"nome_distrito": "distrito"})[["distrito", "data_hora", "mm_chuva"]]

        # amostra_alagamento = (flooding_df.groupby("distrito").size().rename("qtd_alagamentos").reset_index())
        # amostra_drenagem = drainage_df.rename(columns={"nome_distrito": "distrito"})[["distrito","tem_drenagem",
        #     "qt_trechos_drenagem","extensao_total_m"]].copy()

        # final_df = (
        #     amostra_distr
        #     .merge(amostra_entulho, how="left", on="distrito")
        #     .merge(amostra_clima, how="left", on="distrito")
        #     .merge(amostra_alagamento, how="left", on="distrito")
        #     .merge(amostra_drenagem, how="left", on="distrito")
        # )

        # final_df["qtd_lixo"] = final_df["qtd_lixo"].fillna(0).astype(int)
        # final_df["qtd_alagamentos"] = final_df["qtd_alagamentos"].fillna(0).astype(int)

        # return final_df

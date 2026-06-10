import pandas as pd
from modules.entities import EnumEntities
from modules.stages.IStage import IStage

class FinalStage(IStage):

    required_entities = {
        EnumEntities.TREATED_DISTRICTS.value, EnumEntities.TREATED_TRASH.value, EnumEntities.TREATED_CLIMATE.value,
        EnumEntities.TREATED_CGE_FLOODING.value, EnumEntities.TREATED_DRAINAGE.value

    }
    generated_entity = EnumEntities.FINAL_TABLE.value

    def _model_data(self) -> pd.DataFrame:
        distr_df = self.data_heap[EnumEntities.TREATED_DISTRICTS.value.key]
        entulho_df = self.data_heap[EnumEntities.TREATED_TRASH.value.key]
        climate_df = self.data_heap[EnumEntities.TREATED_CLIMATE.value.key]
        drainage_df = self.data_heap[EnumEntities.TREATED_DRAINAGE.value.key]
        flooding_df = self.data_heap[EnumEntities.TREATED_CGE_FLOODING.value.key]

        amostra_distr = distr_df[["nome", "região"]].rename(columns={"nome": "distrito"})
        amostra_entulho = entulho_df["distrito"].value_counts().rename("qtd_lixo").reset_index()
        amostra_clima = climate_df[["distrito", "data_hora", "mm_chuva", "mm_evaporados", "c_temperatura_solo"]]
        amostra_drenagem = drainage_df[["distrito", "qt_trechos_drenagem", "extensao_total_m"]]
        amostra_alagamento = flooding_df[["distrito", "data_hora"]]
        amostra_alagamento["alagamento"] = True

        eixo_datas = pd.Series(
            pd.date_range(self.start_date, self.end_date, freq="h"), name="data_hora"
        ).dt.strftime("%Y-%m-%dT%H:%M")
        base = amostra_distr.merge(eixo_datas, how="cross")

        base_c_infos_distritais = base.merge(amostra_entulho).merge(amostra_drenagem)

        base_c_clima = base_c_infos_distritais.merge(amostra_clima, how="left")
        base_c_clima["mm_chuva"] = base_c_clima["mm_chuva"].fillna(0)
        base_c_clima["mm_evaporados"] = base_c_clima["mm_evaporados"].fillna(0)
        base_c_clima["c_temperatura_solo"] = base_c_clima["c_temperatura_solo"].fillna(0)

        base_c_alag = base_c_clima.merge(amostra_alagamento, how="left")
        base_c_alag["alagamento"] = base_c_alag["alagamento"].fillna(False)

        qtd_alag = len(base_c_alag[base_c_alag["alagamento"]]) * 2
        df_final = base_c_alag.groupby("alagamento").sample(qtd_alag, random_state=5, replace=True).drop_duplicates()
        return df_final

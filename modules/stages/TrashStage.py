import pandas as pd
from entities import EnumEntities
from stages.IStage import IStage

class TrashStage(IStage):

    required_entities = {EnumEntities.RAW_TRASH.value, EnumEntities.TREATED_DISTRICTS.value}
    generated_entity = EnumEntities.TREATED_TRASH.value

    def _model_data(self) -> pd.DataFrame:
        df_entulho_raw = self.data_heap[EnumEntities.RAW_TRASH.value.key]
        distr_df = self.data_heap[EnumEntities.TREATED_DISTRICTS.value.key]

        df_entulho = df_entulho_raw.drop(columns="id").rename(columns={
            "cd_identificador": "id", "tx_situacao_solicitacao": "status",
            "dc_tema": "tema", "dc_servico": "servico", "dc_assunto": "assunto", "dt_parecer": "data"
        })[["id", "data", "status", "tema", "servico", "assunto", "geometry"]].copy()
        df_entulho["data"] = df_entulho["data"].dt.strftime("%Y-%m-%dT%H:%M:%S")

        juncao = df_entulho.merge(distr_df, how="cross", suffixes=("", "_distrito"))
        juncao = juncao[
            juncao.apply(lambda x: x["geometry_distrito"].contains(x["geometry"]), axis=1)
        ]

        df_entulho_trusted = juncao.rename(columns={"nome": "nome_distrito"}).drop(
            columns=["geometry_distrito", "lat", "long"]
        )
        return df_entulho_trusted

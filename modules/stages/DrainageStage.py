import pandas as pd
from modules.entities import EnumEntities
from modules.stages.IStage import IStage


class DrainageStage(IStage):

    required_entities = {
        EnumEntities.RAW_DRAINAGE.value,
        EnumEntities.TREATED_DISTRICTS.value
    }

    generated_entity = EnumEntities.TREATED_DRAINAGE.value

    def _model_data(self) -> pd.DataFrame:

        df_drenagem_raw = self.data_heap[
            EnumEntities.RAW_DRAINAGE.value.key
        ]

        distr_df = self.data_heap[
            EnumEntities.TREATED_DISTRICTS.value.key
        ]

        df_drenagem = df_drenagem_raw[[
            "nm_distrito_municipal",
            "tem_drenagem",
            "qt_trechos_drenagem",
            "extensao_total_m"
        ]].rename(columns={
            "nm_distrito_municipal": "nome_distrito"
        }).copy()

        # Seleciona apenas as colunas desejadas
        # e remove o acento de "região"
        distr_df = distr_df[[
            "id",
            "nome",
            "região",
            # "geometry",
            "lat",
            "long"
        ]].rename(columns={
            "região": "regiao"
        }).copy()

        df_drenagem_trusted = df_drenagem.merge(
            distr_df,
            how="left",
            left_on="nome_distrito",
            right_on="nome"
        )

        # Remove a coluna usada apenas no merge
        df_drenagem_trusted.drop(
            columns=["nome", ],
            inplace=True
        )

        return df_drenagem_trusted
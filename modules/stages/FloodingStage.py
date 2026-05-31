import pandas as pd
from modules.entities import EnumEntities
from modules.stages.IStage import IStage


class FloodingStage(IStage):

    required_entities = {
        EnumEntities.RAW_CGE_FLOODING.value,
        EnumEntities.TREATED_DISTRICTS.value
    }

    generated_entity = EnumEntities.TREATED_CGE_FLOODING.value

    def _model_data(self) -> pd.DataFrame:

        df_cge_alagamentos_raw = self.data_heap[
            EnumEntities.RAW_CGE_FLOODING.value.key
        ]

        distr_df = self.data_heap[
            EnumEntities.TREATED_DISTRICTS.value.key
        ]

        df_cge_alagamentos = df_cge_alagamentos_raw.drop(
            columns=[
                "data",
                "subprefeitura",
                "status",
                "hora_inicio",
                "hora_fim",
                "logradouro",
                "sentido",
                "referencia"
            ],
            errors="ignore"
        )[[
            "zona",
            "distrito",
            "latitude",
            "longitude",
            "dt_hr_inicio",
            "dt_hr_fim"
        ]].copy()

        df_cge_alagamentos["dt_hr_inicio"] = pd.to_datetime(
            df_cge_alagamentos["dt_hr_inicio"],
            errors="coerce"
        ).dt.strftime("%Y-%m-%dT%H:%M:%S")

        df_cge_alagamentos["dt_hr_fim"] = pd.to_datetime(
            df_cge_alagamentos["dt_hr_fim"],
            errors="coerce"
        ).dt.strftime("%Y-%m-%dT%H:%M:%S")

        # Seleciona apenas colunas necessárias do distrito
        distr_df = distr_df[[
            "id",
            "nome",
            "região",
            "lat",
            "long"
        ]].rename(columns={
            "região": "regiao"
        }).copy()

        df_cge_alagamentos_trusted = df_cge_alagamentos.merge(
            distr_df,
            how="left",
            left_on="distrito",
            right_on="nome"
        )

        # Remove coluna usada apenas no merge
        df_cge_alagamentos_trusted.drop(
            columns=["nome"],
            inplace=True
        )

        return df_cge_alagamentos_trusted
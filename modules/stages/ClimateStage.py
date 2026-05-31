import os
import pandas as pd
import requests
from requests import get
from tqdm import tqdm
import pandas as pd
from datetime import datetime
from modules.entities import EnumEntities
from modules.stages.IStage import IStage

class ClimateStage(IStage):

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive?latitude={}&longitude={}&start_date={}&end_date={}&hourly=rain"

    required_entities = {EnumEntities.TREATED_DISTRICTS.value}
    generated_entity = EnumEntities.TREATED_CLIMATE.value

    def _model_data(self) -> pd.DataFrame:
        distr_df = self.data_heap[EnumEntities.TREATED_DISTRICTS.value.key]

        start_date, end_date = self._load_dates()
        raw_climate_df = self.get_climate(start_date, end_date, distr_df)

        non_zero_records = raw_climate_df[raw_climate_df["mm_chuva"] != 0]
        return non_zero_records
        # non_zero_records["group_id"] = non_zero_records['mm_chuva'].ne(
        #     non_zero_records['mm_chuva'].shift()
        # ).cumsum()
        # agg_chuva = non_zero_records.groupby(["nome_distrito", "group_id"]).agg(
        #     dt_hr_inicio=('data_hora', 'first'), dt_hr_fim=('data_hora', 'last'), mm_chuva=('mm_chuva', 'first')
        # ).reset_index().drop(columns="group_id")
        # return agg_chuva[agg_chuva["dt_hr_inicio"] != agg_chuva["dt_hr_fim"]]

    def _load_dates(self):
        start_date = os.getenv("START_DATE")
        end_date = os.getenv("END_DATE")
        if start_date is None or end_date is None:
            raise EnvironmentError("Defina os parâmetros temporais no .env")

        DATE_FORMAT = "%d/%m/%Y"
        try:
            start_date = datetime.strptime(start_date, DATE_FORMAT)
            end_date = datetime.strptime(end_date, DATE_FORMAT)
        except ValueError:
            raise ValueError(
                f"O formato de data de \'{start_date}\' ou \'{end_date}\' não está de acordo com o padrão definido "
                f"(\'{DATE_FORMAT}\')"
            )

        return start_date, end_date

    def get_climate(self, start_date, end_date, distr_df):
        MAX_CHUNK_SIZE = 10
        raw_json_results = []

        print("\t\t\tTrabalando chunks...")
        for chunk_start in tqdm(range(0, len(distr_df), MAX_CHUNK_SIZE)):
            chunk_end = min(chunk_start + MAX_CHUNK_SIZE, len(distr_df))
            chunk = distr_df.loc[chunk_start:chunk_end]
            url = self._format_url(start_date, end_date, chunk)
            json_data = self._request_api(url)
            if json_data is None:
                continue

            for i, idx in enumerate(chunk.index):
                json_data[i]["nome_distrito"] = chunk.loc[idx, "nome"]

            raw_json_results.extend(json_data)

        raw_df = pd.json_normalize(raw_json_results)
        treated_df = raw_df.rename(columns={
            "hourly.time": "data_hora", "hourly.rain": "mm_chuva"
        })[["nome_distrito", "data_hora", "mm_chuva"]].explode(["data_hora", "mm_chuva"], ignore_index=True)
        return treated_df

    def _format_url(self, start_date, end_date, distr_df):
        lats = []
        longs = []
        for i in distr_df.index:
            lats.append(str(distr_df.loc[i, "lat"]))
            longs.append(str(distr_df.loc[i, "long"]))

        return self.BASE_URL.format(
            ",".join(lats), ",".join(longs), start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
        )

    def _request_api(self, url):
        res = get(url)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"ERRO: {e}")
            return None

        json_data = res.json()
        if isinstance(json_data, dict):
            if "error" in json_data.keys():
                raise Exception(json_data["reason"])
        return json_data

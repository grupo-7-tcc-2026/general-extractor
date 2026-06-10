import os
import requests
from requests import get
from tqdm import tqdm
import pandas as pd
from datetime import datetime
from modules.entities import EnumEntities
from modules.stages.IStage import IStage

class ClimateStage(IStage):

    BASE_URL = (
        "https://archive-api.open-meteo.com/v1/archive"
        "?latitude={}&longitude={}&start_date={}&end_date={}"
        "&hourly=rain,et0_fao_evapotranspiration,soil_temperature_0_to_7cm"
    )
    required_entities = {EnumEntities.TREATED_DISTRICTS.value}
    generated_entity = EnumEntities.TREATED_CLIMATE.value

    def _model_data(self) -> pd.DataFrame:
        distr_df = self.data_heap[EnumEntities.TREATED_DISTRICTS.value.key]

        raw_climate_df = self.get_climate(self.start_date, self.end_date, distr_df)

        non_zero_records = raw_climate_df[raw_climate_df["mm_chuva"] != 0]
        return non_zero_records

    def get_climate(self, start_date, end_date, distr_df):
        MAX_CHUNK_SIZE = 10
        raw_json_results = []

        print("\t\t\tTrabalhando chunks...")
        for chunk_start in tqdm(range(0, len(distr_df), MAX_CHUNK_SIZE)):
            chunk_end = min(chunk_start + MAX_CHUNK_SIZE, len(distr_df))
            chunk = distr_df.loc[chunk_start:chunk_end]
            url = self._format_url(start_date, end_date, chunk)
            json_data = self._request_api(url)
            if json_data is None:
                continue

            for i, idx in enumerate(chunk.index):
                json_data[i]["distrito"] = chunk.loc[idx, "nome"]

            raw_json_results.extend(json_data)

        raw_df = pd.json_normalize(raw_json_results)
        treated_df = raw_df.rename(columns={
            "hourly.time": "data_hora", "hourly.rain": "mm_chuva", "hourly.et0_fao_evapotranspiration": "mm_evaporados",
            "hourly.soil_temperature_0_to_7cm": "c_temperatura_solo"
        })[["distrito", "data_hora", "mm_chuva", "mm_evaporados", "c_temperatura_solo"]].explode([
            "data_hora", "mm_chuva", "mm_evaporados", "c_temperatura_solo"
        ], ignore_index=True)
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

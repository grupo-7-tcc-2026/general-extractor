import pandas as pd
import requests
from requests import get
from tqdm import tqdm

BASE_URL = "https://archive-api.open-meteo.com/v1/archive?latitude={}&longitude={}&start_date={}&end_date={}&hourly=rain"

def get_climate(start_date, end_date, distr_records):
    MAX_CHUNK_SIZE = 10
    raw_json_results = []

    print("\t\t\tTrabalando chunks...")
    for chunk_start in tqdm(range(0, len(distr_records), MAX_CHUNK_SIZE)):
        chunk_end = min(chunk_start + MAX_CHUNK_SIZE, len(distr_records))
        chunk = distr_records[chunk_start:chunk_end]
        url = _format_url(start_date, end_date, chunk)
        json_data = _request_api(url)
        if json_data is None:
            continue

        for i in range(len(chunk)):
            id_distr, nome_distr, regiao, _, _, _ = chunk[i]
            json_data[i]["id_distrito"] = id_distr
            json_data[i]["nome_distrito"] = nome_distr
            json_data[i]["região"] = regiao

        raw_json_results.extend(json_data)

    if not raw_json_results:
        print("\tDados vazios...")
        return None

    raw_df = pd.json_normalize(raw_json_results)
    treated_df = raw_df.rename(columns={
        "hourly.time": "data_hora", "hourly.rain": "chuva_mm"
    })[[
        "id_distrito", "nome_distrito", "região", "data_hora", "chuva_mm"
    ]].explode(["data_hora", "chuva_mm"], ignore_index=True)
    return treated_df

def _format_url(start_date, end_date, distr_records):
    lats = []
    longs = []
    for _, _, _, _, lat, long in distr_records:
        lats.append(str(lat))
        longs.append(str(long))

    return BASE_URL.format(
        ",".join(lats), ",".join(longs), start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    )

def _request_api(url):
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

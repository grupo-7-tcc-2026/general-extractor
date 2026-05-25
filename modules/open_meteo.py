import pandas as pd
from requests import get

BASE_URL = """https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=rain&start_date={}&end_date={}"""

def get_climate(start_date, end_date, distr_records):
    MAX_CHUNK_SIZE = 10
    raw_json_results = []

    for chunk_start in range(0, len(distr_records), MAX_CHUNK_SIZE):
        chunk_end = min(chunk_start + MAX_CHUNK_SIZE, len(distr_records))
        chunk = distr_records[chunk_start:chunk_end]
        url = _format_url(start_date, end_date, chunk)
        json_data = _request_api(url)

        for i in range(len(chunk)):
            id_distr, nome_distr, regiao, _, _ = chunk[i]
            json_data[i]["id_distrito"] = id_distr
            json_data[i]["nome_distrito"] = nome_distr
            json_data[i]["região"] = regiao

        raw_json_results.extend(json_data)

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
    for _, _, _, lat, long in distr_records:
        lats.append(str(lat))
        longs.append(str(long))

    return BASE_URL.format(
        ",".join(lats), ",".join(longs), start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    )

def _request_api(url):
    json_data = get(url).json()
    if isinstance(json_data, dict):
        if "error" in json_data.keys():
            raise Exception(json_data["reason"])
    return json_data

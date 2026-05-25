import pandas as pd
from requests import get

BASE_URL = """https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=rain&start_date={}&end_date={}"""

def get_climate(start_date, end_date, distr_records):
    MAX_CHUNK_SIZE = 10
    raw_json_results = []

    for chunk_start in range(0, len(distr_records), MAX_CHUNK_SIZE):
        chunk_end = min(chunk_start + MAX_CHUNK_SIZE, len(distr_records))

        a = distr_records[chunk_start:chunk_end]

        url = _format_url(
            start_date, end_date, distr_records[chunk_start:chunk_end]
        )

        json_data = _request_api(url)
        raw_json_results.extend(json_data)

    raw_df = pd.json_normalize(raw_json_results)
    pass

def _format_url(start_date, end_date, coordinate_pairs):
    lats = []
    longs = []
    for lat, long in coordinate_pairs:
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

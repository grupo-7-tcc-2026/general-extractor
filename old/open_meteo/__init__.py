import pandas as pd
from old.open_meteo import dates, open_meteo_api, rain_intervals

def extract(distr_records) -> pd.DataFrame:
    print("\tEtapa OpenMeteo")
    print("\t\tOrganizando datas do .env...")
    start_date, end_date = dates.get_dates()

    print("\t\tEnviando requisições ao OpenMeteo...")
    raw_climate_df = open_meteo_api.get_climate(start_date, end_date, distr_records)
    if raw_climate_df is None:
        return

    print("\t\tOrganizando os dados de clima obtidos...")
    trusted_climate_df = rain_intervals.generate_rain_intervals(raw_climate_df)
    print("\tEtapa concluída!\n")
    return trusted_climate_df
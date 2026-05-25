from modules import dates, districts, open_meteo, rain_intervals, persist_results
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    print("Extrator de Dados OpenMeteo")

    print("\tOrganizando datas do .env...")
    start_date, end_date = dates.get_dates()
    print("\tCarregando distritos...")
    distr_df, distr_records = districts.get_district_records()

    print("\tEnviando requisições ao OpenMeteo...")
    raw_climate_df = open_meteo.get_climate(start_date, end_date,distr_records)
    print("\tOrganizando os dados de clima obtidos...")
    trusted_climate_df = rain_intervals.generate_rain_intervals(raw_climate_df)

    print("\tGravando resultados...")
    persist_results.persist_results(distr_df, trusted_climate_df)
    print("Concluído!")

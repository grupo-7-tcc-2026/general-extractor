from modules import dates, districts, open_meteo
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    start_date, end_date = dates.get_dates()
    distr_records = districts.get_district_records()

    open_meteo.get_climate(start_date, end_date,distr_records)

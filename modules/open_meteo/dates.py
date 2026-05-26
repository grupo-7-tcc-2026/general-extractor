from datetime import datetime
import os

def get_dates() -> tuple[datetime, datetime]:
    return _load_params()

def _load_params():
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

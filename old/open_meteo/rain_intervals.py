
def generate_rain_intervals(raw_climate_df):
    non_zero_records = raw_climate_df[raw_climate_df["mm_chuva"] != 0]
    non_zero_records["group_id"] = non_zero_records['mm_chuva'].ne(non_zero_records['mm_chuva'].shift()).cumsum()
    agg_chuva = non_zero_records.groupby(['id_distrito', 'nome_distrito', 'região', "group_id"]).agg(
        dt_hr_inicio=('data_hora', 'first'), dt_hr_fim=('data_hora', 'last'), mm_chuva=('mm_chuva', 'first')
    ).reset_index()
    return agg_chuva[agg_chuva["dt_hr_inicio"] != agg_chuva["dt_hr_fim"]]

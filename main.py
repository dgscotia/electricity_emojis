import pandas as pd

gen = "generation_twh"
start = 2010
stop = 2020
years = [year for year in range(start, stop+1)]


emojis = {
    'fossils': 'F',
    'solar': 'S',
    'wind': 'W',
    'nuclear': 'N',
    'hydro': 'H',
    'biomass': 'B',
    'geo': 'G'
}


def change_dtype(x):
    try:
        return float(x)
    except:
        return x


def filter_by_country(target_country, df_func):
    filt = df_func["country_name"] == target_country
    return filt


def filter_by_year(target_year, df_func):
    filt_year = df_func["year"] == target_year
    return filt_year


def create_yearly_gen_dict(df_country, years):
    return {year: df_country[filter_by_year(year, df_country)][gen].to_dict() for year in years}


def create_country_dict(dataframe, country):
    df = dataframe[filter_by_country(country, dataframe)]
    df.set_index("fuel_code", inplace=True)
    return df


df = pd.read_csv("EER_2022_generation.csv")
df = df.apply(lambda x: change_dtype(x))

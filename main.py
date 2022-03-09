import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pywaffle import Waffle

gen = "generation_twh"
start = 2010
stop = 2021
years = [year for year in range(start, stop+1)]


def change_dtype(x):
    try:
        return float(x)
    except:
        return x


icons = pd.read_json("icons.json").columns.tolist()
with open("icons.txt", mode='w') as file:
    file.write("\n".join(icons))

icon_map = {
    'Fossils': 'gas-pump',
    'Solar': 'sun',
    'Wind': 'wind',
    'Nuclear': 'atom',
    'Hydro': 'water',
    'Bioenergy': 'leaf',
    'Other': 'temperature-high'
}

color_map = {
    'Fossils': '#7f7f7f',
    'Solar': '#ff7f0e',
    'Wind': '#17becf',
    'Nuclear': '#c5b0d5',
    'Hydro': '#1f77b4',
    'Bioenergy': '#2ca02c',
    'Other': '#d62728'
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


def create_categories(df):
    df['FOSSILS'] = df['HARDCOAL'] + df['LIGNITE'] + df['OTHFOSS'] + df['GAS']
    return df


def normalize(df):
    tot = df.sum(axis=1)
    for col in df:
        df[col] /= (tot)
        df[col] = round(df[col]*100, 2)
        df[col] - round(df[col], 0)
        #df[col] = df[col].astype(int)
    df.fillna(0, inplace=True)
    return df


def create_normalized_df(df, country):
    country_df = create_country_dict(df, country)
    gen_df = create_yearly_gen_dict(country_df, years)
    cat_df = create_categories(gen_df)
    plot_df = normalize(cat_df)
    return plot_df


def plot_frame(dataframe, country, year):
    df_plot = create_normalized_df(dataframe, country)
    data = df_plot.loc[year].sort_values(ascending=False)
    labels = data.index.tolist()
    icons_plot = [icon_map.get(label) for label in labels]
    colors_plot = [color_map.get(label) for label in labels]
    fig = plt.figure(
        FigureClass=Waffle,
        rows=10,
        values=data,

        title={
            'label': f'{country} in {year}: Electricity Production',
            'loc': 'center',
            'fontdict': {
                'fontsize': 30,
                'fontname': 'Microsoft Yi Baiti'
            }
        },
        legend={
            'labels': labels,
            'loc': 8,
            'bbox_to_anchor': (0.5, -0.1),
            'ncol': len(data),
            'framealpha': 0,
            'fontsize': 12,
        },
        icons=icons_plot,
        colors=colors_plot,
        dpi=200,
        icon_size=35,
        icon_legend=True,
        block_arranging_style='snake',
        figsize=(12, 12),
        facecolor='snow'
    )
    plt.text(0, -0.12, '@duncanmgibb', fontsize=15,
             fontfamily='Microsoft Yi Baiti', color='#7f7f7f')
    plt.savefig(f"exported/{country}_{year}")
    plt.show()


def plot_all_countries(data, country_list):
    for country in country_list:
        plot_frame(data, country, 2021)


def run():
    df = pd.read_csv("EER_2022_generation.csv")
    df = df.apply(lambda x: change_dtype(x))
    countries = df['country_name'].unique().tolist()
    plot_all_countries(df, countries)


if __name__ == "__main__":
    run()

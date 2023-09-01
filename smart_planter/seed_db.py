# import pandas to read the excel file
# note:  We need to install xlrd and openpyxl as well (pip install xlrd openpyxl)
import pandas as pd

from planter import app
from planter.models import Plant, db


def seed_db_with_plants_info(data_path):
    # read the df
    df = pd.read_excel(data_path, sheet_name='plants_data')

    # rename the pandas df columns to map directly to the database model
    col_names = {'Name:': 'name', 'Scientific Name:': 'scientific_name', 'Description:': 'description', 'Soil:': 'soil',
                 'Water:': 'water', 'Sunlight Requirements:':  'sunlight_requirements', 'Minimum cold hardiness:': 'minimum_cold_hardiness'}

    # perform the renaming
    df.rename(columns=col_names, inplace=True)

    with app.app_context():
        # now saveing the dataframe to the database
        for index in df.index:
            plant = {}
            plant['name'] = df['name'][index]
            plant['scientific_name'] = df['scientific_name'][index]
            plant['description'] = df['description'][index]
            plant['soil'] = df['soil'][index]
            plant['water'] = df['water'][index]
            plant['sunlight_requirements'] = df['sunlight_requirements'][index]
            plant['minimum_cold_hardiness'] = df['minimum_cold_hardiness'][index]

            try:
                new_plant = Plant(**plant)
                db.session.add(new_plant)
                db.session.commit()
            except Exception as exception:
                print(f'Error occurred adding a new plant: {exception}')
                continue


if __name__ == "__main__":
    DATA_PATH = './data/plants_data.xlsx'
    seed_db_with_plants_info(data_path=DATA_PATH)

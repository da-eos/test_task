import pandas as pd
import numpy as np
from .dictionaries import *

# data set openning

# google sheet data
sheet_id = '12o1iofQx6V-UhInjUjLjpKxx3Z8ve8EGxnQtzNioIv4'
sheet_name = 'Sheet1'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
row_data = pd.read_csv(url)
df = row_data.copy()

## cleanning & formatting
seasons = {
    1:'winter',
    2:'spring',
    3:'summer',
    4:'fall'
}
missing_data = df.isna().sum()
df['CLAIM_SPECIALTY'] = df['CLAIM_SPECIALTY'].str.capitalize()
df['CLAIM_SPECIALTY'] = df['CLAIM_SPECIALTY'].fillna(df['CLAIM_SPECIALTY'].mode().values[0])
df.loc[df['MONTH'] == 201900, 'MONTH'] = 201901
df['DATE'] = pd.to_datetime(df['MONTH'].astype('str'), format = '%Y%m')
df['PAYER'] = df['PAYER'].apply(lambda x : x.split('Payer')[-1].strip())
df['YEAR'] = df['DATE'].dt.year
df['MONTH'] = df['DATE'].dt.month
df['DATE'] = df['DATE'].astype('str')
df['SEASON'] = df['MONTH'] % 12 // 3 + 1
df['SEASON'] = df['SEASON'].apply(lambda x: seasons[x])
df = df[['DATE', 'YEAR', 'MONTH','SEASON', 'SERVICE_CATEGORY', 'CLAIM_SPECIALTY', 'PAYER', 'PAID_AMOUNT']]
df.columns = [col.lower() for col in df.columns]
df['claim_type'] = np.where(df['paid_amount'] < 0, 'refund', 'paid')

# applying departments

for service in medical_services:
    df.loc[df['service_category'].isin(medical_services[service]), 'department'] = service

# applying new category
for terms in [terms_dict_A, terms_dict_BC, terms_dict_D, terms_dict_E, terms_dict_F, terms_dict_G, terms_dict_H,
            terms_dict_I, terms_dict_L, terms_dict_M, terms_dict_N, terms_dict_O, terms_dict_P, terms_dict_R,terms_dict_S,
            terms_dict_T,terms_dict_UVWX,terms_dict_LAST]:
    for key in terms:
        df.loc[df['claim_specialty'].isin(terms[key]), 'new_specialty'] = key

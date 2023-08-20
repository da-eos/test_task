import streamlit as st
from data_tools.data_prep import (df, 
                                  missing_data)

st.markdown("# Data Pre Processing ")
st.sidebar.markdown("# Data Pre Processing")

st.markdown(
"""
## Dataframe info

"""
)

st.markdown(
"""
```RangeIndex: 52152 entries

Data columns (total 5 columns):

     Column            Non-Null Count  Dtype

 0   MONTH             52152 non-null  int64 
 
 1   SERVICE_CATEGORY  52152 non-null  objectpip
 
 2   CLAIM_SPECIALTY   51901 non-null  object
 
 3   PAYER             52152 non-null  object

 4   PAID_AMOUNT       52152 non-null  int64 

dtypes: int64(2), object(3)

memory usage: 2.0+ MB
"""
)

st.markdown(
"""
## Missing values

Let's look at the missing values and try to manage with them:
"""
)
st.code('df.isna().sum(axis = 0)')

st.write(
    missing_data
)

st.markdown(
"""
Obviously CLAIM_SPECIALTY has 251 missing values but how much them in percentage
"""
)

st.code('round(df.isna().sum(axis = 0).sum() / df.shape[0] * 100, 2)')
st.write(
    f'The percent of missing values is: {round(missing_data.sum() / df.shape[0] * 100, 2)}%'
)

st.markdown("**CONCLUSION: we can fill this values with most common(mode) value because of small percentage.**")


st.markdown(
"""
## Types management

As we can see in the type of column MONTH is int64, so let's retype it to datetime.

- Also there are a wrong data values like `201900` which affected 11 rows.

- In case that `201900` goes after `201812`, probably `201900` related to `201901`. So let's put `201901` values instead of `201900`.
"""
)

st.code(
    "df.loc[df['MONTH'] == 201900, 'MONTH'] = 201901"
)

st.markdown(
    'Than we can convert the MONTH int64 into datetime'
)

st.code(
    "df['DATE'] = pd.to_datetime(df['MONTH'].astype('str'), format = '%Y%m')"
)

st.markdown(
"""
Now let's check the date range it should be equal to 2018/01 - 2020/07
"""
)

st.code(
    "df['MONTH'].min(), df['MONTH'].max()"
)

st.markdown(
"""
**(201801, 202007)**

Great, that what we expected

## Additional columns & cleanning

And also let's
- separate year, month and season columns they will help with forecasting later.
- remake CLAIM_SPECIALTY in one capitalize format because of differencies like ('INTERNAL MEDICINE', 'Internal Medicine').
- regroup CLAIM_SPECIALTY to more clear categories instead of this abreviatures nigtmare, using ChatGPT PLUS, chat created dictionaries for me.
- regroup services as well.
- transform all column names into a lower case.
- add additional columns which split refunds and paids.
- exclude word Payer from column PAYER, because it's in a every row, so we can get rid of this word and remain only abreviatures.

"""
)

st.code(
"""
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

"""
)

st.markdown(
"""
Let's check dublicates
"""
)
st.code(
'df.duplicated().sum() -> 0'
)

st.markdown(
"""
Sample of new dataframe:
"""
)
st.dataframe(
    df.head(), hide_index=True
)


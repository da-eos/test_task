import seaborn as sns
import matplotlib.pyplot as plt
from .data_prep import df
from plotly import express as px


def multi_filter_option(data, column, options):
    filterred = data[data[column].isin(options)]
    return filterred

def filter_by_year(data, option):
    return data[data['year'] == option]

def filter_by_claim(data, option):
    if 'paid' in option:
        return data[data['claim_type'] == option].nlargest(10, 'paid_amount')
    else:
        return data[data['claim_type'] == option].nsmallest(10, 'paid_amount')



def get_bar_figure(data, title,height, **kwargs):
    data.sort_values(by = kwargs['y'])
    fig = px.bar(
        data,
        x = kwargs['x'],
        y = kwargs['y'],
        color = kwargs['color'],
        text = kwargs['y'],
        title = title,
        barmode='group',
        labels = kwargs['labels'])
    fig.update_layout(height = height)
    fig.update_traces(textposition='outside', textfont_size=20)
    return fig

def get_boxplot_figure(data, title, height, **kwargs):
    fig = px.box(
        data,
        x = kwargs['x'],
        y = kwargs['y'],
        title=title,
        color = kwargs['color'],
        labels = kwargs['labels'],
    )
    fig.update_layout(height=height)
    fig.update_traces(quartilemethod="exclusive")
    return fig

## FIG average paids in year by servises

most_pays_service = df.groupby(['year',
                                'department',
                                'claim_type'])\
                                .agg({'paid_amount':'mean'})\
                                .reset_index()\
                                .sort_values(by = 'paid_amount')
most_pays_service['year'] = most_pays_service['year'].astype('str')
most_pays_service['paid_amount'] = most_pays_service['paid_amount'].round(1)

## FIG average paids in year by categories

most_pays_catg = df.groupby(['year',
                                'new_specialty',
                                'claim_type'])\
                                .agg({'paid_amount':'mean'})\
                                .reset_index()\
                                .sort_values(by = ['year', 'paid_amount'])
most_pays_catg['year'] = most_pays_catg['year'].astype('str')
most_pays_catg['paid_amount'] = most_pays_catg['paid_amount'].round(1)
most_pays_catg = most_pays_catg[most_pays_catg['new_specialty'] != 'Others']


## FIG average paids in year by ins.comp
most_pays_company = df.groupby(['year',
                                'payer',
                                'claim_type'])\
                                .agg({'paid_amount':'mean'})\
                                .reset_index()\
                                .sort_values(by = ['year','paid_amount'])
most_pays_company['year'] = most_pays_company['year'].astype('str')
most_pays_company['paid_amount'] = most_pays_company['paid_amount'].round(1)


## FIG average paids in month by servises
months = {
    1:'Jan',
    2:'Feb',
    3:'Mar',
    4:'Apr',
    5:'May',
    6:'Jun',
    7:'Jul',
    8:'Aug',
    9:'Sep',
    10:'Oct',
    11:'Nov',
    12:'Dec'
}
most_pays_service_mom = df.groupby(['year',
                                    'month',
                                'department',
                                'claim_type'])\
                                .agg({'paid_amount':'mean'})\
                                .reset_index()\
                                .sort_values(by = 'paid_amount')
most_pays_service_mom['year'] = most_pays_service_mom['year'].astype('str')
most_pays_service_mom['month_name'] = most_pays_service_mom['month'].apply(lambda x: months[x])
most_pays_service_mom.sort_values(by='month', inplace=True)
most_pays_service_mom['paid_amount'] = most_pays_service_mom['paid_amount'].round(1)


## FIG average paids in month by specialty

most_pays_spec_mom = df.groupby(['year',
                                    'month',
                                'new_specialty',
                                'claim_type'])\
                                .agg({'paid_amount':'mean'})\
                                .reset_index()\
                                .sort_values(by = 'paid_amount')
most_pays_spec_mom['year'] = most_pays_spec_mom['year'].astype('str')
most_pays_spec_mom = most_pays_spec_mom[most_pays_spec_mom['new_specialty'] != 'Others']
most_pays_spec_mom['month_name'] = most_pays_spec_mom['month'].apply(lambda x: months[x])
most_pays_spec_mom.sort_values(by='month', inplace=True)
most_pays_spec_mom['paid_amount'] = most_pays_spec_mom['paid_amount'].round(1)


## FIG average paids in month by ins.comp
most_pays_company_mom = df.groupby(['year',
                                'month',
                                'payer',
                                'claim_type'])\
                                .agg({'paid_amount':'mean'})\
                                .reset_index()\
                                .sort_values(by = ['year','paid_amount'])
most_pays_company_mom['year'] = most_pays_company_mom['year'].astype('str')
most_pays_company_mom['paid_amount'] = most_pays_company_mom['paid_amount'].round(1)
most_pays_company_mom['month_name'] = most_pays_company_mom['month'].apply(lambda x: months[x])
most_pays_company_mom.sort_values(by='month', inplace=True)


## FIG CORRELATION BETWEEN MONTH AND CALIMS
colors = sns.color_palette()
corr_mc = df.copy()
corr_mc = corr_mc[['year','month', 'paid_amount']]
fig_corr = plt.figure(
    figsize=(10,5)
    )
plt.title('Correlation of numerous data')
sns.heatmap(corr_mc.corr(), annot=True)


# SERIES FIGURES

series_data = df.copy()
series_fig = plt.figure(
    figsize=(15,5)
)
plt.title('Line chart of claims amount from 2018 to 2020')
plt.xticks(rotation = 60)
plt.xlabel('Date')
plt.ylabel('Amount of claims')
sns.lineplot(
    data = series_data,
    x = 'date',
    y = 'paid_amount',
    color = colors[5]
)

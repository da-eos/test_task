import plotly.express as px
import streamlit as st
from data_tools.charts_tools import (most_pays_service,
                                     most_pays_catg,
                                     most_pays_company,
                                     multi_filter_option,
                                    get_bar_figure,
                                    filter_by_claim,
                                    filter_by_year)

st.markdown("# Exploratory Data Analysis | YearOverYear")

st.sidebar.markdown("[Departments more paid/refund](#section2)")
st.sidebar.markdown("[TOP10 Categories](#section3)")
st.sidebar.markdown("[Payments & Refunds based on insurance company](#section4)")

st.header('In what department were more paid or refunded services in average?', anchor='section2')
st.markdown(
"""
Let's have a look which particular department has a biggest amount of payments in average YoY

**You can choose different department, year and claim types to see the year refunded or paid AVG value**
"""
)

# Filter Columns
filter_year, filter_claim = st.columns(2)

with filter_year:
    years = list(most_pays_service['year'].unique())
    year_options = st.multiselect(
    'Choose year:',
    years,
    [years[0]], key = 'most_pays_service_1')

with filter_claim:
    claims = list(most_pays_service['claim_type'].unique())
    claim_options = st.multiselect(
    'Choose a claim type:',
    claims,
    claims, key = 'most_pays_service_2')


deps = list(most_pays_service['department'].unique())
department_options = st.multiselect(
        'Choose department:',
        deps,
        deps)


data_avg_serv = multi_filter_option(most_pays_service,'year', year_options)
data_avg_serv = multi_filter_option(data_avg_serv, 'claim_type',claim_options)
data_avg_serv = multi_filter_option(data_avg_serv, 'department', department_options)


# AVG PAIDS BY YEAR SERVICES
fig_avg_paid_year = get_bar_figure(
    data_avg_serv, height=700,
    title="AVG values of department's refund / paid amount by years",
    **{
        'x' : 'year',
        'y':'paid_amount',
        'color':'department',
        'text':'paid_amount',
        'labels': {
                   'paid_amount': 'AVG Paids or Refund amount',
                    'year':'Year',
                    'department':'Department'}
    })
fig_avg_paid_year.update_layout(xaxis = {
    'tickmode':'linear',
    'dtick':1
})

st.plotly_chart(fig_avg_paid_year,
                use_container_width=True)

# ['OutpatientServices', 'InpatientServices', 'ERServices', 'AncillaryFFS', 'PCPEncounter', 'SNFServices', 'SpecialistFFS', 'ASCServices', 'PCPFFS', 'SpecialistsFFS']

st.header('In what categories were more paid or refunded services in average in year(TOP 10 only)?', anchor = 'section3')

# Filter Columns
filter_year, filter_claim = st.columns(2)

with filter_year:
    years = list(most_pays_catg['year'].unique())
    year_options = st.selectbox(
    'Choose year:',
    tuple(years),
    key = 'most_pays_catg_1')
    data_avg_catg = filter_by_year(most_pays_catg, year_options)


with filter_claim:
    claims = list(most_pays_catg['claim_type'].unique())
    claim_options = st.selectbox(
    'Choose a claim type:',
    tuple(claims),
    key = 'most_pays_catg_2')
    data_avg_catg = filter_by_claim(data_avg_catg, claim_options)


specs = list(data_avg_catg['new_specialty'].unique())
specs_options = st.multiselect(
        'Choose speciatly:',
        specs,
        specs)


data_avg_catg = multi_filter_option(data_avg_catg, 'new_specialty', specs_options)


# AVG PAIDS BY YEAR CATEGORIES
fig_avg_paid_year_catg = get_bar_figure(
    data_avg_catg, height=700,
    title="AVG values of specialty's refund / paid amount by years",
    **{
        'x' : 'year',
        'y':'paid_amount',
        'color':'new_specialty',
        'text':'paid_amount',
        'labels': {
                   'paid_amount': 'AVG Paids or Refund amount',
                    'year':'Year',
                    'new_specialty':'Specialty'}
    })
fig_avg_paid_year_catg.update_layout(xaxis = {
    'tickmode':'linear',
    'dtick':1
})

st.plotly_chart(fig_avg_paid_year_catg)


st.header('Which company did more payments or refunds in average YoY?', anchor='section4')


filter_year, filter_claim = st.columns(2)

with filter_year:
    years = list(most_pays_company['year'].unique())
    year_options = st.multiselect(
    'Choose year:',
    years,
    [years[0]],
    key = 'most_pays_company_1')


with filter_claim:
    claims = list(most_pays_company['claim_type'].unique())
    claim_options = st.multiselect(
    'Choose a claim type:',
    claims,
    claims,
    key = 'most_pays_company_2')


comps = list(most_pays_company['payer'].unique())
comps_options = st.multiselect(
        'Choose company:',
        comps,
        comps)


comp_data = multi_filter_option(most_pays_company, 'year', year_options)
comp_data = multi_filter_option(comp_data, 'claim_type', claim_options)
comp_data = multi_filter_option(comp_data, 'payer', comps_options)

# AVG PAIDS BY YEAR COMPANIES
fig_avg_paid_year_companies = get_bar_figure(
    comp_data, height=700,
    title="AVG values of insurance company's refund / paid amount by years",
    **{
        'x' : 'year',
        'y':'paid_amount',
        'color':'payer',
        'text':'paid_amount',
        'labels': {
                   'paid_amount': 'AVG Paids or Refund amount',
                    'year':'Year',
                    'payer':'Company'}
    })
fig_avg_paid_year_companies.update_layout(xaxis = {
    'tickmode':'linear',
    'dtick':1
})

st.plotly_chart(fig_avg_paid_year_companies)

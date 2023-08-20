from audioop import mul
import plotly.express as px
import streamlit as st
from data_tools.charts_tools import (most_pays_service_mom,
                                     most_pays_spec_mom,
                                     most_pays_company_mom,
                                     multi_filter_option,
                                     filter_by_year,
                                    get_boxplot_figure,
                                    fig_corr)


st.markdown("# Exploratory Data Analysis | MonthOverMonth")

st.sidebar.markdown("[Departments more paid/refund](#section2)")
st.sidebar.markdown("[Claim amounts in category](#section3)")
st.sidebar.markdown("[Claims amounts by insurance company](#section4)")
st.sidebar.markdown("[Corrlelations](#section5)")

st.header('In what department were more paid or refunded services in average?', anchor='section2')
st.markdown(
"""
**You can choose different department, year, month and claim types to see the year refunded or paid AVG value**

If you don't see department in the chart that means, that probably in partucular year there is only one value.
"""
)

# Filter Columns
filter_year, filter_month = st.columns(2)

with filter_year:
    years = list(most_pays_service_mom['year'].unique())
    year_options = st.selectbox(
    'Choose year:',
    tuple(years),
    key = 'most_pays_service_mom_1')

with filter_month:
    months = list(most_pays_service_mom['month_name'].unique())
    months_options = st.multiselect(
    'Choose month:',
    months,
    months,
    key = 'most_pays_service_mom_2')

deps = list(most_pays_service_mom['department'].unique())
department_options = st.multiselect(
        'Choose department:',
        deps,
        deps,
        key= 'most_pays_service_mom_4')

#filters
mps_mom = filter_by_year(most_pays_service_mom,  year_options)
mps_mom = multi_filter_option(most_pays_service_mom, 'month_name', months_options)
mps_mom = multi_filter_option(mps_mom, 'department', department_options)

table_view, chart_view = st.tabs(['Table View', 'Box Plot View'])



# TABLE VIEW
with table_view:
    st.dataframe(
    mps_mom.style\
        .highlight_min(subset=['paid_amount'], axis=0, color = 'red')\
        .highlight_max(subset=['paid_amount'], axis=0), hide_index=True
    )
with chart_view:
    # FIG VIEW BOX BY DEPS MOM
    fig_avg_paid_mom = get_boxplot_figure(
    mps_mom,
    f'Distribution of claim amount values',
    height=700,
    **{
        'x':'month_name',
        'y':'paid_amount',
        'color':'department',
        'labels':{
            'paid_amount':'Distribution of month values',
            'month_name':'Month',
            'department':'department'
        }
    }
)
    st.plotly_chart(fig_avg_paid_mom)


st.header('What is claim amount distribution in a particular category?', anchor = 'section3')

# Filter Columns
filter_year, filter_month = st.columns(2)

with filter_year:
    years = list(most_pays_spec_mom['year'].unique())
    year_options = st.selectbox(
    'Choose year:',
    tuple(years),
    key = 'most_pays_spec_mom_1')

with filter_month:
    months = list(most_pays_spec_mom['month_name'].unique())
    months_options = st.multiselect(
    'Choose month:',
    months,
    months,
    key = 'most_pays_spec_mom_2')

st.markdown(
"""
Accroding to a wide range of categories, please choose any of your choice to compare.
"""
)
specs = list(most_pays_spec_mom['new_specialty'].unique())
specs_options = st.multiselect(
        'Choose specialty(first 5 is default value):',
        specs,
        specs[5:11],
        key= 'most_pays_spec_mom_4')

mpss_mom = filter_by_year(most_pays_spec_mom, year_options)
mpss_mom = multi_filter_option(mpss_mom, 'month_name', months_options)
mpss_mom = multi_filter_option(mpss_mom, 'new_specialty', specs_options)

fig_avg_spec_mom = get_boxplot_figure(
    mpss_mom,
    title=f'Distribution of paid_amount values in {year_options}',
    height=700,
    **dict(
        x = 'month_name',
        y = 'paid_amount',
        color = 'new_specialty',
        labels = dict(
            month_name = 'Month',
            new_specialty = 'Specialty',
            paid_amount = 'Distribution of AVG values'
        )
    )
)

st.plotly_chart(fig_avg_spec_mom,
                use_container_width=True)


st.header('What is a claim amount distribution in a particular company?', anchor = 'section4')


# Filter Columns
filter_year, filter_month = st.columns(2)

with filter_year:
    years = list(most_pays_company_mom['year'].unique())
    year_options = st.selectbox(
    'Choose year:',
    tuple(years),
    key = 'most_pays_company_mom_1')

with filter_month:
    months = list(most_pays_company_mom['month_name'].unique())
    months_options = st.multiselect(
    'Choose month:',
    months,
    months,
    key = 'most_pays_company_mom_2')

comps = list(most_pays_company_mom['payer'].unique())
comps_options = st.multiselect(
        'Choose company:',
        comps,
        comps,
        key= 'most_pays_company_mom_4')

data_comps = filter_by_year(most_pays_company_mom,year_options)
data_comps = multi_filter_option(data_comps, 'month_name', months_options)
data_comps = multi_filter_option(data_comps, 'payer', comps_options)


fig_avg_comp_mom = get_boxplot_figure(
    data_comps,
    'Distribution of average claims amounts',
    height=700,
    **dict(
        x = 'month_name',
        y = 'paid_amount',
        color = 'payer',
        labels = dict(
            paid_amount = 'Distribution of claim amount',
            month_name = 'Month',
            payer = 'Insurance Company'
        )
    )
)

st.plotly_chart(fig_avg_comp_mom,
                use_container_width=True)


st.header('Is there any correlations?', anchor = 'section5')

st.pyplot(fig_corr, clear_figure=True)

st.markdown(
"""
Obviously that there is not any correlations between year and paid_amount as well as month with paid_amount
"""
    )
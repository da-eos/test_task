from stat import FILE_ATTRIBUTE_READONLY
import streamlit as st
from data_tools.charts_tools import series_data, series_fig
from data_tools.model_tools import (filter_data_before_fit,
                                    fit_predict_plot)


st.header("Time series forecasting using Facebook model Prophet", anchor = 'section1')
st.sidebar.markdown("[Time series FCST](#section1)")
st.sidebar.markdown("[Predict N future periods](#section2)")
st.markdown(
"""
Firstly lets have a look on time series chart.            
""")

st.pyplot(
    series_fig
)

st.markdown(
"""
## Adding features

In previous steps I added some features for Time Series analysis ['season', 'month', 'year']

Now our dataset looks:

"""
)
st.dataframe(series_data.head(5),hide_index = True)



st.header('Predict next N future periods', anchor= 'section2')

st.markdown(
"""
Let's prdict some trends related to specific parameters using Prophet forecasting model

Choose: `N periods`, `company`, `service`, `specialty` -> to get future trend prediction.

It can be ValueError: Dataframe has no rows, if your parameters are without data.
"""
)

n_days, company = st.columns(2)
service, specialty = st.columns(2)

with n_days:
    number = st.number_input("How much month you want to predict(default 6 month)?",
                    value = 6,
                    min_value=3,
                    max_value=24,
                    key='n_number')

with company:
    company_option = st.selectbox(
        "Choose the company:",
        tuple(series_data['payer'].unique())
    )


with service:
    serv_option = st.selectbox(
        "Choose service category:",
        tuple(series_data['service_category'].unique())
    )

with specialty:
    spec_option = st.selectbox(
        "Choose specialty:",
        tuple(series_data['new_specialty'].unique())
    )

filtered_df = filter_data_before_fit(series_data, company_option, serv_option, spec_option)
mae, maep, history_fig, future_fig = fit_predict_plot(filtered_df,
                                                     number)


st.markdown(
f"""
### Metrics of prediction

Mean Absolute Error: `{round(mae,1)}`

Mean Absolute Percentage Error: `{round(maep, 2)}`%

Predicted chart for

Specialty: {spec_option}

Company: {company_option}

Service category: {serv_option}
"""
)


st.plotly_chart(
    history_fig
)

st.plotly_chart(
    future_fig
)
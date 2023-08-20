from .data_prep import df, pd
from .charts_tools import  px
from sklearn.metrics import (mean_absolute_error,
                             mean_absolute_percentage_error)
from prophet import Prophet
from prophet.plot import plot_plotly



def filter_data_before_fit(data, company, service, specialty):
    company_filtered = data[data['payer'] == company]
    service_filtered = company_filtered[company_filtered['service_category'] == service]
    spec_filtered = service_filtered[service_filtered['new_specialty'] == specialty]
    to_fit = spec_filtered.rename(columns={
        'date':'ds',
        'paid_amount':'y'
    })
    return to_fit

def fit_predict_plot(to_fit_data, predict_n):
    model = Prophet()
    to_fit_data.dropna(inplace=True)
    model.fit(to_fit_data)
    pred_values = model.predict(to_fit_data)
    mae = mean_absolute_error(to_fit_data['y'], pred_values['yhat'])
    maep = mean_absolute_percentage_error(to_fit_data['y'], pred_values['yhat'])
    future_dates = model.make_future_dataframe(periods = predict_n, freq='m', include_history = False)
    future_data = model.predict(future_dates)
    history_fig = plot_plotly(model, pred_values, trend = True)
    future_fig = plot_plotly(model, future_data, trend = True)
    return mae, maep, history_fig, future_fig


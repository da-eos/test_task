import streamlit as st
from data_tools.data_prep import row_data

st.markdown(
"""
# EDA Challenge | Sxope


## Task descritption
            
In this exercise, you are given a dataset with claims data.
You need to perform an Exploratory Data Analysis and present your results to business users (e.g. interactive dashboard, notebook, or some other tool of your choice).
Business users are interested to see trends and anomalies in the data as well as projections for the upcoming 6 months.

## Dataset example

""")

st.write(row_data.head())

st.markdown(
"""
This dataset is a sampled aggregated data for the period of 2018/01 - 2020/07 (numbers are fictional). 

The dataset contains the following columns:

1. **MONTH** - a month claims were lodged

2. **SERVICE_CATEGORY** - a department that provided services to patients

3. **CLAIM_SPECIALTY** - a type of medical services by an official classification system

4. **PAYER** - an insurance company

5. **PAID_AMOUNT** - sum of expenses (claims), $

[A link to Dataset google sheet](https://docs.google.com/spreadsheets/d/12o1iofQx6V-UhInjUjLjpKxx3Z8ve8EGxnQtzNioIv4/edit?usp=sharing)
"""
)

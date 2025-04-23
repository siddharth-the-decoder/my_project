import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns 
import altair as alt
from UI import *
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Page layout
st.set_page_config(page_title="Analytics", page_icon="🌎", layout="wide")

# Theme
theme_plotly = None 

# Load CSS style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

UI()

# Load dataset
df = pd.read_csv('data.csv')

# Sidebar
st.sidebar.image("images/logo2.png")
with st.sidebar:
    st.title("Select Date Range")
    start_date = st.date_input(label="Start Date")
    end_date = st.date_input(label="End Date")

st.error("Business Metrics between [" + str(start_date) + "] and [" + str(end_date) + "]")

# Filter dataset by date range
df2 = df[(pd.to_datetime(df['OrderDate'], dayfirst=True) >= pd.to_datetime(start_date)) &
         (pd.to_datetime(df['OrderDate'], dayfirst=True) <= pd.to_datetime(end_date))]

# Filter explorer
with st.expander("Filter Excel Dataset"):
    filtered_df = dataframe_explorer(df2, case=False)
    st.dataframe(filtered_df, use_container_width=True)

# Charts and metrics
b1, b2 = st.columns(2)

# Bar chart
with b1:
    st.subheader('Products & Quantities', divider='rainbow')
    bar_chart = alt.Chart(df2).mark_bar().encode(
        x=alt.X("Quantity:Q"),
        y=alt.Y("Product:N", sort='-x')
    ).interactive()
    st.altair_chart(bar_chart, use_container_width=True, theme=theme_plotly)

# Metrics
with b2:
    st.subheader('Dataset Metrics', divider='rainbow')
    from streamlit_extras.metric_cards import style_metric_cards

    col1, col2 = st.columns(2)
    col1.metric(label="All Inventory Products", value=df2.Product.count(), delta="Number of Items in stock")
    col2.metric(label="Sum of Product Price USD", value=f"{df2.TotalPrice.sum():,.0f}", delta=df2.TotalPrice.median())

    col11, col22, col33 = st.columns(3)
    col11.metric(label="Maximum Price USD", value=f"{df2.TotalPrice.max():,.0f}", delta="High Price")
    col22.metric(label="Minimum Price USD", value=f"{df2.TotalPrice.min():,.0f}", delta="Low Price")
    col33.metric(label="Total Price Range USD", value=f"{df2.TotalPrice.max() - df2.TotalPrice.min():,.0f}", delta="Price Range")

    style_metric_cards(background_color="#596073", border_left_color="#F71938", border_color="#1f66bd", box_shadow="#F71938")

# Dot plot
a1, a2 = st.columns(2)
with a1:
    st.subheader('Products & Total Price', divider='rainbow')
    chart = alt.Chart(df2).mark_circle().encode(
        x=alt.X('Product:N'),
        y=alt.Y('TotalPrice:Q'),
        color=alt.Color('Category:N')
    ).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)

with a2:
    st.subheader('Products & Unit Price', divider='rainbow')
    bar_chart = alt.Chart(df2).mark_bar().encode(
        x=alt.X("month(OrderDate):O"),
        y=alt.Y("sum(UnitPrice):Q"),
        color=alt.Color("Product:N")
    ).interactive()
    st.altair_chart(bar_chart, use_container_width=True, theme=theme_plotly)

# Scatter plot and histogram
p1, p2 = st.columns(2)

with p1:
    st.subheader('Features by Frequency', divider='rainbow')
    feature_x = st.selectbox('Select feature for x Qualitative data', df2.select_dtypes("object").columns)
    feature_y = st.selectbox('Select feature for y Quantitative Data', df2.select_dtypes("number").columns)

    fig, ax = plt.subplots()
    sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue=df2.Product, ax=ax)
    st.pyplot(fig)

with p2:
    st.subheader('Features by Frequency', divider='rainbow')
    feature = st.selectbox('Select a feature', df2.select_dtypes("object").columns)

    fig, ax = plt.subplots()
    ax.hist(df2[feature], bins=20)
    ax.set_title(f'Histogram of {feature}')
    ax.set_xlabel(feature)
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

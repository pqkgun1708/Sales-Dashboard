import pandas as pd
import streamlit as st
import plotly_express as px

# set streamlit web 
st.set_page_config(page_title='Sales Dashboard', 
                   page_icon=":star:",
                   layout='wide')  # set page name


# we read data from the 4th row and from columns B to R in the excel file
@st.cache
def get_data_from_excel():
    df = pd.read_excel(io='supermarkt_sales.xlsx', skiprows=3, usecols='B:R') 
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df


df = get_data_from_excel()

 
# -------------SIDEBAR-------------
# Header
st.sidebar.header("Filter")
# City
city = st.sidebar.multiselect(
    'City :',
    options=df['City'].unique(),
    default=df['City'].unique()
)
# Customer
customer_type = st.sidebar.multiselect(
    'Customer type :',
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)
# Gender
gender = st.sidebar.multiselect(
    'Gender :',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)
# find data base on filter information
df_selection = df.query(
    'City == @city & Customer_type == @customer_type & Gender == @gender'
)
# print filter data
st.dataframe(df_selection.head(10))

# -------------MAINPAGE-------------
st.title(':bar_chart: Sales Dashboard')
st.markdown('##')
# Display top KPI
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection['Total'].mean(), 2)

left_col, middle_col, right_col = st.columns(3)
with left_col:
    st.subheader('Total sales :')
    st.subheader(f'{total_sales:,} $')
with middle_col:
    st.subheader('Average rating :')
    st.subheader(f'{average_rating} {star_rating}')
with right_col:
    st.subheader('Average Sales Per Transaction :')
    st.subheader(f'{average_sale_by_transaction} $')

st.markdown('---')

# SALES BY PRODUCT LINE
sales_by_product_line = (
    df_selection.groupby(by=['Product line']).sum()[['Total']].sort_values(by='Total')
)
fig_product = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation='h',
    title='<b>Sales by Product Line</b>',
    color_discrete_sequence=['#0083B8'] * len(sales_by_product_line),
    template='plotly_white'
)
fig_product.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR
sales_by_hour = df_selection.groupby(by=['Hour']).sum()[['Total']]
fig_hour = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y='Total',
    title='<b>Sales By Hour </b>',
    color_discrete_sequence=['#0083B8'] * len(sales_by_hour),
    template='plotly_white'
)
fig_hour.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=False))
)

# print 2 chart on left, right
left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_hour, use_container_width=True)
right_col.plotly_chart(fig_product, use_container_width=True)

# Styling the page
hide_st_style = '''
    <style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)
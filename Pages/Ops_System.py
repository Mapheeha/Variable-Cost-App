from anyio import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
from sklearn import preprocessing
from utils import *
from dictionaries import *
from PIL import Image
from streamlit_option_menu import option_menu

st.set_page_config(layout = "wide", page_icon = "chart_with_upwards_trend", page_title="Welcome To Mafube Variable Cost Models")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#st.markdown("<h1 style='text-align: center; color: black;'>Welcome To Variable Cost Models  👋</h1>", unsafe_allow_html=True)

from streamlit_lottie import st_lottie  # pip install streamlit-lottie
import json
import requests


# for a web-based lottie, use the following statements
vFile = "https://assets5.lottiefiles.com/packages/lf20_ft6xCqcC4s.json"
r = requests.get(vFile)
LottieCode = None if r.status_code != 200 else r.json()

#--------------------show the lottie file in the sidebar
try:
    with st.sidebar:
        st_lottie(LottieCode, height=200, width=200, speed=1, loop=True)
except:
    pass



#st.set_page_config(layout = "wide", page_icon = 'logo.png', page_title='Variable Cost Model')
#st.set_page_config(layout = "wide", page_icon = "chart_with_upwards_trend", page_title="Welcome To Variable Cost Models")

#image = Image.open(r"C:\Users\mapheeha.chauke\OneDrive - Exxaro\Desktop\EXXARO\Example\exxaro.jpg")
#st.markdown(image, unsafe_allow_html=True)
#st.image(image)


BU = "Mafube"


analysis = st.sidebar.multiselect(
    "Choose the Analysis to Display",
    ("Prediction Results", "Exploratory Analysis","Variables Prediction")
    )

df = get_data(datasets[BU])


#TTH_input = st.sidebar.number_input('Enter Current TTH volume (Ton)')

st.markdown("<h1 style='text-align: center; color: black;'>Welcome To Mafube Variable Cost Models 👋</h1>", unsafe_allow_html=True)
#st.header("Variable Cost Model")

st.write('Displaying results for ', BU)

if "Prediction Results" in analysis:
     st.subheader("Predictive Model Results")
     with st.sidebar:
          selected2 = option_menu("Select the Variable of Interest",["Diesel", "Explosives", "Magnetite","Maintenance","Energy_Price","Energy_Consumption"],default_index = 0)
     if   selected2 == 'Diesel':
          st.title('Diesel Prediction Results')
          read_df = joblib.load(forecasts[BU][selected2])
          read_df.set_index("Date", inplace=True)
          st.markdown("### Actual vs predicted Quantity")
          st.markdown(f"The graph below shows the plot of the actual and the prediction for the backtest period consisting of the last 6 months of data. The model accuracy is {model_accuracy[BU][selected2]} %")
          fig = px.line(read_df, x=read_df.index, y=read_df.columns)
          st.write(fig)
     
     if   selected2 == 'Magnetite':
          st.title('Diesel Prediction Results')
          read_df = joblib.load(forecasts[BU][selected2])
          read_df.set_index("Date", inplace=True)
          st.markdown("### Actual vs predicted Quantity")
          st.markdown(f"The graph below shows the plot of the actual and the prediction for the backtest period consisting of the last 6 months of data. The model accuracy is {model_accuracy[BU][selected2]} %")
          fig = px.line(read_df, x=read_df.index, y=read_df.columns)
          st.write(fig)

     if   selected2 == 'Maintenance':
          st.title('Diesel Prediction Results')
          read_df = joblib.load(forecasts[BU][selected2])
          read_df.set_index("Date", inplace=True)
          st.markdown("### Actual vs predicted Quantity")
          st.markdown(f"The graph below shows the plot of the actual and the prediction for the backtest period consisting of the last 6 months of data. The model accuracy is {model_accuracy[BU][selected2]} %")
          fig = px.line(read_df, x=read_df.index, y=read_df.columns)
          st.write(fig)
     
     if   selected2 == 'Energy_Price':
          st.title('Diesel Prediction Results')
          read_df = joblib.load(forecasts[BU][selected2])
          read_df.set_index("Date", inplace=True)
          st.markdown("### Actual vs predicted Quantity")
          st.markdown(f"The graph below shows the plot of the actual and the prediction for the backtest period consisting of the last 6 months of data. The model accuracy is {model_accuracy[BU][selected2]} %")
          fig = px.line(read_df, x=read_df.index, y=read_df.columns)
          st.write(fig)

     if   selected2 == 'Explosives':
          st.title('Diesel Prediction Results')
          read_df = joblib.load(forecasts[BU][selected2])
          read_df.set_index("Date", inplace=True)
          st.markdown("### Actual vs predicted Quantity")
          st.markdown(f"The graph below shows the plot of the actual and the prediction for the backtest period consisting of the last 6 months of data. The model accuracy is {model_accuracy[BU][selected2]} %")
          fig = px.line(read_df, x=read_df.index, y=read_df.columns)
          st.write(fig) 

     if   selected2 == 'Energy_Consumption':
          st.title('Diesel Prediction Results')
          read_df = joblib.load(forecasts[BU][selected2])
          read_df.set_index("Date", inplace=True)
          st.markdown("### Actual vs predicted Quantity")
          st.markdown(f"The graph below shows the plot of the actual and the prediction for the backtest period consisting of the last 6 months of data. The model accuracy is {model_accuracy[BU][selected2]} %")
          fig = px.line(read_df, x=read_df.index, y=read_df.columns)
          st.write(fig)     

if "Variables Prediction" in analysis:   
  
    st.subheader("Cost Variable Prediction :")
    with st.sidebar:

     selected = option_menu("Cost Variable to Predict",['Diesel', 'Explosives', 'Magnetite','Maintenance','Energy_Price','Energy_Consumption'],default_index=0)
 #Diesel Prediction Page
    if  selected == 'Diesel':  
    #page title
        st.title('Diesel Prediction using ML')
#getting the input data from the user
#column fro input fields
        #col1, col2,col3,col4= st.columns(4)

        col1, col2 = st.columns(2)
        with col1:
         TTH_input = st.number_input('Enter TTH volume (kg)', min_value=0)
         Diesel_Lag_input = st.number_input('Enter Previous Diesel (L)', min_value=0)
         TTH_Lag_input = st.number_input('Enter Previous TTH volume (kg)', min_value=0)
         Year_input = st.number_input('Enter year', min_value=0)
        with col2:
         diesel_price = st.number_input('Enter Current Price of Diesel (R)', value=10)

        input_df = {
        "Variable":["TTH_input","Year_input","Diesel_Lag_input","TTH_Lag_input"], 
        "Forecasted Quantity":[TTH_input,Diesel_Lag_input,TTH_Lag_input, ],
        
        }
    

        input_dict ={'TTH_input':TTH_input,'Year_input':Year_input,'Diesel_Lag_input':Diesel_Lag_input,'TTH_Lag_input':TTH_Lag_input}
        input_df = pd.DataFrame([input_dict])
        
#st.dataframe(input_df)

        Diesel = joblib.load(models[BU][selected]) # dictionary models[BU][Diesel]
    
        def predictor():
         d = Diesel.predict([[TTH_input,Year_input,Diesel_Lag_input,TTH_Lag_input]])
         return d
     
        predict_button = st.button('Diesel Prediction', on_click=predictor)

        if predict_button:
         result = predictor()
         st.success(f'The predicted values for Diesel (L) is : {result[0]:.2f}   \n The Forecasted Price is : R {diesel_price*result[0]:.2f}' )
         #diesel_price_forecast = diesel_quantity_forecast*diesel_price

    #Explosives Prediction Page

    if selected == 'Explosives':
    #page title
         st.title('Explosives Prediction using ML')
#getting the input data from the user
#column fro input fields

         col1, col2 = st.columns(2)
         with col1:
          TTH_input = st.number_input('Enter TTH volume (kg)', min_value=0)
          Year_Month_input = st.number_input('Enter year month', min_value=0)
          Year = st.number_input('Enter year', min_value=0)
          TTH_Lag_input = st.number_input('Enter Previous TTH volume (kg)', min_value=0)
         with col2:
          explosives_price = st.number_input('Enter Current Price of Explosives (R)', value=10)
    
         input_df = {
         "Variable":["TTH_input","Year_Month_input","Year","TTH_Lag_input"], 
         "Forecasted Quantity":[TTH_input,Year_Month_input,Year,TTH_Lag_input]}

         input_dict ={'TTH_input':TTH_input,'Year_Month_input':Year_Month_input,'Year':Year,'TTH_Lag_input':TTH_Lag_input}
         input_df = pd.DataFrame([input_dict])

         Explosives = joblib.load(models[BU][selected])
    
         def predictor():
          e = Explosives.predict([[TTH_input,Year_Month_input,Year,TTH_Lag_input]])
          return e

         predict_button = st.button('Explosives Prediction', on_click=predictor)

         if predict_button:
          result = predictor()
          st.success(f'The predicted values for Explosives (Kg) is : {result[0]:.2f}   \n The Forecasted Price is : R {explosives_price*result[0]:.2f}')


#Magnetite Prediction Page

    if selected == 'Magnetite':
    
    #page title
         st.title('Magnetite Prediction using ML')
#getting the input data from the user
#column fro input fields


         col1, col2 = st.columns(2)
         with col1:
          Feed_To_Plant_input = st.number_input('Enter Feed to Plant volume (kg)', min_value=0)
          Product_input = st.number_input('Enter Product volume (kg)', min_value=0)
          Year_input = st.number_input('Enter year', min_value=0)
         with col2:
          magnetite_price = st.number_input('Enter Current Price of Magnetite (R)', value=10)

         input_df = {
         "Variable":["TTH_input","Product_input","Year_Month_input"], 
         "Forecasted Quantity":[Feed_To_Plant_input,Product_input,Year_input]}

         magnetite_input_dict ={'Feed_To_Plant_input':Feed_To_Plant_input,'Product_input':Product_input,'year_input':Year_input}
         magnetite_input_df = pd.DataFrame([magnetite_input_dict])
#st.dataframe(explosives_input_df)

         Magnetite = joblib.load(models[BU][selected])
         def magnetite_predictor():
            m = Magnetite.predict([[Feed_To_Plant_input,Product_input,Year_input]])
            return m

         predict_button = st.button('Magnetite Prediction', on_click=magnetite_predictor)

         if predict_button:
          result = magnetite_predictor()
          st.success(f'The predicted values for Magnetite(Kg) is : {abs(result)[0]:.2f}   \n The Forecasted Price is : R {magnetite_price*abs(result[0]):.2f}')


#Maintenance Prediction Page
    if selected == 'Maintenance':
         
   #page title
         st.title('Maintenance Prediction using ML')
#getting the input data from the user
#column fro input fields

         col1, col2 = st.columns(2)
         with col1:
          Feed_to_Plant_input = st.number_input('Enter Feed to Plant volume (kg)', min_value=0)
          ROM_input = st.number_input('Enter ROM volume (kg)', min_value=0)
          Maintenance_input = st.number_input('Enter Previous Maintenance (R)', min_value=0)
          Year_Month_input = st.number_input('Enter year month', min_value=0)
          Year_input = st.number_input('Enter year', min_value=0)
         with col2:
          Maintenance_price = st.number_input('Enter Current Price of Diesel (R)', value=10)

         input_df = {
         "Variable":["ROM_input","Feed_to_Plant_input","Year_Month_input","Year_input","Maintenance_input"], 
         "Forecasted Quantity":[ ROM_input,Feed_to_Plant_input,Year_Month_input,Year_input,Maintenance_input]}

         maintenance_input_dict ={'ROM_input':ROM_input,'Feed_to_Plant_input':Feed_to_Plant_input,'year_month_input':Year_Month_input,'Year_input':Year_input,'Maintenance_input':Maintenance_input}
         maintenance_input_df = pd.DataFrame([maintenance_input_dict])
#st.dataframe(explosives_input_df)

         Maintenance = joblib.load(models[BU][selected ])
         def maintenance_predictor():
            m = Maintenance.predict([[ROM_input,Feed_to_Plant_input,Year_Month_input,Year_input,Maintenance_input]])
            return m

         predict_button = st.button('Maintenance Prediction', on_click=maintenance_predictor)

         if predict_button:
          result = maintenance_predictor()
          st.success(f'The predicted values for Maintenance is : R {result[0]:.2f} ')


#Energy Consumption Prediction Page
    if selected == 'Energy_Consumption':
#page title
         st.title('Energy_Consumption Prediction using ML')
#getting the input data from the user
#column fro input fields

         col1, col2 = st.columns(2)
         with col1:
          TTH_input = st.number_input('Enter TTH volume (kg)', min_value=0)
          ROM_input = st.number_input('Enter ROM volume (kg)', min_value=0)
          Product_input = st.number_input('Enter Product volume (kg)', min_value=0)
          Year_Month_input = st.number_input('Enter year month', min_value=0)
          Year_input = st.number_input('Enter year', min_value=0)
         with col2:
          Energy_Consumption = st.number_input('Enter Current Price of Energy Consumption (R)', value=10)

          input_df = {
         "Variable":["TTH_input", "ROM_input","Product_input","Year_Month_input","Year_input"], 
         "Forecasted Quantity":[TTH_input,ROM_input,Product_input,Year_Month_input,Year_input]}


         energy_consumption_input_dict ={'TTH_input':TTH_input,'ROM_input':ROM_input,'Product_input':Product_input,'Year_Month_input':Year_Month_input,'Year_input':Year_input}
         energy_consumption_input_df = pd.DataFrame([energy_consumption_input_dict])
#st.dataframe(explosives_input_df)

         energy_consumption = joblib.load(models[BU][selected])
    
         def energy_consumption_predictor():
          ec = energy_consumption.predict([[TTH_input,ROM_input,Product_input,Year_Month_input,Year_input]])
          return ec

         predict_button = st.button('Energy Consumption Prediction', on_click=energy_consumption_predictor)

         if predict_button:
          result = energy_consumption_predictor()
          st.success(f'The predicted values for Energy Consumption is (R) : {abs(result[0]):.2f} ')


#Energy Price Prediction Page

    if selected == 'Energy_Price':
#page title
          st.title('Energy_Price Prediction using ML')
#getting the input data from the user
#column fro input fields

          col1, col2 = st.columns(2)
          with col1:
           ROM_input = st.number_input('Enter ROM volume (kg)', min_value=0)
           Product_input = st.number_input('Enter Product volume(kg)', min_value=0)
           Year_input = st.number_input('Enter year', min_value=0)
          with col2:
           Energy_price = st.number_input('Enter Current Price of Diesel (R)', value=10)

           input_df = {
         "Variable":["ROM_input","Product_input","Year_Month_input"], 
         "Forecasted Quantity":[ROM_input,Product_input,Year_input]}

           energy_price_input_dict ={'ROM_input':ROM_input,'Product_input':Product_input,'Year_input':Year_input}
           energy_price_input_df = pd.DataFrame([energy_price_input_dict])
#st.dataframe(energy price_input_df)

           energy_price = joblib.load(models[BU][selected ])
    
           def energy_price_predictor():
            ep = energy_price.predict([[ROM_input,Product_input,Year_input]])
            return ep

          predict_button = st.button('Energy Price Prediction', on_click=energy_price_predictor)

          if predict_button:
           result = energy_price_predictor()
           st.success(f'The predicted values for Energy Price is (R) : {result[0]:.2f} ')

if "Exploratory Analysis" in analysis:
     st.subheader("Exploratory Data Analysis")
     with st.sidebar:
          selected2 = option_menu("Select the BU of Interest",[BU],default_index = 0)
     if   selected2 == 'Mafube':
          st.title('Mafube Correlation Plot')
          cols = df.columns
          variables = st.multiselect("Choose variables for the correlation matrix", cols
        )
          scale_data = st.checkbox('Scale data before plotting')

          fig_col1, fig_col2 = st.columns(2)

          with fig_col1:
           st.markdown("### Correlation Plot")
          if not variables:
            st.error("Please select at least one variable.")
          else:
            fig1, ax = plt.subplots(figsize=(7, 5))
            sns.heatmap(df[variables].corr(), cmap="YlGnBu", annot=True, ax=ax)
            st.write(fig1)
          with fig_col2:
           st.markdown("### Time Series")

          if scale_data:
            scaled_df = df[cols]
            x = df.values #returns a numpy array
            min_max_scaler = preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            scaled_df.iloc[:,:] = min_max_scaler.fit_transform(scaled_df.iloc[:,:].to_numpy())
            fig2 = px.line(scaled_df, x=scaled_df.index, y=variables, title="Monthly Quantity")
          else:
            fig2 = px.line(df, x=df.index, y=variables, title="Monthly Quantity")

        
          st.write(fig2)

          disp_data = st.checkbox('Display Raw Data')
          if disp_data:
           st.subheader('Dataframe:')
           n, m = df.shape
           st.write(f'<p style="font-size:130%">Dataset contains {n} rows and {m} columns.</p>', unsafe_allow_html=True)   
           st.dataframe(df)
         

     











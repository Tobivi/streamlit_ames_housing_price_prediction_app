import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf

import tensorflow_probability as tfp
tfd = tfp.distributions

from pickle import dump
from pickle import load

# dump(scaler, open('scaler.pkl', 'wb'))

scaler = load(open('scaler.pkl', 'rb'))



tf.random.set_seed(42)

np.random.seed(42)




st.title('Estimating Housing Price in Ames, Iowa')

name_list = ['MSSubClass',
 'OverallQual',
 'YearBuilt',
 'YearRemodAdd',
 'BsmtUnfSF',
 'TotalBsmtSF',
 'FstFlrSF',
 'SndFlrSF',
 'GrLivArea',
 'FullBath',
 'HalfBath',
 'TotRmsAbvGrd',
 'Fireplaces',
 'GarageCars',
 'GarageArea',
 'MoSold',
 'YrSold']

description_list = [
 'What is the building class?',
 'What is the Overall material and finish quality?',
 'In which year was the Original construction date?',
 'In which year was it remodelled?',
 'What is the Unfinished square feet of basement area?',
 'What is the Total square feet of basement area?',
 'What is the First Floor square feet?',
 'What is the Second floor square feet?',
 'What is the Above grade (ground) living area square feet?',
 'What is the number of full bathrooms?',
'What is the number of Half baths?',
'What is the number of  Total rooms above grade (does not include bathrooms)?',
'What is the number of fireplaces?',
'What is the garage capacity in car sizes?',
'What is the size of garage in square feet?',
'In which month was it sold?',
'In which year was it sold?'






 ]

min_list = [20.0,1.0,1872.0,
 1950.0,
 0.0,
 0.0,
 334.0,
 0.0,
 334.0,
 0.0,
 0.0,
 2.0,
 0.0,
 0.0,
 0.0,
 1.0,
 2006.0]

max_list = [190.0,
 10.0,
 2010.0,
 2010.0,
 2336.0,
 6110.0,
 4692.0,
 2065.0,
 5642.0,
 3.0,
 2.0,
 14.0,
 3.0,
 4.0,
 1418.0,
 12.0,
 2010.0]

count = 0

with st.sidebar:

    for i in range(len(name_list)):

            

        variable_name = name_list[i]
        globals()[variable_name] = st.slider(description_list[i] ,min_value=int(min_list[i]), max_value =int(max_list[i]),step=1)
    


data_df = {

'MSSubClass': [MSSubClass],
 'OverallQual': [OverallQual],
 'YearBuilt': [YearBuilt],
 'YearRemodAdd': [YearRemodAdd],
 'BsmtUnfSF': [BsmtUnfSF],
 'TotalBsmtSF': [TotalBsmtSF],
 '1stFlrSF': [FstFlrSF],
 '2ndFlrSF': [SndFlrSF],
 'GrLivArea':[GrLivArea],
 'FullBath': [FullBath],
 'HalfBath': [HalfBath],
 'TotRmsAbvGrd':[TotRmsAbvGrd],
 'Fireplaces': [Fireplaces],
 'GarageCars': [GarageCars],
 'GarageArea':[GarageArea],
 'MoSold': [MoSold],
 'YrSold' : [YrSold]





}

model1 = tf.keras.models.load_model('model_files/my_keras_model1.h5')

model1 = tf.keras.models.Sequential(model1.layers[:5])

data_df = pd.DataFrame.from_dict(data_df)

data_df_normal = scaler.transform(data_df)

latent_var = model1.predict(data_df_normal)

model2 = tf.keras.models.load_model('model_files/keras_2.h5')

yhat = model2(latent_var)



if st.button('Calculate range of house price'):

    import time

    #my_bar = st.progress(0)

    with st.spinner('Calculating....'):
        time.sleep(2)



    st.subheader('The Price of Your desired house will be between ')

    col1, col2 = st.columns([3, 3])

    lower_number = "{:,.2f}".format(int(yhat.mean().numpy()-1.95*yhat.stddev().numpy()))
    higher_number = "{:,.2f}".format(int(yhat.mean().numpy()+1.95*yhat.stddev().numpy()))

    col1.subheader("USD "+ str(lower_number))

    col2.subheader("USD "+str(higher_number))

    

    import base64

    file_ = open("kramer_gif.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<center><img src="data:image/gif;base64,{data_url}" alt="cat gif"></center>',
        unsafe_allow_html=True,
    )
    




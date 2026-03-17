# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,  when_matched
import requests 
import pandas as pd
# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
#option=st.selectbox(
# 'What is your favorite fruit?',
# ('Banana', 'Strawberries', 'Peaches'))
# st.write( 'Your favorite fruit is: ',option)



name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be :', name_on_order)


cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_string=''
ingredients_list = st.multiselect('Choose up to 5 ingredients:'
                                  ,my_dataframe, max_selections=5)
if ingredients_list:
    for k in ingredients_list:
      ingredients_string+=k+' '
      st.subheader(k+" Nutrition Information")
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+k)  
      sf_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+ name_on_order+"""')"""





insert_time= st.button('Submit Order')
if insert_time and ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")

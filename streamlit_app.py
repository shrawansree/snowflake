# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

order_name  = st.text_input("Name on Smoothie:")
st.write(f"The name on your Smoothie will be: {order_name}")

cnx  =  st.connection("snowflake")
session =   cnx.session()
my_df   =   session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data = my_df, use_container_width=True)
# st.stop()

pd_df  =  my_df.to_pandas()

ingredients_list    =   st.multiselect(
    'Choose up to 5 ingredients:',
    my_df,
    max_selections=5
)

if ingredients_list:
    ingredients =   ''
  
    for fruit in ingredients_list:
      ingredients  +=  fruit + ' '

      search_on  =  pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
      # st.write('The search value for ', fruit,' is ', search_on, '.')
      search_on  =  search_on if search_on != None else fruit
      
      st.subheader(fruit + ' Nutrition Information')
      smoothiefroot_response  =  requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
      sf_df  =  st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
      
    my_insert_stmt = f"""insert into smoothies.public.orders(name_on_order, ingredients)
            values ('{order_name}','{ingredients}')"""
        
    submit_btn  =   st.button('Submit Order')
    if ingredients and submit_btn and order_name:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



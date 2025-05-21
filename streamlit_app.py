# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

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
my_df   =   session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data = my_df, use_container_width=True)

ingredients_list    =   st.multiselect(
    'Choose up to 5 ingredients:',
    my_df,
    max_selections=5
)

if ingredients_list:
    ingredients =   ' '.join(ingredients_list)
    my_insert_stmt = f"""insert into smoothies.public.orders(name_on_order, ingredients)
            values ('{order_name}','{ingredients}')"""
        

    submit_btn  =   st.button('Submit Order')
    if ingredients and submit_btn and order_name:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

smoothiefroot_response  =  requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df  =  st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

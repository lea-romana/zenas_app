# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title("Zena's Amazing Athleisure Catalog")

# Connect to database
cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table("zenas_athleisure_db.products.catalog_for_website").select(col("COLOR_OR_STYLE"), col("PRICE"), col("DIRECT_URL"), col("SIZE_LIST"), col("UPSELL_PRODUCT_DESC"))
pd_df = my_df.to_pandas()


option = st.selectbox(
    'Pick a sweatsuit color or style:',
    pd_df["COLOR_OR_STYLE"])

temp_df = pd_df[pd_df["COLOR_OR_STYLE"] == option].reset_index(drop = True)
st.write(temp_df.loc[0]["DIRECT_URL])

product_caption = f'Our warm, confortable, {option} sweatsuit!'

# streamlit.image(
#     df2[0],
#     width=400,
#     caption= product_caption
# )

st.dataframe(temp_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_df,
    max_selections=5
)

if ingredients_list:
    # st.text(ingredients_list)
    ingredients_string=''
    for fruit in ingredients_list:
        ingredients_string+=fruit+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit,' is ', search_on, '.')
        # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        # st.text(fruityvice_response)
    # st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered {name_on_order}!', icon="✅")

# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response)

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!""")

# option = st.selectbox(
#     'What is your favorite fruit?',
#     ('Banana', 'Strawberries', 'Peaches'))

# st.write('Your favorite fruit is:', option)

name_on_order = st.text_input('Name on Smoothie: ')
st.write(f'The name on your Smoothie will be: {name_on_order}')

session = get_active_session()
my_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
# st.dataframe(data=my_df, use_container_width=True)

pd_df = my_df.to_pandas()
# st.dataframe(pd_df)
# st.stop()

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

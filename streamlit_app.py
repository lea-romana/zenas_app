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

product_caption = f'Our warm, confortable, {option} sweatsuit!'

st.image(
    temp_df.loc[0]["DIRECT_URL"],
    width=400,
    caption= product_caption
)

st.write("Price: ", temp_df.loc[0]["PRICE"])
st.write("Available sizes: ", temp_df.loc[0]["SIZE_LIST"])
st.write("Bonus: ", temp_df.loc[0]["UPSELL_PRODUCT_DESC"])

# st.dataframe(temp_df)
# st.stop

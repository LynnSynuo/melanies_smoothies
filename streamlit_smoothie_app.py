# Import python packages
# import Streamlit library and assign it the alias 'st'
import streamlit as st

# import 'col' function from snowflake snowpark
# it is used to reference columns in Snowflake tables
from snowflake.snowpark.functions import col
import requests



# Write directly to the app
# sets the title of the streamlit app
st.title("Customize Your Smoothie! :cup_with_straw:")
# write a message to the streamlit app with multiple rows
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    
    """
)
#--------------------------------------
# a select box
# just a few options

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"))

# st.write("Your favorite fruit is:", option)
# above: the select box is removed 
#-----------------------------------

# to have more options
# insert a database table
# my_dataframe is a dataframe

# This line gets the active Snowflake session 
# using the get_active_session function 
# and assigns it to the variable session.
cnx = st.connection("snowflake")
session = cnx.session()
# create dataframe 'my_dataframe'
# by querying Snowflake table smoothies.public.fruit_options
# select column of 'fruit_name' using col function
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
# display the table in Streamlit app using st.dataframe function
# use_container_width = True is to fit width based on the container

# st.dataframe(data = my_dataframe, use_container_width = True)



name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# create a multiselection dropdown in streamlit app
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

# ingredients_list is a list
# to test the content of ingredients_list

if ingredients_list:
   
    ingredients_string = '' # initialize the string with ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit +' '
        st.subheader(each_fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit)
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
    
    st.write(ingredients_string) # write the ingredients_string in Streamlit app


    # insert the selected fruit into snowflake table, under 'ingredients' column
    # SQL insert statement (my_insert_stmt) to insert the selected ingredients 
    # into Snowflake table 'smoothies.public.orders' under the 'ingredients' column.
    # SQL code:
    # insert into smoothies.public.orders(ingredients)
    # values ('a b c');
    # this part --> """ +ingredients_string+ """ is to insert the multi-selection into the order table

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) 
    values ('""" +ingredients_string+ """','"""+ name_on_order + """')
    """
    # st.write(my_insert_stmt)
    # st.stop()
    # create a button called 'Submit Order' 
    # and assign this button to variable time_to_insert
    time_to_insert = st.button('Submit Order')

    if time_to_insert:

        # Executes the SQL insert statement (my_insert_stmt) 
        # using the Snowflake session (session) 
        # and collects the result.
        session.sql(my_insert_stmt).collect()

        # Displays a success message in the Streamlit app 
        # st.success('Your Smoothie is ordered!', icon = "✅")
        # to add a name in the st.success message
        st.success(f'Your Smoothie is ordered! {name_on_order}', icon = "✅")



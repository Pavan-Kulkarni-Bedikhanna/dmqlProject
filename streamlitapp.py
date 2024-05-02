import streamlit as st
import psycopg2
import pandas as pd

# Database credentials
endpoint = "hospitalmgmt.cpoys6m2wfp9.us-east-2.rds.amazonaws.com"
username = "postgres"
password = "postgres"
dbname = "HospitalManagementSystem"
port = 5432

# Initialize a connection to the database
def init_connection():
    return psycopg2.connect(
        host=endpoint,
        user=username,
        password=password,
        dbname=dbname,
        port=port
    )

# Function to get the list of table names from the database
def load_table_names():
    conn = init_connection()
    cur = conn.cursor()
    cur.execute("""SELECT table_name FROM information_schema.tables
                   WHERE table_schema = 'public'""")
    table_names = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return table_names

# Function to get table info
def get_table_info(table_name):
    conn = init_connection()
    cur = conn.cursor()
    cur.execute(f"""SELECT column_name, data_type FROM information_schema.columns
                    WHERE table_name = '{table_name}'""")
    info = pd.DataFrame(cur.fetchall(), columns=['Column Name', 'Data Type'])
    cur.close()
    conn.close()
    return info

# Function to get records from the table
def get_table_records(table_name):
    conn = init_connection()
    df = pd.read_sql(f'SELECT * FROM {table_name}', con=conn)
    conn.close()
    return df

# Function to add background image from URL
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://raw.githubusercontent.com/Pavan-Kulkarni-Bedikhanna/dmqlProject/main/dmql_background.jpg");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to add the background image
add_bg_from_url()

# Title
# st.title("Database Management Dashboard")


# HTML to change title color
st.markdown("""
<style>
.title {
color: #FF6347;  # You can change this hex color as per your preference
}
</style>
""", unsafe_allow_html=True)

# Use the CSS class in your title
st.markdown('<h1 class="title">Hospital Management System</h1>', unsafe_allow_html=True)


# Load table names for the dropdown
table_names = load_table_names()
st.markdown("""
<style>
div.stSelectbox label {
    color: white;    
}
</style>
""", unsafe_allow_html=True)
table_name = st.selectbox("Select Table Name:", table_names)

st.markdown("""
<style>
div.stRadio > label,p {
    color: #FF6347;  
}
</style>
""", unsafe_allow_html=True)

# Options for actions
action = st.radio("Select an action", ["Get Table Information", "Fetch Records"])

if action == "Get Table Information":
    if st.button("Show Information"):
        table_info = get_table_info(table_name)
        st.write(table_info)
elif action == "Fetch Records":
    if st.button("Show Records"):
        records = get_table_records(table_name)
        st.dataframe(records)


# # Create a text input field
# query = st.text_input("Enter your SQL Query here:")
# if st.button("Execute Query"):
#     try:
#         conn = init_connection()
#         df = pd.read_sql(query, con=conn)
#         conn.close()
#         st.dataframe(df)
#     except Exception as e:
#         st.error(f"Error executing query: {str(e)}")

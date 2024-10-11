import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object and specify the spreadsheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Now read the data from the worksheet
data = conn.read(worksheet="Sheet1", usecols=list(range(2)))

st.dataframe(data)

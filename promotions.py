import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet = "1zu1v-w6KnpB-Mw6D5_ikwL2jrkmzGT_MF6Dpu-J0Y_I"

@st.cache_data
def load_promotions_data():
    """Load promotions data from Google Sheets."""
    promotions = conn.read(spreadsheet_id = spreadsheet, worksheet="Promotion")
    return pd.DataFrame(promotions)

def save_promotions_data(dataframe):
    """Save the entire promotions DataFrame to Google Sheets."""
    try:
        conn.update(worksheet="Promotion", data=dataframe)
    except Exception as e:
        st.error(f"Failed to update promotions: {e}")

def manage_promotions():
    st.title("Promotions & Discounts")
    st.write("Manage promotional offers and discounts.")

    # Load existing promotions data
    promo_df = load_promotions_data()

    # Display existing promotions
    st.subheader("Existing Promotions")
    st.write("Edit or remove promotions below:")
    if promo_df.empty:
        st.info("No promotions available. Add a new promotion using the form below.")
    else:
        for index, row in promo_df.iterrows():
            with st.expander(f"Promotion {index + 1}: {row['name']}"):
                with st.form(f"edit_form_{index}"):
                    # Editable fields for the promotion
                    promo_name = st.text_input("Promotion Code", value=row["name"])
                    promo_desc = st.text_area("Promotion Description", value=row["description"])
                    start_date = st.date_input("Start Date", value=pd.to_datetime(row["start_date"]).date())
                    end_date = st.date_input("End Date", value=pd.to_datetime(row["end_date"]).date())
                    discount = st.number_input("Discount (%)", min_value=0, max_value=100, value=int(row["discount"]))
                    
                    # Save or delete options
                    col1, col2 = st.columns(2)
                    with col1:
                        save_button = st.form_submit_button("Save Changes")
                    with col2:
                        delete_button = st.form_submit_button("Delete Promotion")

                    # Save changes
                    if save_button:
                        promo_df.loc[index, "name"] = promo_name
                        promo_df.loc[index, "description"] = promo_desc
                        promo_df.loc[index, "start_date"] = str(start_date)
                        promo_df.loc[index, "end_date"] = str(end_date)
                        promo_df.loc[index, "discount"] = discount
                        save_promotions_data(promo_df)
                        st.cache_data.clear()  # Clear cached data
                        st.success(f"Promotion '{promo_name}' updated successfully!")
                        st.rerun()

                    # Delete promotion
                    if delete_button:
                        promo_df = promo_df.drop(index)
                        save_promotions_data(promo_df)
                        st.cache_data.clear()  # Clear cached data
                        st.success(f"Promotion '{row['name']}' deleted successfully!")
                        st.rerun()

    # Add new promotion form
    st.subheader("Add New Promotion")
    with st.form("add_promotion"):
        promo_name = st.text_input("Promotion Name")
        promo_desc = st.text_area("Promotion Description")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        discount = st.number_input("Discount (%)", min_value=0, max_value=100)
        submitted = st.form_submit_button("Create Promotion")
        
        if submitted:
            # Append new promotion to the DataFrame
            new_promo = pd.DataFrame(
                [
                    {
                        "name": promo_name,
                        "description": promo_desc,
                        "start_date": str(start_date),
                        "end_date": str(end_date),
                        "discount": discount
                    }
                ]
            )
            promo_df = pd.concat([promo_df, new_promo], ignore_index=True)
            save_promotions_data(promo_df)
            st.cache_data.clear()  # Clear cached data
            st.success(f"Promotion '{promo_name}' created successfully!")
            st.rerun()

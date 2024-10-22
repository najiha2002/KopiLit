import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data
def load_promotions_data():
    promotion = conn.read(worksheet="Promotion")
    return pd.DataFrame(promotion)

def save_promotions_data(dataframe):
    promotion = conn.read(worksheet="Promotion")

    # Clear the existing data
    worksheet.clear()
    
    # Update the worksheet with new data from the dataframe
    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())



def manage_promotions():
    #st.title("Promotions & Discounts")
    #st.write("Manage promotional offers and discounts.")
    #coupon_code = st.text_input("Enter Coupon Code")
    #discount = st.slider("Discount Percentage", 0, 100)
    #if st.button("Create Coupon"):
    #    st.success(f"Coupon {coupon_code} offering {discount}% discount created!")

    with st.form("Add Promotion"):
        promo_name = st.text_input("Promotion Name")
        promo_desc = st.text_area("Promotion Description")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        discount = st.number_input("Discount (%)", min_value=0, max_value=100)
        submitted = st.form_submit_button("Create Promotion")
        
        if submitted:
            # Load existing promotions data
            promo_df = load_promotions_data()
            
            # Append the new promotion
            new_promo = pd.DataFrame (
                [
                    {
                'name': promo_name,
                'description': promo_desc,
                'start_date': str(start_date),  # Convert to string for Google Sheets
                'end_date': str(end_date),      # Convert to string for Google Sheets
                'discount': discount
                    }
                ]
            )
    

            new_promo_df = promo_df._append(new_promo, ignore_index=True)
            
            # Save to Google Sheets
            #save_promotions_data(promo_df)
            #st.success("Promotion created successfully!")

            try:
                #Update Gsheet by appending new row
                new_promo_df = pd.concat([promo_df, new_promo,], ignore_index=True)
                conn.update(worksheet="Promotion", data=new_promo_df)
                st.success("Promotion created successfully!")
            
            except Exception as e:
                st.error(f"Failed to update promotions: {e}")

    
        # Display existing promotions
        promo_df = load_promotions_data()
        st.dataframe(promo_df)

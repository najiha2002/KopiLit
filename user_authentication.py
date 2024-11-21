import streamlit as st

# Simulated Payment Popup
st.title("Payment Gateway Example")

if st.button("Pay Now"):
    st.markdown("### Payment in Progress... 💳")
    with st.expander("Enter Payment Details (Simulated Popup)", expanded=True):
        card_number = st.text_input("Card Number")
        expiry_date = st.text_input("Expiry Date (MM/YY)")
        cvv = st.text_input("CVV", type="password")
        amount = st.number_input("Amount to Pay", min_value=1.00, step=0.01)

        if st.button("Submit Payment"):
            if card_number and expiry_date and cvv:
                st.success("Payment Successful! 🎉")
            else:
                st.error("Please fill in all the fields.")

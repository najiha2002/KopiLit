import streamlit as st

def payment_user():
    st.title("Secure Payment - Customer Side")
    st.write("Complete your payment to confirm the order.")
    
    payment_method = st.selectbox("Select Payment Method", ["Credit Card", "Debit Card", "PayPal"])
    card_number = st.text_input("Card Number") if payment_method in ["Credit Card", "Debit Card"] else None
    expiration_date = st.text_input("Expiration Date (MM/YY)") if card_number else None
    cvv = st.text_input("CVV", type="password") if card_number else None
    
    if payment_method == "PayPal":
        paypal_email = st.text_input("PayPal Email")
    
    if st.button("Pay Now"):
        if payment_method in ["Credit Card", "Debit Card"] and (not card_number or not expiration_date or not cvv):
            st.error("Please fill in all card details.")
        elif payment_method == "PayPal" and not paypal_email:
            st.error("Please enter your PayPal email.")
        else:
            st.success("Payment successful! Your order has been confirmed.")
            st.write("You can view or download your invoice below.")
            st.download_button(label="Download Invoice", data="Invoice details here", file_name="invoice.txt")

import streamlit as st

def payment_user():
    st.title("Secure Payment - Customer Side")
    st.write("Complete your payment to confirm the order.")
    
    payment_method = st.selectbox("Select Payment Method", ["Credit Card", "Debit Card", "PayPal"])
    card_number = st.text_input("Card Number") if payment_method in ["Credit Card", "Debit Card"] else None
    expiration_date = st.text_input("Expiration Date (MM/YY)") if card_number else None
    cvv = st.text_input("CVV", type="password") if card_number else None
    
    if payment_method == "PayPal":
        paypal_email = st.text_input("PayPal Email")
    
    if st.button("Pay Now"):
        if payment_method in ["Credit Card", "Debit Card"] and (not card_number or not expiration_date or not cvv):
            st.error("Please fill in all card details.")
        elif payment_method == "PayPal" and not paypal_email:
            st.error("Please enter your PayPal email.")
        else:
            st.success("Payment successful! Your order has been confirmed.")
            st.write("You can view or download your invoice below.")
            st.download_button(label="Download Invoice", data="Invoice details here", file_name="invoice.txt")

payment_user()
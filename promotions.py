import streamlit as st

def manage_promotions():
    st.title("Promotions & Discounts")
    st.write("Manage promotional offers and discounts.")
    coupon_code = st.text_input("Enter Coupon Code")
    discount = st.slider("Discount Percentage", 0, 100)
    if st.button("Create Coupon"):
        st.success(f"Coupon {coupon_code} offering {discount}% discount created!")
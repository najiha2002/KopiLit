import streamlit as st

def payment_user():
    st.title("💳 Secure Payment - Customer Side")
    st.write("Complete your payment to confirm the order.")

    # Select payment method
    payment_method = st.selectbox("Select Payment Method", ["Credit Card", "Debit Card", "PayPal"])
    
    st.markdown("---")
    st.markdown("### Payment Details")

    # Fields for Credit/Debit Card payment
    card_number, expiration_date, cvv = None, None, None
    paypal_email = None

    if payment_method in ["Credit Card", "Debit Card"]:
        st.markdown("#### Card Information")
        card_number = st.text_input("Card Number", placeholder="Enter your card number")
        expiration_date = st.text_input("Expiration Date (MM/YY)", placeholder="MM/YY")
        cvv = st.text_input("CVV", placeholder="Enter CVV", type="password")

    # Fields for PayPal payment
    if payment_method == "PayPal":
        st.markdown("#### PayPal Information")
        paypal_email = st.text_input("PayPal Email", placeholder="Enter your PayPal email")

    # Process payment
    st.markdown("---")
    if st.button("💰 Pay Now"):
        if payment_method in ["Credit Card", "Debit Card"]:
            # Validate Credit/Debit Card fields
            if not card_number or not expiration_date or not cvv:
                st.error("Please fill in all card details.")
            else:
                st.success("Payment successful! Your order has been confirmed.")
                generate_invoice(payment_method, card_number, None, expiration_date, cvv)
        elif payment_method == "PayPal":
            # Validate PayPal fields
            if not paypal_email:
                st.error("Please enter your PayPal email.")
            else:
                st.success("Payment successful! Your order has been confirmed.")
                generate_invoice(payment_method, None, paypal_email, None, None)

def generate_invoice(payment_method, card_number, paypal_email, expiration_date, cvv):
    """Generate and display a downloadable invoice."""
    st.write("📄 You can view or download your invoice below.")

    # Dynamic invoice content
    invoice_details = f"""
    Payment Method: {payment_method}
    {'Card Number: ' + card_number if card_number else ''}
    {'PayPal Email: ' + paypal_email if paypal_email else ''}
    {'Expiration Date: ' + expiration_date if expiration_date else ''}
    {'CVV: ***' if cvv else ''}
    """

    st.download_button(
        label="📥 Download Invoice",
        data=invoice_details,
        file_name="invoice.txt",
        mime="text/plain"
    )
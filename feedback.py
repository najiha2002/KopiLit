#fasya try test

import streamlit as st

def collect_feedback():
    st.title("Customer Feedback")
    st.write("We value your feedback!")
    feedback_text = st.text_area("Please share your thoughts")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

def view_feedback():
    st.title("View Feedback")
    st.write("Customer feedback received:")
    feedback_data = ["Great coffee!", "Loved the service", "Would appreciate more vegan options"]
    st.write(feedback_data)

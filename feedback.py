#fasya try test

import streamlit as st


#load feedback data from gsheet
def load_feedback_data():
    feedback = conn.read(worksheet="Feedback")
    return pd.DataFrame(feedback)


def collect_feedback():
    st.title("Customer Feedback")
    st.write("We value your feedback!")
    feedback_text = st.text_area("Please share your thoughts")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

#Admin - Feedback Overview

def view_feedback():
    st.title("View Feedback")
    st.write("Customer feedback received:")
    
    #dummy 
    feedback_data = ["Great coffee!", "Loved the service", "Would appreciate more vegan options"]
    st.write(feedback_data)

    #real
    feedback_df = load_feedback_data()

    # Show feedback as table
    st.dataframe(feedback_df)
    
    # Display stats and analysis
    avg_rating = feedback_df['rating'].mean()
    st.write(f"Average Rating: {avg_rating:.2f}/5")
    
    # Display charts (e.g., feedback trend over time)
    st.line_chart(feedback_df['rating'])





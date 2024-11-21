import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Load feedback data from Google Sheets
@st.cache_data
def load_feedback_data():
    try:
        feedback = conn.read(worksheet="Feedback")
        return pd.DataFrame(feedback)
    except Exception as e:
        st.error(f"Error loading feedback data: {e}")
        return pd.DataFrame()

# Save feedback data to Google Sheets
def save_feedback_data(new_feedback):
    try:
        feedback_df = load_feedback_data()
        updated_feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
        conn.update(worksheet="Feedback", data=updated_feedback_df)
        st.success("Thank you for your feedback!")
    except Exception as e:
        st.error(f"Failed to save feedback: {e}")

# Collect customer feedback
def collect_feedback():
    st.title("Customer Feedback")
    st.write("We value your feedback! Please share your thoughts below.")
    
    feedback_text = st.text_area("Your Feedback")
    rating = st.slider("Rate your experience (1 = Poor, 5 = Excellent)", min_value=1, max_value=5)
    
    if st.button("Submit Feedback"):
        if feedback_text.strip():
            new_feedback = pd.DataFrame([{
                "Feedback": feedback_text,
                "Rating": rating,
                "Timestamp": pd.Timestamp.now()
            }])
            save_feedback_data(new_feedback)
            st.experimental_rerun()
        else:
            st.error("Feedback text cannot be empty.")

# Admin feedback overview
def view_feedback():
    st.title("Feedback Overview")
    st.write("View all customer feedback and analyze ratings.")

    # Load feedback data
    feedback_df = load_feedback_data()
    
    if feedback_df.empty:
        st.info("No feedback available yet.")
        return

    # Display feedback data as a table
    st.subheader("Customer Feedback Data")
    st.dataframe(feedback_df)
    
    # Check if the required columns exist
    if 'Rating' in feedback_df.columns:
        # Calculate average rating
        feedback_df['Rating'] = pd.to_numeric(feedback_df['Rating'], errors='coerce')
        avg_rating = feedback_df['Rating'].mean()
        st.write(f"Average Rating: {avg_rating:.2f}/5")

        # Display rating trend over time (assuming a timestamp column exists)
        if 'Timestamp' in feedback_df.columns:
            feedback_df['Timestamp'] = pd.to_datetime(feedback_df['Timestamp'], errors='coerce')
            feedback_df = feedback_df.sort_values('Timestamp')
            st.line_chart(feedback_df.set_index('Timestamp')['Rating'])
        else:
            st.warning("Timestamp column is missing for trend analysis.")
    else:
        st.warning("Rating column is missing for statistical analysis.")

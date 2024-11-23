import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet = "1zu1v-w6KnpB-Mw6D5_ikwL2jrkmzGT_MF6Dpu-J0Y_I"

# Load feedback data from Google Sheets
@st.cache_data
def load_feedback_data():
    try:
        feedback = conn.read(spreadsheet_id = spreadsheet, worksheet="Feedback")
        return pd.DataFrame(feedback)
    except Exception as e:
        st.error(f"Error loading feedback data: {e}")
        return pd.DataFrame()

# Save feedback data to Google Sheets
def save_feedback_data(new_feedback):
    try:
        # Clear cache before fetching fresh data
        st.cache_data.clear()
        feedback_df = load_feedback_data()
        updated_feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
        conn.update(spreadsheet_id = spreadsheet, worksheet="Feedback", data=updated_feedback_df)
        st.success("Thank you for your feedback!")
        # Clear cache after updating data
        st.cache_data.clear()
    except Exception as e:
        st.error(f"Failed to save feedback: {e}")

# Load user data to get last names
@st.cache_data
def load_users_data():
    users_data = conn.read(spreadsheet_id = spreadsheet, worksheet="User")
    return pd.DataFrame(users_data)

# Collect customer feedback
def collect_feedback():
    st.title("Customer Feedback")
    st.write("We value your feedback! Please share your thoughts below.")
    
    # Get the logged-in user's last name
    users_data = load_users_data()
    current_user = st.session_state.get("username")
    user_row = users_data.loc[users_data["Username"] == current_user]
    
    if not user_row.empty:
        last_name = user_row.iloc[0]["Last Name"]
        st.write(f"Logged in as: {last_name}")
    else:
        last_name = "Unknown User"
        st.warning("Could not fetch user information. Please log in again.")

    feedback_text = st.text_area("Your Feedback")
    rating = st.slider("Rate your experience (1 = Poor, 5 = Excellent)", min_value=1, max_value=5)
    
    if st.button("Submit Feedback"):
        if feedback_text.strip():
            new_feedback = pd.DataFrame([{
                "Name": last_name,
                "Feedback": feedback_text,
                "Rating": rating,
                "Timestamp": pd.Timestamp.now()
            }])
            save_feedback_data(new_feedback)
            st.experimental_rerun()
        else:
            st.error("Feedback text cannot be empty.")

# Admin feedback overview
# Admin feedback overview with analytics visualization
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
        # Convert Rating column to numeric
        feedback_df['Rating'] = pd.to_numeric(feedback_df['Rating'], errors='coerce')
        
        # Calculate average rating
        avg_rating = feedback_df['Rating'].mean()
        st.metric("Average Rating", f"{avg_rating:.2f} / 5")

        # Distribution of ratings
        st.subheader("Ratings Distribution")
        st.bar_chart(feedback_df['Rating'].value_counts().sort_index())

        # Rating trend over time (assuming a timestamp column exists)
        if 'Timestamp' in feedback_df.columns:
            feedback_df['Timestamp'] = pd.to_datetime(feedback_df['Timestamp'], errors='coerce')
            feedback_df = feedback_df.sort_values('Timestamp')

            # Display line chart for rating trend
            st.subheader("Rating Trend Over Time")
            st.line_chart(feedback_df.set_index('Timestamp')['Rating'])
        else:
            st.warning("Timestamp column is missing for trend analysis.")
    else:
        st.warning("Rating column is missing for statistical analysis.")

    # Display top feedbacks
    st.subheader("Top Feedback Comments")
    if 'Feedback' in feedback_df.columns and 'Rating' in feedback_df.columns:
        top_feedbacks = feedback_df.sort_values(by='Rating', ascending=False).head(5)
        for _, row in top_feedbacks.iterrows():
            st.write(f"**Rating:** {row['Rating']} ⭐")
            st.write(f"**Comment:** {row['Feedback']}")
            st.write("---")
    else:
        st.warning("Feedback or Rating column is missing for detailed comments analysis.")


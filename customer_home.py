import streamlit as st
import pandas as pd
import customer_order
import feedback
import rewards
from streamlit_gsheets import GSheetsConnection
import datetime


# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)


def fetch_menu():
    menu_data = pd.DataFrame(conn.read(worksheet = "Menu"))
    

# Styling
    st.markdown(
        """
        <style>
        body {
            background-color: #1b1b1b; /* Dark background */
        }
        .header-section {
            text-align: center;
            color: white;
            padding: 50px 20px;
            font-family: 'Georgia', serif;
        }
        .header-title {
            font-size: 3.5em;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .header-subtitle {
            font-size: 1.5em;
            margin-bottom: 40px;
        }
        .btn-container {
            margin-top: 20px;
        }
        .btn {
            display: inline-block;
            text-decoration: none;
            padding: 10px 25px;
            font-size: 1.1em;
            font-weight: bold;
            color: #1b1b1b;
            background-color: white;
            border: 2px solid white;
            border-radius: 5px;
            margin: 5px;
            transition: all 0.3s ease-in-out;
        }
        .btn:hover {
            background-color: #ffc107; /* Coffee color */
            color: #1b1b1b;
        }
        .stats-container {
            display: flex;
            justify-content: center;
            margin-top: 40px;
            gap: 50px;
        }
        .stats-item {
            text-align: center;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .stats-item h2 {
            font-size: 2.5em;
            margin: 0;
        }
        .stats-item p {
            font-size: 1em;
            margin: 0;
        }
        .coffee-image {
            text-align: center;
            margin-top: 30px;
        }
        .coffee-image img {
            max-width: 400px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    # Header Section
    st.markdown(
        """
        <div class="header-section">
            <h1 class="header-title">Discover The Art Of Perfect Coffee</h1>
            <p class="header-subtitle">
                Experience the rich and bold flavors of KopiLit's exquisite coffee blends, 
                crafted to awaken your senses and start your day right.
            </p>
            <div class="btn-container">
                <a href="#" class="btn">Order Now</a>
                <a href="#" class="btn">Explore More</a>
            </div>
            <div class="stats-container">
                <div class="stats-item">
                    <h2>50+</h2>
                    <p>Items of Coffee</p>
                </div>
                <div class="stats-item">
                    <h2>20+</h2>
                    <p>Orders Running</p>
                </div>
                <div class="stats-item">
                    <h2>2k+</h2>
                    <p>Happy Customers</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # Coffee Image Section
    st.markdown(
        """
        <div class="coffee-image">
            <img src="https://thumbs.dreamstime.com/b/dynamic-coffee-splash-mug-dark-background-high-speed-capture-droplets-frozen-time-around-white-325109112.jpg" alt="Coffee Splash">
        </div>
        """,
        unsafe_allow_html=True,
    )


    # Styling
    st.markdown(
        """
        <style>
        .product-card {
            text-align: center;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .product-card img {
            border-radius: 10px;
            max-width: 100%;
            height: auto;
        }
        .product-title {
            font-size: 18px;
            font-weight: bold;
            color: #6D4C41;
            margin: 10px 0 5px;
        }
        .product-description {
            font-size: 14px;
            color: #795548;
            margin: 5px 0 15px;
        }
        .product-price {
            font-size: 16px;
            color: #3E2723;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .add-to-cart-btn {
            display: inline-block;
            background-color: #6D4C41;
            color: #fff;
            text-decoration: none;
            font-size: 14px;
            padding: 10px 20px;
            border-radius: 5px;
            margin-top: 10px;
        }
        .add-to-cart-btn:hover {
            background-color: #3E2723;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    return menu_data


def display_menu():

    menu_data = fetch_menu()

    # Create an expander for the menu
    with st.expander("Display Featured Menu", expanded=True):
        # Display menu items in a grid layout
        cols = st.columns(3)  # Adjust the number of columns based on preference
        for index, row in menu_data.iterrows():  # Use the index to ensure unique keys
            # Handle missing images with a placeholder
            image_url = row['Image'] if 'Image' in row and pd.notna(row['Image']) else "https://via.placeholder.com/150"
            with cols[index % 3]:  # Distribute items across columns
                st.markdown(
                    f"""
                    <div class="product-card">
                        <img src="{image_url}" alt="{row['Name']}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 10px;">
                        <div class="product-title">{row['Name']}</div>
                        <div class="product-description">Type: {row['Type']} | Size: {row['Size']}</div>
                        <div class="product-price">Price: RM{row['Price']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                # Order button with a unique key
                if st.button(f"Order {row['Name']}", key=f"order-{row['Menu ID']}-{index}"):
                    st.query_params(page="Menu")  # Navigate to the menu page


# styling
    st.markdown(
        """
        <style>
        .feedback-container {
            text-align: center;
            background-color: #3e2723;
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin: 20px auto;
            max-width: 600px;
        }
        .feedback-container img {
            border-radius: 50%;
            margin-bottom: 20px;
        }
        .feedback-stars {
            color: #ffc107;
            font-size: 1.5em;
            margin: 10px 0;
        }
        .feedback-name {
            font-weight: bold;
            font-size: 1.2em;
            margin-top: 10px;
        }
        .arrow-button {
            background-color: transparent;
            border: none;
            color: #3e2723;
            font-size: 1.5em;
            cursor: pointer;
            padding: 10px;
        }
        .arrow-button:hover {
            color: #ffc107;
        }
            .footer-container {
            background-color: #3e2723;
            color: white;
            padding: 20px;
            font-family: 'Arial', sans-serif;
        }
        .footer-columns {
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
        }
        .footer-column {
            flex: 1;
            padding: 10px;
            text-align: center;
        }

        .footer-column img {
            width: 100%;
            max-width: 100px;
            border-radius: 10px;
        }
        .footer-column h3 {
            font-size: 1.2em;
            font-weight: bold;
        }
        .footer-column p {
            margin: 5px 0;
            line-height: 1.5;
        }
        .subscribe-input {
            padding: 10px;
            width: 80%;
            border: none;
            border-radius: 5px;
            margin-right: 10px;
            outline: none;
        }
        .subscribe-button {
            padding: 10px 15px;
            background-color: #ffc107;
            border: none;
            border-radius: 5px;
            color: #3e2723;
            font-weight: bold;
            cursor: pointer;
        }
        .subscribe-button:hover {
            background-color: #e6a700;
        }
        .footer-social-icons {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 10px;
        }
        .footer-social-icons a {
            color: white;
            font-size: 1.5em;
            text-decoration: none;
        }
        .footer-social-icons a:hover {
            color: #ffc107;
        }
        .footer-copyright {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9em;
            color: #ccc;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def fetch_feedback():
    feedback_data = pd.DataFrame(conn.read(worksheet="Feedback"))  # Replace "Feedback" with your sheet name
    return feedback_data


def display_feedback():
    feedback_data = fetch_feedback()  # Fetch dynamic feedback data

    if "feedback_index" not in st.session_state:
        st.session_state["feedback_index"] = 0

    current_index = st.session_state["feedback_index"]

    with st.expander("What Our Customers Say", expanded=True):
        if not feedback_data.empty:
            # Display feedback dynamically
            current_feedback = feedback_data.iloc[current_index]
            stars = "★" * int(current_feedback["Rating"])

            st.markdown(
                f"""
                <div class="feedback-container">
                    <p>{current_feedback["Feedback"]}</p>
                    <div class="feedback-stars">{stars}</div>
                    <div class="feedback-name">{current_feedback["Name"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Navigation buttons
            col1, col2, col3 = st.columns([1, 6, 1])

            with col1:
                if st.button("⬅", key="prev") and current_index > 0:
                    st.session_state["feedback_index"] -= 1

            with col3:
                if st.button("➡", key="next") and current_index < len(feedback_data) - 1:
                    st.session_state["feedback_index"] += 1
        else:
            st.warning("No feedback available.")

# Footer Content
def display_footer():
    st.markdown(
        """
        <div class="footer-container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>KopiLit</h3>
                    <p>Enjoy better quality coffee with KopiLit.</p>
                </div>
                <div class="footer-column">
                    <h3>Contact Us</h3>
                    <p>Email: KopiLit@gmail.com</p>
                    <p>Call: (+60)12-345678</p>
                    <p>Address: UTP, Seri Iskandar, Perak</p>
                </div>
                <div class="footer-column">
                    <h3>Stay Updated</h3>
                    <form>
                        <input type="email" class="subscribe-input" placeholder="Enter your email address">
                        <button class="subscribe-button" type="submit">Subscribe</button>
                    </form>
                    <div class="footer-social-icons">
                        <a href="#" target="_blank">📘</a>
                        <a href="#" target="_blank">📸</a>
                        <a href="#" target="_blank">🐦</a>
                        <a href="#" target="_blank">📌</a>
                    </div>
                </div>
            </div>
            <div class="footer-copyright">
                © 2023 KopiLit Coffee. All Rights Reserved.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def check_notifications(username):
    try:
        # Load notifications from the Google Sheets
        notifications_data = pd.DataFrame(conn.read(worksheet="Notifications"))

        # Convert the Timestamp column to datetime format
        notifications_data["Timestamp"] = pd.to_datetime(
            notifications_data["Timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
        )
        
        # Filter notifications for today and where the recipient matches the username
        today = datetime.datetime.now().date()
        notifications_data["Timestamp"] = notifications_data["Timestamp"].dt.date
        today_notifications = notifications_data[
            (notifications_data["Timestamp"] == today) & 
            (notifications_data["Recipient"] == username)
        ]

        if not today_notifications.empty:
            # Add an expander to show today's notifications
            with st.sidebar.expander(f"Notifications for {today.strftime('%Y-%m-%d')}"):
                for _, notification in today_notifications.iterrows():
                    st.info(notification["Message"])
        else:
            st.sidebar.info("No notifications for today.")
    except Exception as e:
        st.sidebar.error(f"Error fetching notifications: {e}")


def flow(username):
    # Load user data from Google Sheets
    user_df = pd.DataFrame(conn.read(worksheet="User"))
    user_data = user_df[user_df['Username'] == username]
    first_name = user_data['First Name'].iloc[0]

    # Add sidebar branding
    image_url = "https://i.ibb.co/rbPn1vt/kopilit.png"
    st.sidebar.image(image_url, use_column_width=True)

    # Display notifications
    check_notifications(username)

    # Sidebar navigation options
    st.sidebar.title(f"Hi, {first_name}!")
    navigation = st.sidebar.selectbox("Navigate", ["Home", "Menu", "Orders", "Rewards", "Account"])

    if navigation == "Home":
        display_menu()       
        display_feedback()   
        display_footer()   

    elif navigation == "Menu":
        customer_order.customer_order(username)

    elif navigation == "Orders":
        st.header("Your Orders")
        orders_data = pd.DataFrame(conn.read(worksheet="Order"))
        user_orders = orders_data[orders_data['Username'] == username]
        st.write(user_orders)

    elif navigation == "Rewards":
        st.header("Rewards")
        rewards.customer_rewards(username)

    elif navigation == "Account":
        st.header("Your Account")
        feedback.collect_feedback()


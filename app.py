import streamlit as st
import pandas as pd
from utils.ai_assistant import ask_ai

st.set_page_config(page_title="Membership Manager", layout="centered")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/members.csv")

def save_data(df):
    df.to_csv("data/members.csv", index=False)

df = load_data()

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")
    st.stop()

# Dashboard
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Dashboard", "Add Member", "Record Payment", "AI Assistant"])

if page == "Dashboard":
    st.title("Dashboard")
    emirate_filter = st.selectbox("Filter by Emirate", ["All"] + sorted(df['Emirate'].unique()))
    if emirate_filter == "All":
        st.dataframe(df)
    else:
        st.dataframe(df[df['Emirate'] == emirate_filter])

elif page == "Add Member":
    st.title("Add New Member")
    name = st.text_input("Name")
    emirate = st.selectbox("Emirate", ["Dubai", "Sharjah", "Ajman", "Abu Dhabi", "Al Ain", "Northern Emirates"])
    phone = st.text_input("Phone")
    if st.button("Add Member"):
        new_id = df['MemberID'].max() + 1
        df = pd.concat([df, pd.DataFrame({
            "MemberID": [new_id],
            "Name": [name],
            "Emirate": [emirate],
            "Phone": [phone],
            "Payments": [""]
        })], ignore_index=True)
        save_data(df)
        st.success(f"Added member {name}")

elif page == "Record Payment":
    st.title("Record Payment")
    member_id = st.number_input("Enter Member ID", min_value=1, step=1)
    payment_month = st.text_input("Payment Month (e.g., 2025-04)")
    if st.button("Record Payment"):
        if member_id in df['MemberID'].values:
            idx = df[df['MemberID'] == member_id].index[0]
            payments = df.at[idx, 'Payments']
            if payments:
                payments += f",{payment_month}"
            else:
                payments = payment_month
            df.at[idx, 'Payments'] = payments
            save_data(df)
            st.success("Payment recorded")
        else:
            st.error("Member ID not found")

elif page == "AI Assistant":
    st.title("AI Assistant")
    question = st.text_area("Ask a question about memberships")
    context = df.to_string()
    if st.button("Get Answer"):
        answer = ask_ai(question, context)
        st.write(answer)

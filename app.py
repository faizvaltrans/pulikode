import streamlit as st
import pandas as pd

# Load your data (adjust filename/path if needed)
@st.cache_data
def load_data():
    try:
        # Try Excel first (change path to your actual file)
        df = pd.read_excel('data/members.xlsx')
    except Exception as e:
        st.warning("Excel load failed, trying CSV...")
        try:
            df = pd.read_csv('data/members.csv')
        except Exception as e2:
            st.error("Failed to load data file.")
            st.stop()
    return df

df = load_data()

# Debug: show columns
st.write("Columns in data:", df.columns.tolist())

# Check if 'Emirate' column exists
if 'Emirate' in df.columns:
    emirate_filter = st.selectbox("Filter by Emirate", ["All"] + sorted(df['Emirate'].dropna().unique()))
else:
    st.error("Data file missing 'Emirate' column. Please check your data.")
    st.stop()

# Filter data based on emirate_filter selection
if emirate_filter != "All":
    df = df[df['Emirate'] == emirate_filter]

# Show filtered data (example)
st.dataframe(df)

# Continue your app logic here...

import streamlit as st
import duckdb

# Configure the page layout
st.set_page_config(page_title="Warehouse Dashboard", layout="wide")
st.title("📊 Daily Product Revenue Dashboard")
st.write("This dashboard reads live data directly from our local DuckDB warehouse.")

# Function to fetch data
def load_data():
    # Connect in read-only mode to avoid locking the database while the scheduler is writing to it
    conn = duckdb.connect('data/warehouse.db', read_only=True)
    df = conn.execute("SELECT * FROM daily_product_revenue ORDER BY total_revenue DESC").df()
    conn.close()
    return df

# Fetch the latest data
data = load_data()

# Create two columns for the layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")
    # Streamlit's native bar chart
    st.bar_chart(data, x='product', y='total_revenue', color='#00d4b2')

with col2:
    st.subheader("Raw Warehouse Data")
    # Display the actual dataframe
    st.dataframe(data, use_container_width=True)

# Add a manual refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()
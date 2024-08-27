import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def clean_currency(value):
    """Remove currency symbols and commas from price values."""
    if pd.isna(value):
        return 0.0
    return float(value.replace('KSh ', '').replace(',', '').strip())

def clean_percentage(value):
    """Remove percentage symbols from discount values."""
    if pd.isna(value):
        return 0.0
    return float(value.replace('%', '').strip())

def get_data():
    """Fetch data from the SQLite database and clean it."""
    conn = sqlite3.connect('jumia_products.db')
    query = 'SELECT * FROM products'
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Clean data
    df['current_price'] = df['current_price'].apply(clean_currency)
    df['original_price'] = df['original_price'].apply(clean_currency)
    df['discount_percentage'] = df['discount_percentage'].apply(clean_percentage)

    # Handle missing data
    df = df.fillna({
        'current_price': 0,
        'original_price': 0,
        'discount_percentage': 0,
        'rating': 0,
        'reviews': 0
    })

    return df

def main():
    # Set up the Streamlit app
    st.title('Dashboard made by Analyst Gatitu')
    st.write("Explore and filter the Jumia products data.")

    # Load data
    df = get_data()

    # Sidebar filters
    st.sidebar.header('Filter Options')

    # Price filter
    min_price, max_price = st.sidebar.slider(
        'Select price range',
        float(df['current_price'].min()),
        float(df['current_price'].max()),
        (float(df['current_price'].min()), float(df['current_price'].max()))
    )
    filtered_df = df[(df['current_price'] >= min_price) & (df['current_price'] <= max_price)]

    # Discount filter
    min_discount, max_discount = st.sidebar.slider(
        'Select discount percentage range',
        float(df['discount_percentage'].min()),
        float(df['discount_percentage'].max()),
        (float(df['discount_percentage'].min()), float(df['discount_percentage'].max()))
    )
    filtered_df = filtered_df[(filtered_df['discount_percentage'] >= min_discount) & (filtered_df['discount_percentage'] <= max_discount)]

    # Display filtered data
    st.write(f"Showing {len(filtered_df)} products")
    st.dataframe(filtered_df)

    # Visualization: Price Distribution
    st.subheader('Price Distribution')
    st.bar_chart(filtered_df['current_price'].value_counts().sort_index())

    # Visualization: Discount Distribution
    st.subheader('Discount Distribution')
    st.bar_chart(filtered_df['discount_percentage'].value_counts().sort_index())

    # Visualization: Pie Chart of Discount Distribution
    st.subheader('Discount Percentage Distribution')
    discount_data = filtered_df['discount_percentage'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(discount_data, labels=discount_data.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Discount Percentage Distribution')
    st.pyplot(fig)

    # Visualization: Scatter Plot of Price vs. Discount
    st.subheader('Price vs. Discount Scatter Plot')
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x='current_price', y='discount_percentage', ax=ax)
    ax.set_title('Price vs. Discount')
    st.pyplot(fig)

    # Visualization: Box Plot of Prices by Discount
    st.subheader('Box Plot of Prices by Discount')
    fig, ax = plt.subplots()
    sns.boxplot(data=filtered_df, x='discount_percentage', y='current_price', ax=ax)
    ax.set_title('Box Plot of Prices by Discount Percentage')
    st.pyplot(fig)

    # Visualization: Box Plot of Discount Percentage
    st.subheader('Box Plot of Discount Percentage')
    fig, ax = plt.subplots()
    sns.boxplot(data=filtered_df, y='discount_percentage', ax=ax)
    ax.set_title('Box Plot of Discount Percentage')
    st.pyplot(fig)

if __name__ == '__main__':
    main()


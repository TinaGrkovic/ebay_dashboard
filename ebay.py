import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# Create Streamlit app and display some text
st.title('eBay Data Dashboard')

# Read the csv
df = pd.read_csv('EbayCleanedDataSample.csv')
# Drop first column
df = df.iloc[:, 1:]

# Tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Table", "Average Price per Brand", "Brand Distribution", "Price vs Screen Size", "Price Distribution by Brand"])

# Create Sidebar
st.sidebar.header('Filters')

# Sidebar Filters
def apply_filters(df):
    # Multiselect for Brand
    brands = df['Brand'].unique()
    brand_selection = st.sidebar.multiselect('Select Brand(s):', options=brands, default=brands)

    # Slider for Price
    min_price = 0
    max_price = int(df['Price'].max())
    price_selection = st.sidebar.slider('Select Price Range:', min_value=min_price, max_value=max_price, value=(min_price, max_price))

    # Selectbox for Condition
    conditions = df['Condition'].unique()
    condition_selection = st.sidebar.selectbox('Select Condition:', options=conditions)

    # Apply all filters
    filtered_df = df[
        (df['Brand'].isin(brand_selection)) &
        (df['Price'] >= price_selection[0]) &
        (df['Price'] <= price_selection[1]) &
        (df['Condition'] == condition_selection)
    ]
    return filtered_df

# Apply filters to the dataframe
filtered_df = apply_filters(df)

# Tab 1: Data Table
with tab1:
    # Summary Statistics
    st.write("### Summary Metrics:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Laptops", len(filtered_df))
    with col2:
        st.metric("Average Price", f"${filtered_df['Price'].mean():,.0f}")
    with col3:
        st.metric("Price Range", f"${filtered_df['Price'].min():,.0f} - ${filtered_df['Price'].max():,.0f}")

    # Add most common brand
    common_brand = filtered_df['Brand'].mode()[0]
    a1,col4, a3, col5,a4 = st.columns(5)
    with col4:
        st.metric("Most Common Brand", common_brand)
    with col5:
        st.metric("Unique Brands", len(filtered_df['Brand'].unique()))
    
    # Data Table
    st.subheader('Data Table')
    st.dataframe(filtered_df, height=500)
    
    # Analysis
    st.subheader('Analysis')
    st.write("""This table provides an overview of the eBay dataset, showcasing 
             all key attributes. By applying the filters on the sidebar, the dataset can narrow
             to focus on specific brands, price ranges, or product conditions. The summary metrics 
             provide a quick overview of the dataset. The Total Laptops metric reflects the number 
             of listings available in the filtered dataset. The Average Price gives an indication 
             of the typical price point for the selected filters, helping identify the affordability 
             or premium nature of the products. The Price Range shows the minimum and maximum prices,
              highlighting the breadth of pricing and potential opportunities for targeting different
              customer segments.""")

# Tab 2: Average Price per Brand
with tab2:
    st.subheader('Average Price per Brand')

    # Use all brands from the original dataset for filtering
    all_brands = df['Brand'].unique()
    selected_brands = st.multiselect("Filter by Brand(s):", options=all_brands, default=all_brands)
    
    # Filter based on selected brands in the multiselect
    filtered_data = filtered_df[filtered_df['Brand'].isin(selected_brands)]

    # Bar Chart
    price_per_brand = filtered_data.groupby('Brand')['Price'].mean().sort_values(ascending=False)
    st.bar_chart(price_per_brand)

    # Table Below the Chart
    st.subheader("Data Table")
    formatted_table = price_per_brand.reset_index()
    formatted_table['Price'] = formatted_table['Price'].round(0).astype(int)
    formatted_table.rename(columns={'Price': 'Average Price'}, inplace=True)
    st.table(formatted_table)

    # Overall Trends
    st.metric("Overall Average Price", f"${filtered_df['Price'].mean():,.0f}")

    # Analysis
    st.subheader('Analysis:')
    st.write("""
    This tab provides insights into the average price for each brand. Filtering options allow a focused analysis of specific
    brands, while the bar chart highlights pricing trends across all brands. For instance, premium brands like Razer and ASUS
    dominate the higher price range, whereas budget-friendly brands like SGIN appeal to more cost-conscious consumers. 
    These insights are crucial for competitive pricing and inventory decisions.
    """)

# Tab 3: Brand Distribution Pie
with tab3:
    st.subheader('Brand Distribution')
    brand_counts = filtered_df['Brand'].value_counts().reset_index()
    brand_counts.columns = ['Brand', 'Count']

    # Plot Pie
    fig = px.pie(brand_counts, values='Count', names='Brand')
    st.plotly_chart(fig)

    # Analysis
    st.subheader('Analysis:')
    st.write("""The distribution of brands shows that HP, Lenovo, and Chunghwa are the most prominent in the dataset, 
             indicating their popularity or dominance in the market. This insight can help managers focus on inventory, 
             marketing, or pricing strategies for the leading brands while also evaluating the potential of underrepresented brands.""")

# Tab 4: Price vs Screen Size
with tab4:
    st.subheader('Price vs Screen Size')

    # Convert screen size to numeric values
    filtered_df['Screen Size (in)'] = (filtered_df['Screen Size'].str.extract(r'(\d+\.?\d*)').astype(float))
    
    # Sort by screen size
    filtered_df = filtered_df.sort_values('Screen Size (in)')
    
    # Scatter plot
    fig = px.scatter(filtered_df, x='Screen Size (in)', y='Price', color='Brand', size='Price', hover_name='Model')
    st.plotly_chart(fig)

    # Analysis
    st.subheader('Analysis:')
    st.write("""The scatter plot shows that larger screen sizes, such as 15.6" and 16", are generally associated with higher prices, 
                with premium brands like Dell, ASUS, and Razer dominating this segment. A dense cluster of laptops is visible 
                around 14", priced between 300 and 800 dollars, highlighting this size as a popular and competitive category.""")

# Tab 5: Price Distribution by Brand
with tab5:
    st.subheader('Select a Brand to View Price Distribution')
    selected_brand = st.selectbox('Choose a Brand:', options=filtered_df['Brand'].unique(), key="brand_selection")
    brand_filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
    
    # Compute statistics
    stats = brand_filtered_df['Price'].describe()
    mean_price = brand_filtered_df['Price'].mean()
    
    # Make Plot
    fig = px.box(brand_filtered_df, x='Brand', y='Price', hover_data={
            "Mean": [f"{mean_price:.2f}"] * len(brand_filtered_df),
            "Q1": [f"{stats['25%']:.2f}"] * len(brand_filtered_df),
            "Median": [f"{stats['50%']:.2f}"] * len(brand_filtered_df),
            "Q3": [f"{stats['75%']:.2f}"] * len(brand_filtered_df),
            "Max": [f"{stats['max']:.2f}"] * len(brand_filtered_df),
        })
    st.plotly_chart(fig)

    # Analysis
    st.subheader('Analysis:')
    st.write("""The boxplot highlights the price distribution for selected brands, showcasing their pricing consistency. Narrow interquartile ranges 
indicate consistent pricing, while outliers suggest premium or budget models. Comparing multiple brands helps identify competitive pricing strategies.
""")
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data
file_path = r'E:\coding\data analyst\new project\New folder\dicoding\PRSA_Data_Changping_20130301-20170228.csv'

air_pollution_df = pd.read_csv(file_path)

# Data Cleaning
columns_to_replace = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
for column in columns_to_replace:
    column_mean = air_pollution_df[column].mean()
    air_pollution_df[column].fillna(column_mean, inplace=True)

# Streamlit Dashboard
st.title("Air Pollution Analysis Dashboard")
st.sidebar.title("analisis kualitas udara changping")

# Sidebar options
selected_option = st.sidebar.radio("Select Analysis", ["PM10 Over the Years", "Pollutants Exceeding WHO Standards"])

# Analysis 1: PM10 Over the Years
if selected_option == "PM10 Over the Years":
    st.header("PM10 Over the Years")
    plt.figure(figsize=(15, 6))
    sns.lineplot(x='year', y='PM10', data=air_pollution_df)
    plt.title('PM10 over the year')
    plt.xlabel('Year')
    plt.ylabel('PM10 Pollutant')
    st.pyplot(plt)

# Analysis 2: Pollutants Exceeding WHO Standards
elif selected_option == "Pollutants Exceeding WHO Standards":
    st.header("Pollutants Exceeding WHO Standards")

    # Visualize pollutants exceeding WHO standards
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    fig, axes = plt.subplots(nrows=len(pollutants), figsize=(12, 6 * len(pollutants)))

    for i, pollutant in enumerate(pollutants):
        max_concentration_per_year = air_pollution_df.groupby(['year', 'station'])[pollutant].max().reset_index()
        heatmap_data = max_concentration_per_year.pivot_table(index='year', columns='station', values=pollutant, aggfunc='max')

        sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f", linewidths=.5, ax=axes[i])
        axes[i].set_title(f'Station with the Highest {pollutant} Concentration Each Year')

    plt.tight_layout()
    st.pyplot(plt)

# Conclusion
st.sidebar.header("Conclusion")
if selected_option == "PM10 Over the Years":
    st.sidebar.markdown(
        """
        **Conclusion for PM10 Over the Years:**
        The graph shows a general trend of decreasing PM10 levels over the two-year period. The highest PM10 level is 104 µg/m³ in 2013, 
        and the lowest level is 84 µg/m³ in 2015. The graph also shows some seasonal variation, with PM10 levels being higher in the 
        winter months and lower in the summer months.
        """
    )
elif selected_option == "Pollutants Exceeding WHO Standards":
    st.sidebar.markdown(
        """
        **Conclusion for Pollutants Exceeding WHO Standards:**
        The PM2.5 pollution level in Changping is still significantly above the standards set by the World Health Organization (WHO). 
        WHO recommends that the annual PM2.5 level should not exceed 10 micrograms per cubic meter (µg/m³). The annual PM2.5 level 
        in Changping averages 45.8 µg/m³ in 2023.
        """
    )

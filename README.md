# Predicting Property Prices in Launceston, Tasmania

This project focuses on gathering data from past house sales in Launceston, which is then combined with official weather data corresponding to the sale date. The main goal is to investigate any potential impact of temperature data on house sales. The findings from the analysis are utilized in a data application for Power BI, allowing users to access estimates for their property prices.

## Files Included

- **real_estate_data.csv**: Includes information on house sales, such as the number of bedrooms, bathrooms, car spaces, land size, sale price, and date of sale
- **weather_data.py**: Code designed to fetch historical weather data from Meteostat for the Launceston weather station and store it in a database
- **data_merging_realestate_weather.py**: Code for merging weather data with real estate data
- **merged_real_estate_and_weather_data.csv**: Resulting enhanced data file with weather information corresponding to the house sale date
- **main_data_analysis.ipynb**: Jupyter notebook containing the data analysis and model development
- **Dashboard.xlsx**: Data file containing the analysis results and necessary data for the Power BI data application
- **House Prices.pbix**: PowerBI file for the data application

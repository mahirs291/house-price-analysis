import pandas as pd
import sqlite3

# Read real estate data from CSV
real_estate_data = pd.read_csv('real_estate_data.csv')

# Define a dictionary mapping column names to data types
column_data_types = {
    'date of sale': 'datetime64[ns]',
    'bedrooms': int,
    'bathrooms': int,
    'car spaces': int,
    'land size': int,
    'price': int
}

# Convert columns to specified data types using the dictionary
real_estate_data = real_estate_data.astype(column_data_types)

# Connect to SQLite database
conn = sqlite3.connect('weather_data.db')

# Define the SQL query to select the original weather columns for merging
sql_query_original = """
SELECT "time", "tavg", "tmin", "tmax"
FROM weather_data;
"""

# Execute the SQL query to fetch the original weather data
weather_data_original = pd.read_sql_query(sql_query_original, conn)

# Convert 'time' column to datetime format
weather_data_original['time'] = pd.to_datetime(weather_data_original['time'])

# Define an empty DataFrame to store the final merged data
merged_real_estate_and_weather_data = real_estate_data.copy()

# Merge the original weather data with the real estate data
merged_real_estate_and_weather_data = pd.merge(merged_real_estate_and_weather_data, weather_data_original,
                                               left_on='date of sale', right_on='time', how='left')

# Define the SQL query to calculate the 7-day and 30-day averages for each column
for days in [7, 30]:
    sql_query = f"""
    WITH numbered_data AS (
        SELECT *,
               ROW_NUMBER() OVER (ORDER BY "time") AS rn
        FROM weather_data
    ),
    averages_{days} AS (
        SELECT nd1."time",
               ROUND(AVG(nd2."tavg"), 1) AS avg_tavg_{days}_days,
               ROUND(AVG(nd2."tmin"), 1) AS avg_tmin_{days}_days,
               ROUND(AVG(nd2."tmax"), 1) AS avg_tmax_{days}_days
        FROM numbered_data nd1
        JOIN numbered_data nd2 ON nd1.rn - nd2.rn BETWEEN 1 AND {days}
        GROUP BY nd1."time"
    )
    SELECT a."time", a.avg_tavg_{days}_days, a.avg_tmin_{days}_days, a.avg_tmax_{days}_days
    FROM weather_data wd
    JOIN averages_{days} a ON wd."time" = a."time";
    """

    # Execute the SQL query to calculate the averages
    weather_data_averages = pd.read_sql_query(sql_query, conn)

    # Convert 'time' column to datetime format
    weather_data_averages['time'] = pd.to_datetime(weather_data_averages['time'])

    # Merge the calculated averages with the final merged data
    merged_real_estate_and_weather_data = pd.merge(merged_real_estate_and_weather_data, weather_data_averages,
                                                   left_on='date of sale', right_on='time', how='left')

# Select only the desired columns in the final output
merged_real_estate_and_weather_data = merged_real_estate_and_weather_data[
    ['bedrooms', 'bathrooms', 'car spaces', 'land size', 'price', 'date of sale', 'tavg', 'tmin', 'tmax',
     'avg_tavg_7_days', 'avg_tmin_7_days', 'avg_tmax_7_days', 'avg_tavg_30_days', 'avg_tmin_30_days',
     'avg_tmax_30_days']]

# Save the final dataframe to a CSV file
merged_real_estate_and_weather_data.to_csv('merged_real_estate_and_weather_data.csv', index=False)

# Close the database connection
conn.close()

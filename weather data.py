# Import Meteostat library and dependencies
from datetime import datetime
from meteostat import Point, Daily
import sqlite3

# Set time period for data retrieval
start = datetime(2005, 1, 1)
end = datetime.now()

# Create Point for Launceston, TAS to fetch weather data
launceston = Point(-41.4167, 147.1167)

# Get daily weather data from 01.01.2005 to today for Launceston
data = Daily(launceston, start, end)
data = data.fetch()

# Reset the index to convert the index (time) into a regular column
data.reset_index(inplace=True)

# Remove leading and trailing whitespaces from column names
data.columns = data.columns.str.strip()

# Drop columns that are not needed for analysis
columns_to_drop = ['snow', 'wpgt', 'pres', 'wdir', 'wspd', 'tsun']
data = data.drop(columns=columns_to_drop, errors='ignore')

# Define the data types for each column in the DataFrame
data_types = {
    'time': 'datetime64[ns]',
    'tavg': 'float64',
    'tmin': 'float64',
    'tmax': 'float64',
    'prcp': 'float64',
}

# Convert data types in the DataFrame for consistency
data = data.astype(data_types)

# Save the weather data to a SQLite database
conn = sqlite3.connect('weather_data.db')
data.to_sql('weather_data', conn, if_exists='replace', index=False)
conn.close()

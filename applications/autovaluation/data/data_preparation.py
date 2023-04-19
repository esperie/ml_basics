import config
import pickle
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport

# This flow is how we code in Jupyter notebook:

# Step 1: Data sourcing and ETL
# ## Load the data from source
data = pd.read_csv(config.DATA_PATH / 'housing_transactions.csv')

# Step 2: Exploratory Data Analysis
# ## Export profile report for analysis
initial_profile = ProfileReport(data)
initial_profile.to_file(
	config.DATA_PATH / 'autovaluation_initial_profile.html')

# Step 3: Data Preparation
# ## Rename columns to make it easier to wrangle via Pandas
column_map = {
	'Project Name': 'project_name', 'Address': 'address',
	'No. of Units': 'num_units', 'Area (sqm)': 'area_sqm',
	'Type of Area': 'area_type',
	'Transacted Price ($)': 'total_price', 'Nett Price($)': 'nett_price',
	'Unit Price ($ psm)': 'price_psm',
	'Unit Price ($ psf)': 'price_psf', 'Sale Date': 'sale_date',
	'Property Type': 'property_type', 'Tenure': 'tenure',
	'Completion Date': 'completion_date', 'Type of Sale': 'sale_type',
	'Purchaser Address Indicator': 'purchaser_address',
	'Postal District': 'postal_district', 'Postal Sector': 'postal_sector',
	'Postal Code': 'postal_code', 'Planning Region': 'planning_region',
	'Planning Area': 'planning_area'
}

data.rename(column_map, axis=1, inplace=True)

# ## More Data Cleaning
# ## Enbloc and block purchases do not accurately reflect the price that most
# ## purchasers face, thus we should remove observations with no_of_units more
# ## than 1
data = data[data.num_units == 1]

# ## Remove landed properties since their purchase is restricted to residents,
# ## while foreigners can still buy condominiums and apartments (non-landed).
data = data[data.property_type.isin(
	['Condominium', 'Apartment', 'Executive Condominium'])]

# ## Remove Unknown in completion date and set the year to 2023 for Uncompleted
data = data[data.completion_date != 'Unknown']

# ## All uncompleted units will have its year set to 2023
data['completion_date'] = data.completion_date.apply(
	lambda x: 2023 if not x[0].isdigit() else int(x))

# ## Convert sale date to a proper datetime form
data['sale_date'] = data.sale_date.apply(pd.to_datetime)

# ## Create a reference date, where the earliest date in the dataset is 0 and
# ## each subsequent date increases by 1

# ## This will allow decision trees to group observations by dates in a very
# ## fine manner - Trend capturing.

# ## First get a de-duplicated list of sale date, then sort them, followed by
# ## incrementing the date using i += 1 for each consecutive date
dates = sorted(data.sale_date.drop_duplicates())

# ## Use enumerate to create an id mapped to each date
date_dict = {dt: idx for idx, dt in enumerate(dates)}
# ## Save this engineered feature to map for model prediction
with open(config.DATA_PATH / 'date_dict.pkl', 'wb') as f:
	pickle.dump(date_dict, f)

with open(config.DATA_PATH / 'date_dict.pkl', 'rb') as f:
	date_dict = pickle.load(f)

# ## Apply the date dictionary to the dataframe and call this date feature
# ## date_id.
data['date_id'] = data.sale_date.apply(lambda x: date_dict[x])

# ## Create leasehold/freehold dummy
# ## First, check what are the various tenures in the dataset
data.tenure.apply(lambda x: x.split(' ')[0]).value_counts()


# ## Wrangling this field is more complex than a single line function, so we
# ## need to write a def before applying it
def is_leasehold(tenure):
	tenure = tenure.split(' ')[0]
	if tenure in ('Freehold', 'N.A.'):
		return 0
	elif int(tenure) <= 99:
		return 1
	else:
		return 0


# ## Apply the function to the tenure column
data['is_leasehold'] = data.tenure.apply(is_leasehold)

# ## Merge lat/lon data to postal code
# ## First, read the postal code - lat/lon dataset
postal_lat_lon = pd.read_csv(config.DATA_PATH / 'postal_lat_lon.csv')

# ## Then merge lat lon to main dataset via postal codes using how='left'
data = pd.merge(data, postal_lat_lon, on='postal_code', how='left')

# ## Final step, drop all missing values due to missing postal coords
data.dropna(inplace=True)

# ## Do a final check on the summary statistics to complete the data prep
final_profile = ProfileReport(data)
final_profile.to_file(config.DATA_PATH / 'autovaluation_final_profile.html')

# ## Save the file for training
data.to_parquet(config.DATA_PATH / 'prepped_data.parquet')

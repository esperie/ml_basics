import config
import pickle
import pandas as pd
from fastapi import APIRouter
from config import setup_logger  # initialize_django
from applications.autovaluation.schemas import QueryBase

from pycaret.regression import *

# initialize_django()

logger = setup_logger(
	'autovaluation_requests', logfile='autovaluation_requests.log')

# Create FastAPI instance
app = APIRouter()

# Load the trained model
loaded_model = load_model(config.MODELS_PATH / 'autovaluation_model')
print(loaded_model)


@app.post('/predict')
def predict(query: QueryBase):
	# Convert the query into a dictionary to feed into the model
	query_dict = query.dict()

	# Need to convert postal code into
	# ## postal district, postal sector, lat, lon, planning region, planning area
	postal_code = query_dict.pop()

	# todo: extract sector, find district, lat-lon, planning region, and area from onemap api

	# Get date_id from sale_date
	with open(config.DATA_PATH / 'date_dict.pkl', 'rb') as f:
		date_dict = pickle.load(f)

	query_dict['date_id'] = date_dict[query.sale_date]

	# Use the query and engineered feature to predict the value
	predicted_value = loaded_model.predict(pd.DataFrame([query_dict]))

	# Log the request
	logger.log(
		level=20,
		msg=(
			f'Endpoint: /predict | '
			f'POST request: {query.dict()} | '
			f'Predicted value: {predicted_value}'))

	return {'estimated_psf': predicted_value}

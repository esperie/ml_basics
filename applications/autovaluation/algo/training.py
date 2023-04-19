import pandas as pd
from datetime import datetime, date, time, timedelta
from pycaret.regression import RegressionExperiment

import config

# Retrieve the prepped data
data = pd.read_parquet(config.DATA_PATH / 'prepped_data.parquet')

# Setup the experiment
s = RegressionExperiment()
s.setup(data, target='price_psf',
        ignore_features=['project_name', 'address', 'num_units',
                         'transacted_price', 'nett_price', 'price_psm',
                         'tenure', 'postal_code'],
        date_features=['sale_date'],
        normalize=True,
        log_experiment=True,
        experiment_name=f'autovaluation_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        )

# Compare the performance of all the models and select the best one
best = s.compare_models()

# Check the 10-fold cross validation results of the best model
s.create_model('catboost')

# Inspect the feature importance to see if we can craft a sensible story
s.plot_model(best, plot='feature', save=True)

# check the residuals of trained model to see how are the errors clustered
s.plot_model(best, plot='residuals_interactive', save=True)

# check the learning curve to have a sense of the over and underfitting issues
s.plot_model(best, plot='learning', save=True)

# Check the shap values to see how each feature contributes to the prediction
s.interpret_model(best, save=True)

# Test the model on the holdout set
s.predict_model(best)

# Hyperparameter tuning to gain some extra performance out of the best model
tuned_model = s.tune_model(
	best,
	choose_better=True,
	search_library='optuna',
	n_iter=100,
	optimize='MAPE',
	early_stopping=True
)

# Finalize the model with all data
final_model = s.finalize_model(best)

# Save the trained model for future deployment
s.save_model(final_model, config.MODELS_PATH / 'autovaluation_model')

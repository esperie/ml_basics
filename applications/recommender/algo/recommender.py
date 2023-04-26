import pandas as pd

import config


# Supervised ML
# ## What characteristics/fingerprint of an artist is likely to win a grammys
# ## Collect the list of artists who have won a grammys
# ## Use that as an outcome, use the NMF features as the features, and
# ## train a supervised ML model

# todo: Please complete this exercise.

# Propensity Matching


def recommend_most_similar_artists(nmf_feature_df, target_name,
                                   n_recommendations=10):
	nmf_values = nmf_features.loc[target_name]
	similarity_scores = nmf_feature_df.dot(nmf_values)
	print(similarity_scores.nlargest(n_recommendations))
	return similarity_scores.nlargest(n_recommendations)


if __name__ == '__main__':
	# Load the NMF trained features
	nmf_features = pd.read_parquet(config.MODELS_PATH / 'nmf_features.parquet')

	# Check the list of artists that is in the dataset
	list_of_artists = nmf_features.index

	# List of artists we want to test
	artists = ['周杰倫', 'Imagine Dragons', 'فريد الاطرش', 'Руки Вверх']

	recommend_most_similar_artists(nmf_features, artists[3], 20)

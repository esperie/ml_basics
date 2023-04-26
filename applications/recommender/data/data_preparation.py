import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MaxAbsScaler, Normalizer

import config

# Load data
spotify_filename = 'spotify.csv'
spotify_data = pd.read_csv(config.DATA_PATH / spotify_filename)

spotify_data.set_index('artistname', inplace=True)

# Process data
sparse_data = csr_matrix(spotify_data)  # Convert to sparse matrix

# NMF model with pre and post processing
mas = MaxAbsScaler()
nmf = NMF(n_components=20)
nml = Normalizer()

pipeline = make_pipeline(mas, nmf, nml)

nmf_features = pipeline.fit_transform(sparse_data)
nmf_df = pd.DataFrame(nmf_features, index=spotify_data.index)

nmf_df.columns = [f'component_{i}' for i in range(20)]
nmf_df.to_parquet(config.MODELS_PATH / 'nmf_features.parquet')

import numpy as np
import hdbscan
import _pickle as pickle
import gzip


compressed_file = gzip.GzipFile('array.npy.gz', "r")
array = np.load(compressed_file)

clusterer = hdbscan.HDBSCAN(
    prediction_data=True, min_samples=1, min_cluster_size=5,
    cluster_selection_method='eom')

model = clusterer.fit(array)

print(clusterer.labels_)
print(clusterer.labels_.max())


def save_zipped_pickle(obj, filename, protocol=4):
    with gzip.open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol)


save_zipped_pickle(model, "model.bin")

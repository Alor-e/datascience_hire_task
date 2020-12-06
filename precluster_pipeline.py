import _pickle as pickle
import gzip
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.feature_selection import VarianceThreshold

training_data = pd.read_csv('csv_files/training.csv')


def pipeline(column_name):
    """
    Converts text from pandas columns into vectors.
    """
    vectorizer = TfidfVectorizer()
    vectorized_text = vectorizer.fit_transform(
        training_data[column_name].values.astype('U')).toarray()
    return vectorized_text


def pipeline_pickler(column_name):
    """
    Pickles a trained vectorizer.
    """
    vectorizer = TfidfVectorizer()
    vectorized_text = vectorizer.fit(
        training_data[column_name].values.astype('U'))
    pickle.dump(vectorized_text, open(
        f'{column_name}_vectorizer.bin', 'wb'), protocol=4)


def variance_selector_pickler(array_tuple):
    """
    Pickles a trained variance selector.
    """
    joined_array = np.column_stack(array_tuple)
    sel = VarianceThreshold(threshold=(.999 * (1 - .99999)))
    variance_selector = sel.fit(joined_array)
    pickle.dump(variance_selector, open(
        'variance_threshold.bin', 'wb'), protocol=4)


name_array = pipeline('product_name')
type_array = pipeline('product_type')

combined_array = np.column_stack(
    (name_array, type_array))

sel = VarianceThreshold(threshold=(.999 * (1 - .99999)))
reduced_array = sel.fit_transform(combined_array)
reduced_array = normalize(reduced_array, norm='l2')
print(reduced_array.shape)

f = gzip.GzipFile("array.npy.gz", "w")
np.save(f, reduced_array)
f.close()

array_tuple = (name_array, type_array)

pipeline_pickler('product_name')
pipeline_pickler('product_type')
variance_selector_pickler(array_tuple)

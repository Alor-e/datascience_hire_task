import _pickle as pickle
import gzip
import hdbscan
from sql_database import fetch_cluster_rows
from api_gen_helpers import list_of_dict, page_scraper, pipeline


def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object


clusterer = load_zipped_pickle('model.bin')


def links_recommender(link):
    """
    Accepts url links and passes it to various helper functionsto get a vector.
    Passes the vector to a pretrained clusterer.
    Returns recommendations.
    """
    page_tuple = page_scraper(link)
    array = pipeline(page_tuple)
    cluster_prediction = hdbscan.prediction.approximate_predict(
        clusterer, array)
    if cluster_prediction[0][0] != -1:
        cluster_list = clusterer.labels_.tolist()
        indices = [i for i, x in enumerate(
            cluster_list) if x == cluster_prediction[0][0]]
        cluster_members = fetch_cluster_rows(indices)
        cluster_members_json = list_of_dict(cluster_members)
        return cluster_members_json
    else:
        return{'status': 'No recommendations are available for the given link'}

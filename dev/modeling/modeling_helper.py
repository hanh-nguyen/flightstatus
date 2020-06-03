import pandas as pd
from keras.utils.np_utils import to_categorical


def search_result(searchcv):
    result = pd.DataFrame.from_dict(searchcv.cv_results_['params'])
    result['mean_score'] = searchcv.cv_results_['mean_test_score']
    result['std_score'] = searchcv.cv_results_['std_test_score']
    return result.sort_values('mean_score', ascending=False)


def create_xy(data):
    return data.drop(['TARGET'], axis=1), data['TARGET']


def transform_xy(data):
    return (data.drop(['TARGET'], axis=1)).as_matrix(), to_categorical(data['TARGET'])

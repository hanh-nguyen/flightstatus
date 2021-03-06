import pandas as pd
import numpy as np
from keras.utils.np_utils import to_categorical
from sklearn.metrics import classification_report, SCORERS, roc_curve, auc, precision_recall_curve, make_scorer
import matplotlib.pyplot as plt


def search_result(searchcv):
    result = pd.DataFrame.from_dict(searchcv.cv_results_['params'])
    result['mean_score'] = searchcv.cv_results_['mean_test_score']
    result['std_score'] = searchcv.cv_results_['std_test_score']
    return result.sort_values('mean_score', ascending=False)


def create_xy(data):
    return data.drop(['TARGET'], axis=1), data['TARGET']


def transform_xy(data):
    return (data.drop(['TARGET'], axis=1)).to_numpy(), to_categorical(data['TARGET'])


def get_roc(y_actual, y_pred, plotting=False):
    fpr, tpr, _ = roc_curve(y_actual, y_pred)
    roc_auc = auc(fpr, tpr)
    if plotting:
        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2,
                 label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.show()
    return roc_auc


def optimize_threshold(y_actual, y_pred):
    fpr, tpr, thresholds = roc_curve(y_actual, y_pred)
    opt_idx = np.argmin(np.sqrt(np.square(1-tpr) + np.square(fpr)))
    opt_threshold = thresholds[opt_idx]
    return opt_threshold


def get_important_feature(features, scores):
    return pd.DataFrame({'feature': features, 'importance_score': scores}).sort_values('importance_score', ascending=False)


def pr_auc_score(y_true, y_score):
    """
    Generates the Area Under the Curve for precision and recall.
    """
    precision, recall, thresholds = precision_recall_curve(
        y_true, y_score[:, 1])
    return auc(recall, precision, reorder=True)


pr_auc_scorer = make_scorer(
    pr_auc_score, greater_is_better=True, needs_proba=True)

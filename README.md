## Flight Status
*Which airline should you fly on to avoid significant delays or cancelations?*

---

### The Data

The flight delay and cancellation data were collected and published by the US Department of Transportation - Bureau of Transportation Statistics, and made publicly available on [Kaggle](https://www.kaggle.com/usdot/flight-delays).

The data processing steps were put into a reproducible analysis toolkit and a unit test suite.

### The performance metrics

I wanted to predict flight cancelation and delays (more than 15 minutes).

Three factors are taken into consideration
- This is a classification problem and I am intesterested in probabilities. Knowing the ranking will allow us to pick the one with the highest likelihood of being on-time if we are considering two or more flight options.
- The dataset is slightly imbalanced (35% of data are of the positive class).
- The false negative result is more important (it is more costly to predict a delayed or cancelled flight incorrectly).

I decided to use ROC and Precision-Recall curve (PRC) for model evaluation.


### The Predictive Models

I built different models to predict flight cancelation and delays (more than 15 minutes) based on airlines and travel routes. A dummy classifier model (`sklearn.dummy`) was used for comparison.

* __XGBoost__: I run random search and grid search for hyperparameter tuning, including `max_depth`, `min_child_weight`, `subsample`, `colsample_bytree`, `learning_rate`. `scale_pos_weight` was set at 1.9 to reflect the negative and positive class ratio. Precision-Recall Area Under a Curve (PR-AUC) was used when fitting the model (`eval_metric = 'aucpr'` as well as tuning hyperparameters (`scoring = 'average_precision'`) 
* __Neural Network__: I experimented with different architectures by starting with a small network and gradually increasing the model capacity until the validation score is no longer improving (PR-AUC). The models include fully connected hidden layers, a dropout layer to reduce overfitting, and an output softmax layer. Similar to XGBoost's `early_stopping_round` and `scale_pos_weight`, I set up an early stopping monitor `EarlyStopping(patience=5)` and `class_weight={0:1., 1:1.9}`.

I also tried two approaches for splitting the train-validation-test data. The first approach is splitting by the months: from January to June for training, from July to September for validation and October to December for test. The second approach is randomly splitting using `train_test_split` with `stratify` from `sklearn`. The second approach resulted in higher model performance (10%), potentially because the trained model could learn some seasonal patterns throughout the whole year in the train and validation sets.

Both XGBoost and Neural Network models performed better than the dummy model. 

|  ROC-AUC   |          |         |                |
| :--------: | :------: | :-----: | :------------: |
|            | Baseline | XGBoost | Neural Network |
|   Train    |   0.50   |  0.73   |      0.66      |
| Validation |   0.50   |  0.72   |      0.66      |
|    Test    |   0.50   |  0.72   |      0.66      |

|   PR-AUC   |          |         |                |
| :--------: | :------: | :-----: | :------------: |
|            | Baseline | XGBoost | Neural Network |
|   Train    |   0.46   |  0.60   |      0.51      |
| Validation |   0.46   |  0.59   |      0.47      |
|    Test    |   0.46   |  0.59   |      0.50      |

The top features selected are the scheduled departure time, airline, and flight length. Flight delays and cancellations have several causes: weather, security, late aircraft, etc. Therefore, in order to improve the model performance, I will need to collect more useful information.

To reproduce the models, follow the [Instructions](#instructions) section. 

### Instructions

* Clone the repository

``` shell
git clone https://github.com/hanh-nguyen/flightstatus
cd flightstatus
```

* Download the data from [Kaggle](https://www.kaggle.com/usdot/flight-delays) and save to

```
./data
```

* Install dependencies

``` shell
python -m pip install -r requirements.txt
```

* Run unit tests

``` shell
cd test
pytest
```

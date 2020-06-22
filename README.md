## Flight Status
*Which airline(s) should you fly on to avoid significant delays or cancelations?*

---

### The Data

The flight delay and cancellation data were collected and published by the US Department of Transportation - Bureau of Transportation Statistics, and made publicly available on [Kaggle](https://www.kaggle.com/usdot/flight-delays).

The data processing steps were put into a reproducible analytical toolkit. A unit test suite is also included.

### The performance metrics

I wanted to predict flight cancelation and delays (more than 15 minutes). Three factors were taken into consideration:
- This is a classification problem and we are intesterested in probabilities. When considering two or more flight options, knowing the ranking will allow us to pick the option with the highest likelihood of being on-time.
- The dataset is slightly imbalanced (35% of the data are of the positive class).
- The false negative results are more important than the false positive results--it is more costly to predict a delayed or cancelled flight incorrectly compared to predicting an on-time flight incorrectly.

I decided to use ROC and Precision-Recall Curve (PRC) for model evaluation.


### The Predictive Models

I built different models to predict flight cancelation and delays (more than 15 minutes) based on airlines and travel routes. A dummy classifier model (`sklearn.dummy`) was used for comparison.

* __XGBoost__: I ran random search and grid search for hyperparameter tuning, including `max_depth`, `min_child_weight`, `subsample`, `colsample_bytree`, and `learning_rate`. The `scale_pos_weight` was set at 1.9 to reflect the negative and positive class ratio. Precision-Recall Area Under a Curve (PR-AUC) was used when fitting the model (`eval_metric = 'aucpr'`) as well as tuning hyperparameters (`scoring = 'average_precision'`) 
* __Neural Network__: I experimented with different architectures by starting with a small network and gradually increasing the model capacity until the validation score was no longer improving (PR-AUC). The models include fully connected hidden layers, a dropout layer to reduce overfitting, and an output softmax layer. Similar to XGBoost's `early_stopping_round` and `scale_pos_weight`, I set up an early stopping monitor `EarlyStopping(patience=5)` and `class_weight={0:1., 1:1.9}`.

I also tried two approaches for splitting the train-validation-test data. The first approach was splitting by months of the year: from January to June for training, from July to September for validation, and October to December for testing. The second approach was randomly splitting using `train_test_split` with `stratify` from `sklearn`. The second approach resulted in higher model performance (10%), potentially because the trained model could learn some seasonal patterns throughout the whole year in the train and validation sets.

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

The top features selected are the scheduled arrival time, airline, month of the year, and flight distance. Flight delays and cancellations have several causes: weather, security, late aircraft, etc. Therefore, in order to improve the model's performance, we would need to collect more extensive information.

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

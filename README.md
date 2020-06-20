## Flight Status
*Which airline should you fly on to avoid significant delays or cancelations?*

---

### The Data

The flight delay and cancellation data was collected and published by the US Department of Transportation - Bureau of Transportation Statistics, and made publicly available on [Kaggle](https://www.kaggle.com/usdot/flight-delays).

Data were processed as follows: 
- categorize categorical variables
- remove constant variables
- create new features such as airport or airline traffic through aggregation

The data processing steps were put into a reproducible analysis toolkit and a unit test suite.

### The performance metrics

I want to predict flight cancelation and delays (more than 15 minutes).

Three factors are taken into considerations
- This is a classification problem and I need to predict both probabilities and class labels
- The dataset is imbalanced (35% of data are of the positive class)
- The false negative result is more important (it is more costly to predict a delayed or cancelled flight incorrectly)

I decided to use Precision-Recall Area Under a Curve (PR-AUC) for model evaluation.

### The Predictive Models

I built different models to predict flight cancelation and delays (more than 15 minutes) based on airlines and travel routes. A baseline model (predicting all flights are delayed or cancelled) is also used for comparison.

* XGBoost: run random search and grid search for hyperparameter tuning
* Neural Network: experiment with different architectures, use dropout for regularization.

Both XGBoost and Neural Network models do not perform as well as the baseline model. Having said that, a predictive model allows us to get the probability prediction if we are considering two flight options and want to pick the one with higher likelihood of being on-time. The top features selected are the scheduled departure time, airline, and flight length. Flight delays and cancellations have several causes: weather, security, late aircraft, etc. Therefore, I will need to gather more useful information for the next round of modeling.

|            |  PR-AUC  |         |                |
| :--------: | :------: | :-----: | :------------: |
|            | Baseline | XGBoost | Neural Network |
|   Train    |   0.68   |  0.54   |      0.48      |
| Validation |   0.66   |  0.49   |      0.46      |
|    Test    |   0.67   |  0.52   |      0.47      |

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

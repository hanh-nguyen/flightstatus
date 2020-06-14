## Flight Status
*Which airline should you fly on to avoid significant delays or cancelations?*

---

### The Predictive Models

I built different models to predict flight cancelation and delays (more than 15 minutes) based on airlines and travel routes.

* XGBoost: run random search and grid search for hyperparameter tuning
* Neural Network: experiment with different architectures, use dropout for regularization.

To reproduce the models, follow the [Instructions](#instructions) section.

### The Data

The flight delay and cancellation data was collected and published by the US Department of Transportation - Bureau of Transportation Statistics, and made publicly available on [Kaggle](https://www.kaggle.com/usdot/flight-delays).

Data were processed as follows: 
- categorize categorical variables
- remove constant variables
- create new features such as airport or airline traffic through aggregation

The data processing steps were put into a reproducible analysis toolkit and a unit test suite.

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
python -m pip install requirements.txt
```

* Run unit tests

``` shell
cd test
pytest
```

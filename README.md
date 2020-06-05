# flightstatus

The flight delay and cancellation data was collected and published by the DOT's Bureau of Transportation Statistics. Go to https://www.kaggle.com/usdot/flight-delays to download the data.

I built different models to predict flight cancelation and delay (more than 15 minutes).
- XGBoost: run random search and grid search for hyperparameter tuning
- Neural Network: experiment with different architectures, use dropout for regularization.

I also created a portable package. To install the package, first clone the repo and run:

    pip install .


A unit test suite with Pytest has been developed. To run the tests:

    cd test
    pytest


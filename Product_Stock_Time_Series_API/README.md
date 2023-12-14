# Product Stock Time Series API

## Description

This is an API applicaton we use to deploy the product stock time series model.

We use flask because it uses python that provides extensive support of machine learning library like TensorFlow.

To get product stock prediction, send POST request along with JSON input data that contains sequences of product stock history data. The API will then receive the data and preprocess it to predict future values of product stock. Lastly, it will return the prediction along with previous input data in JSON format.

This API has 2 version, the first one `/predict` will only predict one future value which means only the next day. While the second version `/predict_v2`, will predict the next 30 days. But the longer day it predict the less accurate it become.

This directory also contains 2 examples: `request.py` which shows how to send POST request to API and `visualization.html` which shows the visualization of predicted values.

## Installation

1. Clone the repository

```bash
git clone https://github.com/C23-GT02/Machine-Learning.git
```

2. Create environment and install dependencies

```bash
cd Machine-Learning/Product_Stock_Time_Series_API

python -m venv env

source env/activate.sh

pip install -r requirements.txt
```

3. Get the saved model and the scaler params on `Product_Stock_Time_Series_Model`

```bash
cp ../Product_Stock_Time_Series_Model/lstm_model.h5 ../Product_Stock_Time_Series_Model/scaler_params.npy .
```

## Usage

1. Run the app

```bash
python app.py
```

# Product Stock Time Series Model

## Description

This is a time series model to predict product stock for SMEs to improve supply chain management.

We use syntetic data by generating the sequences of values with custom trend, seasonality, noise, autocorrelation, and impulse. Then we saved the generated data in JSON file format.

For the model, we use Long Short-Term Memory (LSTM) to train the model. The advantage of LSTM is it can capture and remember information over longer sequences.

## Installation

1. Clone the repository

```bash
git clone https://github.com/C23-GT02/Machine-Learning.git
```

2. Create environment and install dependencies

```bash
cd Machine-Learning

python -m venv env

source env/activate.sh

pip install -r requirements.txt
```

## Usage

1. Move Directory

```bash
cd Product_Stock_Time_Series_Model
```

2. Open the corresponding notebook with Visual Studio Code or Jupyter Notebook

```bash
code .
```

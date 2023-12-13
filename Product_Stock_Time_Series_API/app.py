import json
from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Load the trained LSTM model
model = tf.keras.models.load_model('lstm_model.h5')

# Load the scaler used during training
scaler = MinMaxScaler()
scaler.min_, scaler.scale_ = np.load('scaler_params.npy')

# Use the same sequence length as used during training
sequence_length_api = 10


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        input_data = request.json.get('data')
        if input_data is None:
            return jsonify({'error': 'Missing "data" key in the request payload'})

        # Preprocess the input data
        preprocessed_data = np.array(input_data).reshape(-1, 1)
        scaled_data = scaler.transform(preprocessed_data)

        # Adjust the sequence length
        reshaped_data = scaled_data[-sequence_length_api:].reshape(1, -1, 1)

        # Make predictions using the loaded model
        predictions = model.predict(reshaped_data)

        # Invert the scaling to get the original scale
        inverted_predictions = scaler.inverse_transform(predictions)

        # Return the predictions
        result = {'input_data': input_data,
                  'predictions': inverted_predictions.flatten().tolist()}
        return jsonify(result)

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': str(e)})


@app.route('/predict_v2', methods=['POST'])
def predict_next_30_days():
    try:
        # Get input data from the request
        input_data = request.json.get('data')
        if input_data is None:
            return jsonify({'error': 'Missing "data" key in the request payload'})

        # Preprocess the input data
        preprocessed_data = np.array(input_data).reshape(-1, 1)
        scaled_data = scaler.transform(preprocessed_data)

        # Initialize a list to store predictions
        predicted_values = []

        # Predict 30 days into the future
        for _ in range(30):
            # Adjust the sequence length
            reshaped_data = scaled_data[-sequence_length_api:].reshape(
                1, -1, 1)

            # Make predictions using the loaded model
            predictions = model.predict(reshaped_data)

            # Append the predicted value to the list
            predicted_values.append(predictions[0, 0])

            # Update the input data for the next prediction
            scaled_data = np.append(
                scaled_data, predictions[0, 0].reshape(-1, 1), axis=0)

        # Invert the scaling to get the original scale for the predicted values
        inverted_predictions = scaler.inverse_transform(
            np.array(predicted_values).reshape(-1, 1))

        # Return the predictions for the next 30 days
        result = {'input_data': input_data,
                  'predictions': inverted_predictions.flatten().tolist()}
        return jsonify(result)

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)

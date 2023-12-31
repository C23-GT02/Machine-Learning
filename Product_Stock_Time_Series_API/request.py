import requests
import json

# URL of the Flask API
# Replace with the actual URL if deployed elsewhere
# api_url = "http://127.0.0.1:5000/predict"
api_url = "http://127.0.0.1:5000/predict_v2"

# Input data for predictions
input_data = {
    'data': [22.0, 20.0, 22.0, 21.0, 23.0, 23.0, 21.0, 22.0, 23.0, 24.0, 25.0, 25.0, 26.0, 26.0, 28.0, 28.0, 27.0, 27.0, 29.0, 25.0, 26.0, 29.0, 29.0, 32.0, 28.0, 28.0, 27.0, 29.0, 27.0, 30.0, 32.0, 32.0, 29.0, 30.0, 31.0, 31.0, 30.0, 32.0, 30.0, 32.0, 30.0, 31.0, 32.0, 30.0, 31.0, 31.0, 32.0, 32.0, 34.0, 34.0, 35.0, 33.0, 33.0, 34.0, 35.0, 35.0, 37.0, 39.0, 38.0, 42.0, 40.0, 41.0, 43.0, 41.0, 43.0, 44.0, 41.0, 40.0, 39.0, 41.0, 42.0, 42.0, 43.0, 44.0, 41.0, 41.0, 44.0, 42.0, 42.0, 40.0, 40.0, 40.0, 41.0, 40.0, 43.0, 39.0, 40.0, 42.0, 40.0, 44.0, 40.0, 43.0, 40.0, 40.0, 40.0, 38.0, 42.0, 40.0, 41.0, 41.0, 40.0, 41.0, 41.0, 42.0, 46.0, 43.0, 47.0, 40.0, 42.0, 42.0, 42.0, 43.0, 42.0, 44.0, 45.0, 47.0, 47.0, 48.0, 45.0, 45.0, 45.0, 44.0, 44.0, 43.0, 47.0, 46.0, 49.0, 47.0, 47.0, 47.0, 48.0, 51.0, 48.0, 48.0, 48.0, 47.0, 48.0, 50.0, 53.0, 50.0, 49.0, 50.0, 48.0, 50.0, 49.0, 48.0, 52.0, 48.0, 48.0, 49.0, 49.0, 48.0, 49.0, 48.0, 50.0, 52.0, 50.0, 49.0, 49.0, 49.0, 49.0, 48.0, 48.0, 47.0, 47.0, 48.0, 47.0, 46.0, 47.0, 46.0, 45.0, 45.0, 45.0, 47.0, 47.0, 46.0, 49.0, 47.0, 49.0, 48.0, 46.0, 50.0, 46.0, 46.0, 47.0, 48.0, 47.0, 47.0, 51.0, 48.0, 49.0, 50.0, 49.0, 48.0, 50.0, 49.0, 50.0, 51.0, 52.0, 52.0, 53.0, 54.0, 53.0, 51.0, 49.0, 54.0, 53.0, 52.0, 52.0, 52.0, 53.0, 51.0, 52.0, 52.0, 51.0, 52.0, 53.0, 53.0, 53.0, 57.0, 56.0, 56.0, 56.0, 55.0, 58.0, 56.0, 56.0, 59.0, 56.0, 58.0, 59.0, 58.0, 59.0, 57.0, 60.0, 60.0, 58.0, 61.0, 59.0, 60.0, 60.0, 62.0, 62.0, 61.0, 62.0, 61.0, 62.0, 62.0, 66.0, 62.0, 64.0, 65.0, 67.0, 65.0, 66.0, 68.0, 67.0, 69.0, 71.0, 72.0, 72.0, 71.0, 70.0, 70.0, 71.0, 71.0, 70.0, 72.0, 72.0, 73.0, 73.0, 70.0, 71.0, 73.0, 70.0, 69.0, 70.0, 72.0, 72.0, 70.0, 76.0, 70.0, 70.0, 68.0, 72.0, 69.0, 70.0, 74.0, 72.0, 71.0, 73.0, 73.0, 76.0, 76.0, 74.0, 74.0, 74.0, 75.0, 75.0, 74.0, 74.0, 74.0, 74.0, 75.0, 73.0, 77.0, 75.0, 74.0, 74.0, 74.0, 75.0, 72.0, 72.0, 73.0, 74.0, 76.0, 76.0, 79.0, 76.0, 76.0, 78.0, 78.0, 77.0, 76.0, 77.0, 77.0, 77.0, 79.0, 82.0, 79.0, 80.0, 81.0, 79.0, 79.0, 80.0, 79.0, 80.0, 80.0, 80.0, 79.0, 78.0, 79.0, 78.0, 79.0, 78.0, 81.0, 80.0, 80.0, 81.0, 80.0, 81.0, 82.0, 86.0, 82.0, 84.0, 82.0, 83.0, 82.0, 81.0, 81.0, 84.0, 88.0, 82.0, 83.0, 87.0]
}

# Convert the input_data dictionary to a JSON string
input_data_json = json.dumps({'data': input_data['data']})

# Make a POST request to the /predict endpoint with the Content-Type header
headers = {'Content-Type': 'application/json'}
response = requests.post(api_url, data=input_data_json, headers=headers)

# Save the response to a JSON file
output_filename = 'predictions_response.json'
with open(output_filename, 'w') as json_file:
    json.dump(response.json(), json_file, indent=4)

# Print the response
if response.status_code == 200:
    predictions = response.json().get('predictions')
    print(f'Model Predictions for the Next 30 Days: {predictions}')
    print(f'Response saved to: {output_filename}')
else:
    print(
        f'Request failed with status code: {response.status_code}, response: {response.text}')

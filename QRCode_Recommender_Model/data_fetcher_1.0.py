import requests
import json
import pandas as pd

def fetch_api_data():
    api_url = 'http://127.0.0.1:5000/api/products'  # Change the URL accordingly
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"Failed to fetch data from API. Status Code: {response.status_code}")

def save_to_json(api_data, filename='api_data.json'):
    with open(filename, 'w') as json_file:
        json.dump(api_data, json_file, indent=4)

def create_dataframe(api_data):
    columns = [
        'id_user',
        'id_produk',
        'Nama_Produk',
        'Harga',
        'Bahan baku',
        'Kategori',
        'Nama_umkm'
        # Add more columns if needed
    ]

    data = []
    for item in api_data:
        row = [item.get(column) for column in columns]
        data.append(row)

    df = pd.DataFrame(data, columns=columns)
    return df

def main():
    try:
        api_data = fetch_api_data()
        save_to_json(api_data)  # Save data to JSON file

        dataframe = create_dataframe(api_data)
        print(dataframe)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

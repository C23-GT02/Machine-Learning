import requests
import pandas as pd
import json

def fetch_api_data():
    api_url = 'https://tracker-64690.et.r.appspot.com/api/products'  # Change the URL accordingly
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"Failed to fetch data from API. Status Code: {response.status_code}")

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

        # Uncomment the line below to print the JSON data
        # print(json.dumps(api_data, indent=4))

        dataframe = create_dataframe(api_data)
        print(dataframe)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

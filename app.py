from flask import Flask, jsonify
from google.cloud import firestore

app = Flask(__name__)
app.json.sort_keys = False
db = firestore.Client.from_service_account_json('connection-firebase.json')

@app.route('/api/products', methods=['GET'])
def get_product():
    try:
        product_ref = db.collection('scannedProducts').get()

        if len(product_ref) == 0:
            return jsonify({'status': 'failed', 'message': 'products not found', 'data': None}), 404

        products = []
        for product in product_ref:
            data = product.to_dict()
            user_ref = data.get('userRef')
            user_doc = user_ref.get().to_dict()
            user_data = {'id_user': user_doc.get('uuid')}
            product_ref = data.get('productRef')
            product_data = {}

            if product_ref:
                product_doc = product_ref.get().to_dict()

                if product_doc:
                    partner_ref_path = product_doc.get('partnerRef')
                    partner_ref = db.document(partner_ref_path).get().to_dict()
                    product_ref_path = product_doc.get('productRef')
                    product_ref = db.document(product_ref_path).get().to_dict()
                    product_data = {
                        'id_produk': product_doc.get('id'),
                        'Nama_Produk': product_doc.get('name'),
                        'Harga' : product_ref.get('harga'),
                        'Bahan baku' : product_ref.get('material'),
                        'Kategori': product_ref.get('kategori') if 'kategori' in product_ref else None
                    }

                    # Include partner data in the response
                    partner_data = {
                        'Nama_umkm': partner_ref.get('businessName'),  # Adjust this based on your actual partner document structure
                    }

                    product_data.update(partner_data)

            else:
                print(f"Product Document Reference is None")

            combined_data = {
                **product_data,
                **user_data
            }
            products.append(combined_data)

        return jsonify({'status': 'success', 'message': 'products retrieved successfully', 'data': products}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None}), 500
        
if __name__ == '__main__':
    app.run(debug=True)
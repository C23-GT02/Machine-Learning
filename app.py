from flask import Flask, jsonify
from google.cloud import firestore

app = Flask(__name__)
app.json.sort_keys = False
db = firestore.Client.from_service_account_json('connection-firebase.json')

@app.route('/api/<partner_name>/products', methods=['GET'])
def get_product(partner_name):
    try:
        partner_ref = db.collection('verifiedPartner').document(partner_name)
        partner_snapshot = partner_ref.get()
        if not partner_snapshot.exists:
            return jsonify({'status': 'failed', 'message': 'partner not found', 'data': None}), 404
        products_collection_ref = partner_ref.collection('products')
        products_snapshot = products_collection_ref.get()
        products = []
        for product in products_snapshot:
            data = product.to_dict()
            products.append(data)
        return jsonify({'status': 'success', 'message': 'products retrieved successfully', 'data': products}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None}), 500
        
@app.route('/api/<partner_name>/products/material', methods=['GET'])
def get_material(partner_name):
    try:
        partner_ref = db.collection('verifiedPartner').document(partner_name)
        partner_snapshot = partner_ref.get()
        if not partner_snapshot.exists:
            return jsonify({'status': 'failed', 'message': 'Partner not found', 'data': None}), 404
        products_collection_ref = partner_ref.collection('products')
        products_snapshot = products_collection_ref.get()
        material_data = []
        for doc in products_snapshot:
            doc_data = doc.to_dict()
            material_field = doc_data.get('material')
            product_name = doc_data.get('name')
            if material_field and product_name:
                material_and_name_obj = {'product': product_name, 'material': material_field}
                material_data.append(material_and_name_obj)
        return jsonify({'status': 'success', 'message': 'Material retrieved successfully', 'data': material_data}), 200
    except Exception as e:
        return jsonify({'status': 'failed', 'message': str(e), 'data': None}), 500

@app.route('/api/<partner_name>/products/category', methods=['GET'])
def get_category(partner_name):
    try:
        partner_ref = db.collection('verifiedPartner').document(partner_name)
        partner_snapshot = partner_ref.get()
        if not partner_snapshot.exists:
            return jsonify({'status': 'failed', 'message': 'Partner not found', 'data': None}), 404
        products_collection_ref = partner_ref.collection('products')
        products_snapshot = products_collection_ref.get()
        category_data = []
        for doc in products_snapshot:
            doc_data = doc.to_dict()
            category_field = doc_data.get('kategori')
            product_name = doc_data.get('name')
            if category_field and product_name:
                category_and_name_obj = {'product': product_name, 'Category': category_field}
                category_data.append(category_and_name_obj)
        return jsonify({'status': 'success', 'message': 'Category retrieved successfully', 'data': category_data}), 200
    except Exception as e:
        return jsonify({'status': 'failed', 'message': str(e), 'data': None}), 500


@app.route('/api/partner', methods=['GET'])
def get_partner():
    try:
        partner_ref = db.collection('verifiedPartner')
        partner_snapshot = partner_ref.get()
        if len(partner_snapshot) == 0:
            return jsonify({'status': 404, 'message': 'Partner not found', 'data': partner_snapshot})
        partner_data = []
        for partner in partner_snapshot:
            data = partner.to_dict()
            partner_data.append(data)
        return jsonify({'status': 'success', 'message':'Partner retrieved successfully', 'data': partner_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None}), 500

@app.route('/api/users', methods=['GET'])
def get_user():
    try:
        user_ref = db.collection('users')
        user_snapshot = user_ref.get()
        user_data = []
        for user in user_snapshot:
            data = user.to_dict()
            data['id'] = data.pop('uuid')
            user_data.append(data)
        return jsonify({'status': 'success', 'message':'Users retrieved successfully', 'data': user_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None}), 500

@app.route('/api/users/<user_email>/history', methods=['GET'])
def get_history(user_email):
    try:
        user_ref = db.collection('users').document(user_email)
        user_snapshot = user_ref.get()
        if not user_snapshot.exists:
            return jsonify({'status': 'failed', 'message': 'User not found', 'data': None}), 404
        history_collection_ref = user_ref.collection('history')
        history_snapshot = history_collection_ref.get()
        history_data = []
        for history in history_snapshot:
            data = history.to_dict()
            if 'transactionRef' in data and data['transactionRef']:
                transaction_ref_id = data['transactionRef'].id
                data['transactionRef'] = transaction_ref_id
                transaction_doc_ref = db.document(f'verifiedPartner/uwg/history/{transaction_ref_id}')
                transaction_data = transaction_doc_ref.get().to_dict()
                if transaction_data:
                    data['transactionData'] = transaction_data
                    if 'productRef' in transaction_data and transaction_data['productRef']:
                        product_ref = transaction_data['productRef']
                        product_doc_ref = db.document(product_ref)
                        product_data = product_doc_ref.get().to_dict()
                        data['transactionData']['productData'] = product_data
                        del data['transactionData']['productRef']
                else:
                    data['transactionData'] = None
            history_data.append(data)
        return jsonify({'status': 'success', 'message':' History Users retrieved successfully', 'data': history_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None}), 500

if __name__ == '__main__':
    app.run(debug=True)
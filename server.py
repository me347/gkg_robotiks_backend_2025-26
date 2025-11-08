from flask import Flask, request, jsonify

app = Flask(__name__)

# in-memory store
data_store = {}

@app.route('/data', methods=['POST'])
def post_data():
    payload = request.get_json()
    data_store['value'] = payload.get('value')
    return jsonify({'status': 'ok'})

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({'value': data_store.get('value', None)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

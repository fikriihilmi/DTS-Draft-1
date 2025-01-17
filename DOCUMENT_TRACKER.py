import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('records.db')  # Ensure the database file is named correctly
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/documents', methods=['POST'])
def add_document():
    data = request.get_json()
    name = data['name']
    location = data.get('location', '')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO records (name, location) VALUES (?, ?)', (name, location))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Document added successfully!'}), 201

@app.route('/documents', methods=['GET'])
def get_documents():
    conn = get_db_connection()
    documents = conn.execute('SELECT * FROM records').fetchall()
    conn.close()
    
    return jsonify([dict(doc) for doc in documents]), 200

@app.route('/documents/<int:id>', methods=['GET'])
def get_document(id):
    conn = get_db_connection()
    document = conn.execute('SELECT * FROM records WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if document is None:
        return jsonify({'error': 'Document not found!'}), 404
    
    return jsonify(dict(document)), 200

@app.route('/documents/<int:id>', methods=['PUT'])
def update_document(id):
    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    
    conn = get_db_connection()
    conn.execute('UPDATE records SET name = ?, location = ? WHERE id = ?', (name, location, id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Document updated successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)

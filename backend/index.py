from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app, app_check, auth
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
import flask
from uuid import uuid4

load_dotenv()
app = Flask(__name__)
CORS(app)

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

##Schemas
todo_ref = db.collection('todos')

## helpers
def geterate_unique_id():
    return uuid4().hex

@app.before_request
def verify_app_check() -> None:
    print(request.headers)
    app_check_token = request.headers.get("Authorization")
    print(app_check_token)
    try:
        # app_check_claims = app_check.verify_token(app_check_token)
        app_check_claims = auth.verify_id_token(app_check_token)
        # If verify_token() succeeds, okay to continue to route handler.
    except Exception as e:
        print(str(e), '--')
        flask.abort(401)

## Routes
@app.route('/',methods=['GET'])
def home():
    return {"res": "working"}, 200

@app.route('/add', methods=['POST'])
def create():
    try:
        data = {
            'id': geterate_unique_id(),
            'title': request.json['title'],
            'content': request.json['content']
        }
        todo = todo_ref.add(data)
        todo = todo[1].get().to_dict()
        print(todo)
        return {"res": "success", "record": todo}, 200
    except Exception as e:
        return f"An Error Occured: {e}", 500


@app.route('/get', methods=['GET'])
def read():
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')    
        if todo_id:
            todo = todo_ref.where('id', '==', todo_id).get()
            if todo: 
                return jsonify(todo[0].to_dict()), 200
            else:
                return {'res': 'not found'}, 200
    except Exception as e:
        return f"An Error Occured: {e}", 500

@app.route('/getall', methods=['GET'])
def readall():
    try:
        # Check if ID was passed to URL query 
        all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}", 500


@app.route('/update', methods=['POST', 'PUT'])
def update():
    try:
        todo_id = request.json['id']
        for doc in todo_ref.where('id', '==', todo_id).stream() :
            unique_id = doc.id
            break
        todo_ref.document(unique_id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        for doc in todo_ref.where('id', '==', todo_id).stream() :
            unique_id = doc.id
            break        
        todo_ref.document(unique_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

if __name__ == '__main__':
    app.run(debug=True)
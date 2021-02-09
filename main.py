from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

documents = dict()

class uploadCollection(Resource):
    def put(self, collection_id):
        txt = request.form['txt']
        documents[collection_id] = txt
        return {
            collection_id: txt
        }
api.add_resource(uploadCollection, '/upload/<string:collection_id>')

class listCollections(Resource):
    def get(self):
        return {
            'documents': documents
        }
api.add_resource(listCollections, '/list')

# Add Resources to app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


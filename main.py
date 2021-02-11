from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pathlib import Path
from os import environ

app = Flask(__name__)
CORS(app)
api = Api(app)

class uploadCollection(Resource):
    def post(self):

        collections_dir = environ.get('COLLECTIONS_DIR')

        # Get collection name
        collection_name = request.form['collectionName']
        collection_dir = os.path.join(collections_dir, collection_name)

        # Save new files in collection
        os.makedirs(collection_dir, exist_ok=True)
        for e in request.files:
            f = request.files[e]

            file_path = os.path.join(collection_dir, f.filename)
            f.save(file_path)

        return {
            'Collection Files': [f.filename for f in request.files.values()]
        }

api.add_resource(uploadCollection, '/upload')

class listCollections(Resource):
    def get(self):

        collections_dir = environ.get('COLLECTIONS_DIR')
        collections = os.listdir(collections_dir)

        collections_data = {
            'collection_count': len(collections),
            'collections': []
        }

        for cn in collections:
            cpath = os.path.join(collections_dir, cn)
            doclist = os.listdir(cpath)
            collections_data['collections'].append({
                'collection_name': cn,
                'collection_size': len(doclist),
            })

        return collections_data

api.add_resource(listCollections, '/list')

# Add Resources to app
if __name__ == '__main__':

    # Load configuration file

    # Assume in same directory for now
    config_path = Path('.') / '/.env'
    load_dotenv(dotenv_path=config_path)

    app.run(debug=True, host='0.0.0.0')


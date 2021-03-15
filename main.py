from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv
from threading import Thread
import requests
import utils
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
        pdfs_dir = os.path.join(collection_dir, 'pdfs')
        xmls_dir = os.path.join(collection_dir, 'xmls')
        structs_dir = os.path.join(collection_dir, 'structs')

        # Save new files in collection
        os.makedirs(pdfs_dir, exist_ok=True)
        os.makedirs(xmls_dir, exist_ok=True)

        loaded_pdfs = []
        for e in request.files:
            f = request.files[e]
            file_path = os.path.join(pdfs_dir, f.filename)
            xml_path = os.path.join(xmls_dir, f.filename[:-4] + '.xml')

            if f.filename.lower().endswith('.pdf'):
                loaded_pdfs.append(f.filename)
                f.save(file_path)
        
        endpoint = environ.get('GROBID_URL')
        utils.process_uploaded_pdfs(pdfs_dir, xmls_dir, structs_dir, grobid_url=endpoint)

        return {
            'Collection Files': loaded_pdfs
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
            cpath = os.path.join(collections_dir, cn, 'pdfs')
            doclist = os.listdir(cpath)
            collections_data['collections'].append({
                'collection_name': cn,
                'document_names': list(doclist),
                'collection_size': len(doclist),
            })

        return collections_data


api.add_resource(listCollections, '/list')

class listModels(Resource):
    def get(self):

        models_dir = environ.get('MODELS_DIR')
        models = os.listdir(models_dir)

        return {
            'models': list(models)
        }

api.add_resource(listModels, '/listModels')

# Add Resources to app
if __name__ == '__main__':

    # Load configuration file

    # Assume in same directory for now
    config_path = Path('.') / '/.env'
    load_dotenv(dotenv_path=config_path)

    app.run(debug=True, host='0.0.0.0')

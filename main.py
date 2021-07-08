from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv
from threading import Thread
import requests
import utils
import os
from pathlib import Path
from os import environ
from extract import create_extraction
from datetime import datetime

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

class createExtraction(Resource):
    def post(self):

        # Create extraction
        model_name = request.form['modelName']
        collection_name = request.form['collectionName']

        collections_dir = environ.get('COLLECTIONS_DIR')
        models_dir = environ.get('MODELS_DIR')
        extractions_dir = environ.get('EXTRACTIONS_DIR')

        model_path = os.path.join(models_dir, model_name)
        model_exists = os.path.exists(model_path)
        print(f'Model Path: {model_path}, exists: {model_exists}')


        collection_path = os.path.join(collections_dir, collection_name)
        collection_exists = os.path.exists(collection_path)
        print(f'Collection Path: {collection_path}; collection exists: {collection_exists}')

        extraction_dir_path = os.path.join(extractions_dir, collection_name + '__' + model_name)
        os.makedirs(extraction_dir_path, exist_ok=True)


        input_struct_path = os.path.join(collection_path, 'structs', 'struct_base.json')
        extraction_args = (input_struct_path, model_path, extraction_dir_path, True)
        thread = Thread(target=create_extraction, args=extraction_args)
        thread.start()

api.add_resource(createExtraction, '/createExtraction')

class listExtractions(Resource):
    def get(self):

        # List all available extractions
        extractions_dir = environ.get('EXTRACTIONS_DIR')
        extraction_list = os.listdir(extractions_dir)

        extractions = []
        for eid in extraction_list:
            collection_name, model_name = eid.split('__')
            extraction_dir = os.path.join(extractions_dir, eid)
            mtime = os.path.getmtime(extraction_dir)
            print(f'Modified time: {mtime}')

            extractions.append({
                'collection': collection_name,
                'model': model_name,
                'modtime': str(datetime.fromtimestamp(mtime))
            })

        return { 'extractions': extractions }

api.add_resource(listExtractions, '/listExtractions')

class serveExtraction(Resource):
    def get(self):

        # Download queried extraction
        args = request.args

        model = args.get('model', None)
        collection = args.get('collection', None)

        if (not model) or (not collection):
            return {
                'error': 'No collection or model was found.'
            }

        extractions_dir = environ.get('EXTRACTIONS_DIR')
        extraction_dir_path = os.path.join(extractions_dir, f'{collection}__{model}')
        output_path = os.path.join(extraction_dir_path, 'output_table.xlsx')

        print('Extraction Dir:')
        print(extraction_dir_path)
        print(os.path.exists(extraction_dir_path))
        print(os.path.exists(output_path))

        return send_from_directory(extraction_dir_path, 'output_table.xlsx')

api.add_resource(serveExtraction, '/getExtraction')


# Add Resources to app
if __name__ == '__main__':

    # Load configuration file

    print('Starting up server ... \n')

    # Assume in same directory for now
    config_path = Path('.') / '/.env'
    load_dotenv(dotenv_path=config_path)

    app.run(debug=True, host='0.0.0.0')

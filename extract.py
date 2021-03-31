import os
from ya.dotdict import DotDict
from tempfile import TemporaryDirectory
from medtrialextractor import formatting
from medtrialextractor.train import prod_predict

def create_extraction(input_struct_path, model_dir, debug=False):

    if debug:
        temp_dir = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/tempdir'
        root_dir = os.path.join(temp_dir, 'root')

    else:
        temp_dir = TemporaryDirectory()
        root_dir = os.path.join(temp_dir.name, 'root')

    # Step 1: Create empty NER input
    ner_input_file_path = os.path.join(root_dir, 'ner_input.txt')
    formatting.make_empty_ner_bio(input_struct_path, ner_input_file_path)

    # Step 2: Make NER predictions
    cache_dir = os.path.join(root_dir, 'cache_dir')
    ner_labels_path = os.path.join(model_dir, 'ner_labels.txt')
    ner_model_path = os.path.join(model_dir, 'ner')
    ner_output_file_path = os.path.join(root_dir, 'ner_output.txt')

    model_args = DotDict()
    model_args['model_name_or_path'] = ner_model_path
    model_args['cache_dir'] = cache_dir
    model_args['use_fast'] = True
    model_args['use_cls'] = False
    model_args['use_crf'] = True

    predict_args = DotDict()
    predict_args['labels'] = ner_labels_path
    predict_args['no_cuda'] = False
    predict_args['input_file'] = ner_input_file_path
    predict_args['max_seq_length'] = 512
    predict_args['overwrite_cache'] = True
    predict_args['batch_size'] = 256
    predict_args['output_file'] = ner_output_file_path

    prod_predict(model_args, predict_args)

    # Step 3: Load NER predictions into struct

    # Step 4: Create empty RD output

    # Step 5: Make RD predictions

    # Step 6: Load RD predictions

    # Step 7: Creat tabular summary output


if __name__ == '__main__':

    input_struct_path = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/collections_dir/Hello/structs/struct_base.json'
    model_dir = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/models/8020/'

    create_extraction(input_struct_path, model_dir, debug=True)
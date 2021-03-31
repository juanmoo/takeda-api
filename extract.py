import utils
import os
from ya.dotdict import DotDict
from tempfile import TemporaryDirectory
from medtrialextractor import formatting

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

    # Step 3: Load NER predictions into struct

    # Step 4: Create empty RD output

    # Step 5: Make RD predictions

    # Step 6: Load RD predictions

    # Step 7: Creat tabular summary output


if __name__ == '__main__':

    input_struct_path = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/collections_dir/Hello/structs/struct_base.json'
    model_dir = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/models/8020/'

    create_extraction(input_struct_path, model_dir, debug=True)
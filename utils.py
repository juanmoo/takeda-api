from medtrialextractor import formatting
from multiprocessing import Process
import requests
import os

# Process Uploaded PDFs

def process_uploaded_pdfs(pdfs_dir, xmls_dir, structs_dir, grobid_url=''):

    if not grobid_url:
        return None

    pdf_paths = [e for e in os.listdir(pdfs_dir) if e.lower().endswith('.pdf')]

    print('PDFs')
    plist = []

    for pdf_name in pdf_paths:
        name = pdf_name[:-4]
        pdf_path = os.path.join(pdfs_dir, pdf_name)
        xml_path = os.path.join(xmls_dir, name + '.xml')
        p = Process(target=process_pdf_file, args=(
            pdf_path, xml_path, grobid_url))
        plist.append(p)

    # Ensure Folders Exist
    os.makedirs(pdfs_dir, exist_ok=True)
    os.makedirs(xmls_dir, exist_ok=True)
    os.makedirs(structs_dir, exist_ok=True)

    # User GROBID service to parse PDFs
    for p in plist:
        p.start()
    for p in plist:
        p.join()

    # Create Struct
    struct_path = os.path.join(structs_dir, 'struct_base.json')
    formatting.batch_process(xmls_dir, struct_path)


def process_pdf_file(input_path, output_path, grobid_url):
    with open(input_path, 'rb') as pdf_file:
        r = requests.post(grobid_url, files={'input': pdf_file})
        with open(output_path, 'w') as xml_file:
            xml_file.write(r.text)


if __name__ == '__main__':

    # pdfs_dir = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/collections_dir/pilot/pdfs'
    # xmls_dir = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/collections_dir/pilot/xmls'
    structs_dir = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/collections_dir/pilot/structs'
    # grobid_url = 'http://localhost:8070/api/processFulltextDocument'

    # process_uploaded_pdfs(pdfs_dir, xmls_dir, structs_dir, grobid_url)
    struct_path = os.path.join(structs_dir, 'struct_base.json')
    dummy = '/data/rsg/nlp/juanmoo1/projects/05_dev/workdir/collections_dir/pilot/bio/ner_input.txt'


    # make_empty_ner_bio(struct_path, dummy)

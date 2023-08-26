import box
import timeit
import yaml
import argparse
from dotenv import find_dotenv, load_dotenv
from src.utils import setup_dbqa

import gradio as gr

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

def query(input):
    # Setup DBQA
    start = timeit.default_timer()
    dbqa = setup_dbqa()
    response = dbqa({'query': input})
    end = timeit.default_timer()

    answer = response["result"]

    # Process source documents
    source_docs = response['source_documents']
    for i, doc in enumerate(source_docs):
        print(f'\nSource Document {i+1}\n')
        print(f'Source Text: {doc.page_content}')
        print(f'Document Name: {doc.metadata["source"]}')
        print(f'Page Number: {doc.metadata["page"]}\n')
        print('='* 60)

    responsetime = f"Time to retrieve response: {end - start}"

    answer = answer + " " + source_docs + " " + responsetime
    return answer

demo = gr.Interface(fn=query,
                    inputs=gr.inputs.Textbox(lines=5, label="Input Text"),
                    outputs=gr.outputs.Textbox(label="Generated Text"))
    
if __name__ == "__main__":
    demo.launch() 
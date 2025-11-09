from flask import Flask, jsonify, request
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import uuid
import os
import shutil
from glob import glob

from schemas.SerializedDoc import SerializedDoc
from schemas.Description import Description

# Nuke on start up
# for file in glob("tmp/*"):
#     if os.path.isdir(file):
#         shutil.rmtree(file)

if not os.path.isdir('tmp'):
    os.mkdir('tmp/')

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({ 'msg': 'Hello World' })

@app.route('/ingest')
def ingest():
    llm = ChatOpenAI(
        # model='nemotron:70b',
        model='nemo',
        base_url="http://204.52.27.251:11434/v1",
        api_key='HACKATHON SAVE OUR SOULS',
        temperature=0
    )
    structured_llm = llm.with_structured_output(SerializedDoc)

    repo_url = request.args.get('repo_url') # NOTE: expected to come without https://
    if not repo_url:
        return jsonify({ 'error': 'repo_url parameter is required' }), 400

    folder_name = uuid.uuid4()
    clone_dir = f'tmp/{folder_name}'
    
    os.system(f'git clone --depth 1 https://{repo_url} {clone_dir}')

    if not os.path.isdir(clone_dir):
        return jsonify({ 'error': 'Failed to clone repository.' }), 500

    try:
        # Scan *.md files recursively
        md_content = ''
        for file_path in glob(f'{clone_dir}/**/*.md', recursive=True):
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        md_content += f'####{file_path}\n'
                        md_content += f.read() + "\n"
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")

        description = get_description(content=md_content, llm=llm)

        # Code analysis
        documents = []
        for file_path in glob(f'{clone_dir}/**', recursive=True):
            if '.git/' in file_path or '__pycache__' in file_path or 'node_modules/' in file_path:
                continue
            
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        f.read(1024)
                        f.seek(0)
                        documents.append(f.read())
                except (UnicodeDecodeError, IOError):
                    print(f"Skipping non-text or unreadable file: {file_path}")
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.create_documents(documents)
        
        embedding_function = OllamaEmbeddings(model="nomic-embed-text", base_url="http://204.52.27.251:11434")
        chroma_client = chromadb.HttpClient(host='204.52.27.251', port=8000)
        vectorstore = Chroma.from_documents(texts, embedding_function, client=chroma_client)
        retriever = vectorstore.as_retriever()

        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        msgs = [
            ('system', 'You are a senior software engineer. Analyze the following code and provide a structured analysis. The pages directive should be the names of the pages needed to explain the project in its detail. The description is what the code does in a short descriptive sentence. Context: {context}'),
            ('human', 'Question: {question}')
        ]

        # Check for deps
        dep_content = ''
        req_path = f'{clone_dir}/requirements.txt'
        if os.path.isfile(req_path): # Python
            with open(req_path, 'r', encoding='utf-8') as f:
                dep_content += f'####{req_path}\n'
                dep_content += f.read() + "\n" 
                msgs.append(('human', f'dependencies file: {dep_content}'))

        pkg_path = f'{clone_dir}/package.json'
        if os.path.isfile(pkg_path): # TypeScript / JavaScript
            with open(pkg_path, 'r', encoding='utf-8') as f:
                dep_content += f'####{pkg_path}\n'
                dep_content += f.read() + "\n" 
                msgs.append(('human', f'dependencies file: {dep_content}'))

        prompt = ChatPromptTemplate.from_messages(msgs)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | structured_llm
        )

        response = chain.invoke("Analyze the provided code and generate a structured analysis.")

        print("--- Successfully Received Pydantic Object ---")
        print(f"Type of response: {type(response)}")
        print("\n")
        print(response.model_dump_json(indent=2))
        print(f"Libraries: {response.dependencies}")

        return jsonify(response.model_dump_json())

    except Exception as e:
        print(f"--- Error ---")
        print(f"An error occurred: {e}")
        print("This often happens if your model or API endpoint doesn't support tool-calling.")
        return jsonify({ "msg": "An error occurred during processing."})
    finally:
        if os.path.isdir(clone_dir):
            shutil.rmtree(clone_dir)

def get_description(content: str, llm):
    structured_llm = llm.with_structured_output(Description)
    prompt = ChatPromptTemplate.from_messages([
     ('system', 'You are a senior software engineer. Your job is to summarize what this GitHub project is about based on its README.md'),
     ('human', '{content}'),
    ])
    chain = prompt | structured_llm
    response = chain.invoke({ 'content': content})

    return response.description

app.run(debug=True, host='0.0.0.0', port=3333)


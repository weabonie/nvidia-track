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
import git
import json

from schemas.SerializedDoc import SerializedDoc
from schemas.Description import Description
from schemas.Dependencies import Dependencies
from schemas.InstallProcess import InstallProcess

import analysis

# Nuke on start up
# for file in glob("tmp/*"):
#     if os.path.isdir(file):
#         shutil.rmtree(file)

if not os.path.isdir('tmp'):
    os.mkdir('tmp/')

app = Flask(__name__)

LANGUAGE_CONFIG = {
    'Python': {'extensions': ['py']},
    'JavaScript': {'extensions': ['js', 'jsx']},
    'TypeScript': {'extensions': ['ts', 'tsx']},
    'Java': {'extensions': ['java']},
    'HTML': {'extensions': ['html']},
    'CSS': {'extensions': ['css', 'scss', 'sass']},
    'Shell': {'extensions': ['sh']},
    'Ruby': {'extensions': ['rb']},
    'Go': {'extensions': ['go']},
    'Rust': {'extensions': ['rs']},
    'PHP': {'extensions': ['php']},
}

def detect_dependencies(clone_dir):
    detected_langs = set()
    ext_to_lang = {f".{ext}": lang for lang, data in LANGUAGE_CONFIG.items() for ext in data['extensions']}

    for root, dirs, files in os.walk(clone_dir):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'vendor']]
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in ext_to_lang:
                detected_langs.add(ext_to_lang[ext])

    # Check for framework/dependency files
    if os.path.exists(os.path.join(clone_dir, 'package.json')):
        detected_langs.add('Node.js')
        try:
            with open(os.path.join(clone_dir, 'package.json'), 'r') as f:
                package_json = json.load(f)
                all_deps = {**package_json.get('dependencies', {}), **package_json.get('devDependencies', {})}
                if 'react' in all_deps:
                    detected_langs.add('React')
                if 'vue' in all_deps:
                    detected_langs.add('Vue.js')
                if '@angular/core' in all_deps:
                    detected_langs.add('Angular')
                if 'next' in all_deps:
                    detected_langs.add('Next.js')
                if 'svelte' in all_deps:
                    detected_langs.add('Svelte')
        except json.JSONDecodeError:
            print(f"Warning: Could not parse package.json in {clone_dir}")


    if os.path.exists(os.path.join(clone_dir, 'requirements.txt')):
        detected_langs.add('Python')
    if os.path.exists(os.path.join(clone_dir, 'pom.xml')) or os.path.exists(os.path.join(clone_dir, 'build.gradle')):
        detected_langs.add('Java') # Could be Maven or Gradle
    if os.path.exists(os.path.join(clone_dir, 'Gemfile')):
        detected_langs.add('Ruby')
    if os.path.exists(os.path.join(clone_dir, 'go.mod')):
        detected_langs.add('Go')
    if os.path.exists(os.path.join(clone_dir, 'Cargo.toml')):
        detected_langs.add('Rust')
    if os.path.exists(os.path.join(clone_dir, 'composer.json')):
        detected_langs.add('PHP')

    return sorted(list(detected_langs))

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

    repo_url = request.args.get('repo_url') # NOTE: expected to come without https://
    if not repo_url:
        return jsonify({ 'error': 'repo_url parameter is required' }), 400

    folder_name = uuid.uuid4()
    clone_dir = f'tmp/{folder_name}'
    
    try:
        git.Repo.clone_from(f'https://{repo_url}', clone_dir, depth=1)
    except Exception as e:
        print(f"Failed to clone repo: {e}")
        return jsonify({ 'error': 'Failed to clone repository.' }), 500

    try:
        # 1. Detect dependencies
        dependencies = detect_dependencies(clone_dir)

        # 2. Get description from READMEs
        md_content = ''
        for file_path in glob(f'{clone_dir}/**/*.md', recursive=True):
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        md_content += f'####{file_path}\n'
                        md_content += f.read() + "\n"
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
        
        description_obj = get_description(content=md_content, llm=llm)
        goal = description_obj.description if description_obj else "Could not determine project goal."

        # 3. Get repo name
        repo_name = repo_url.split('/')[-1]

        # 4. Generate comprehensive pages from graph analysis
        # This performs deep code analysis using the integrated 1_build_skeleton and 2_enrich_graph logic
        pages = {"summary": "This is an auto-generated summary."}  # Default fallback
        try:
            full_repo_url = f"https://{repo_url}"
            print("\n=== Starting deep code analysis ===")
            analysis_result = analysis.analyze_repo(full_repo_url, llm)
            
            # Extract pages from analysis result
            if analysis_result and 'pages' in analysis_result:
                pages = analysis_result['pages']
                print(f"✓ Successfully generated {len(pages)} pages from code analysis")
            else:
                print("⚠ Analysis returned but no pages found, using default")
        except Exception as e:
            print(f"⚠ Graph analysis failed: {e}")
            print("  Continuing with basic analysis only...")

        # 5. Generate installation process
        install_process = get_install_process(str(dependencies), llm)

        # 6. Construct the result
        result = SerializedDoc(
            dependencies=dependencies,
            goal=goal,
            pages=pages,
            repo_name=repo_name,
            install_process=install_process
        )

        return jsonify(result.dict())

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

    return response

def get_deps(content: str, llm) -> list:
    structured_llm = llm.with_structured_output(Dependencies)
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'You are a senior software engineer. Your job is to compile all dependencies needed from the overview of the projects functions given'),
        ('human', 'Overview: {overview}')
    ])
    chain = prompt | structured_llm
    response = chain.invoke({ 'overview': content })

    return response

def get_install_process(content: str, llm) -> str:
    if not content or content == '[]':
        return "No specific installation steps identified. Please refer to the project's documentation."
    
    try:
        structured_llm = llm.with_structured_output(InstallProcess)
        prompt = ChatPromptTemplate.from_messages([
            ('system', 'You are a senior software engineer who loves writing. Your job is to write an install process for the given dependencies. You do not need to mention installing standard libraries. But you must require mentioning installing the toolchain for the languages it uses. For instance, if the project uses JavaScript it may need NPM.'),
            ('human', 'Dependencies: {content}')
        ])
        chain = prompt | structured_llm
        response = chain.invoke({ 'content': content })
        return response.install_process
    except Exception as e:
        print(f"Could not generate install process via LLM: {e}")
        return "Could not automatically generate installation steps. Please refer to the project's documentation."

app.run(debug=True, host='0.0.0.0', port=3333)

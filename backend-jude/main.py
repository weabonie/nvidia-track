from flask import Flask, jsonify, request
from flask_cors import CORS
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
import requests
import logging
from datetime import datetime

from schemas.SerializedDoc import SerializedDoc
from schemas.Description import Description
from schemas.Dependencies import Dependencies
from schemas.InstallProcess import InstallProcess
from schemas.Pages import Pages
from schemas.ProjectName import ProjectName

import analysis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Nuke on start up
# for file in glob("tmp/*"):
#     if os.path.isdir(file):
#         shutil.rmtree(file)

if not os.path.isdir('tmp'):
    os.mkdir('tmp/')
    logger.info("Created tmp directory")

app = Flask(__name__)

# Configure CORS to allow requests from specific origins
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://nvidia.weabonie.com",
            "http://100.74.32.124",
            "https://100.74.32.124",
            "http://100.81.27.36",
            "https://100.81.27.36"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
logger.info("CORS enabled for: https://nvidia.weabonie.com, 100.74.32.124, 100.81.27.36")

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
    'C#': {'extensions': ['cs']},
    'C++': {'extensions': ['cpp', 'cc', 'cxx', 'hpp', 'h']},
    'C': {'extensions': ['c', 'h']},
}

def detect_dependencies(clone_dir):
    """Detect dependencies with better formatting and version info where possible."""
    logger.info(f"Starting dependency detection for: {clone_dir}")
    detected_deps = []
    ext_to_lang = {f".{ext}": lang for lang, data in LANGUAGE_CONFIG.items() for ext in data['extensions']}
    
    detected_langs = set()
    for root, dirs, files in os.walk(clone_dir):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'vendor']]
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in ext_to_lang:
                detected_langs.add(ext_to_lang[ext])

    logger.info(f"Detected languages from file extensions: {detected_langs}")

    # Check for framework/dependency files with versions
    if os.path.exists(os.path.join(clone_dir, 'package.json')):
        logger.info("Found package.json, parsing for Node.js dependencies...")
        try:
            with open(os.path.join(clone_dir, 'package.json'), 'r') as f:
                package_json = json.load(f)
                all_deps = {**package_json.get('dependencies', {}), **package_json.get('devDependencies', {})}
                
                # Check for major frameworks
                if 'next' in all_deps:
                    version = all_deps['next'].replace('^', '').replace('~', '').split('.')[0]
                    detected_deps.append(f'Next.js {version}' if version.isdigit() else 'Next.js')
                elif 'react' in all_deps:
                    version = all_deps['react'].replace('^', '').replace('~', '').split('.')[0]
                    detected_deps.append(f'React {version}' if version.isdigit() else 'React')
                
                if 'vue' in all_deps:
                    version = all_deps['vue'].replace('^', '').replace('~', '').split('.')[0]
                    detected_deps.append(f'Vue.js {version}' if version.isdigit() else 'Vue.js')
                
                if '@angular/core' in all_deps:
                    detected_deps.append('Angular')
                
                if 'svelte' in all_deps:
                    detected_deps.append('Svelte')
                
                if 'express' in all_deps:
                    detected_deps.append('Express.js')
                
                # Add Node.js if we have package.json
                if all_deps:
                    detected_deps.append('Node.js')
                    
        except json.JSONDecodeError:
            print(f"Warning: Could not parse package.json in {clone_dir}")
            if 'JavaScript' in detected_langs or 'TypeScript' in detected_langs:
                detected_deps.append('Node.js')

    # Python dependencies
    if os.path.exists(os.path.join(clone_dir, 'requirements.txt')):
        try:
            with open(os.path.join(clone_dir, 'requirements.txt'), 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Extract package name and version
                        if '==' in line:
                            pkg, ver = line.split('==')[:2]
                            detected_deps.append(f'{pkg.strip()} {ver.strip()}')
                        elif '>=' in line:
                            pkg = line.split('>=')[0].strip()
                            detected_deps.append(pkg)
                        else:
                            detected_deps.append(line.split('[')[0].strip())
        except Exception as e:
            print(f"Warning: Could not parse requirements.txt: {e}")
    
    # Add Python if .py files exist
    if 'Python' in detected_langs and not any('Python' in dep for dep in detected_deps):
        detected_deps.append('Python')
    
    # Other toolchains
    if os.path.exists(os.path.join(clone_dir, 'pom.xml')) or os.path.exists(os.path.join(clone_dir, 'build.gradle')):
        detected_deps.append('Java')
        if os.path.exists(os.path.join(clone_dir, 'pom.xml')):
            detected_deps.append('Maven')
        if os.path.exists(os.path.join(clone_dir, 'build.gradle')):
            detected_deps.append('Gradle')
    
    if os.path.exists(os.path.join(clone_dir, 'Gemfile')):
        detected_deps.append('Ruby')
    
    if os.path.exists(os.path.join(clone_dir, 'go.mod')):
        detected_deps.append('Go')
    
    if os.path.exists(os.path.join(clone_dir, 'Cargo.toml')):
        detected_deps.append('Rust')
    
    if os.path.exists(os.path.join(clone_dir, 'composer.json')):
        detected_deps.append('PHP')
    
    # Unity/Game Engine detection
    if os.path.exists(os.path.join(clone_dir, 'ProjectSettings')):
        detected_deps.append('Unity')
        # Try to get Unity version
        project_version_file = os.path.join(clone_dir, 'ProjectSettings', 'ProjectVersion.txt')
        if os.path.exists(project_version_file):
            try:
                with open(project_version_file, 'r') as f:
                    for line in f:
                        if 'm_EditorVersion:' in line:
                            version = line.split(':')[1].strip()
                            detected_deps.append(f'Unity {version}')
                            detected_deps.remove('Unity')  # Remove generic Unity
                            logger.info(f"Detected Unity version: {version}")
                            break
            except Exception as e:
                logger.warning(f"Could not parse Unity version: {e}")
    
    # Unreal Engine detection
    try:
        uproject_files = [f for f in os.listdir(clone_dir) if f.endswith('.uproject') and os.path.isfile(os.path.join(clone_dir, f))]
        if uproject_files:
            detected_deps.append('Unreal Engine')
            logger.info(f"Detected Unreal Engine project: {uproject_files[0]}")
    except Exception as e:
        logger.warning(f"Error checking for Unreal Engine: {e}")
    
    # Godot detection
    if os.path.exists(os.path.join(clone_dir, 'project.godot')):
        detected_deps.append('Godot')
        logger.info("Detected Godot project")
    
    # Add C# if detected (common in Unity/game dev)
    if 'C#' in detected_langs and not any('C#' in dep for dep in detected_deps):
        detected_deps.append('C#')
    
    # Database indicators
    if os.path.exists(os.path.join(clone_dir, 'docker-compose.yml')) or os.path.exists(os.path.join(clone_dir, 'docker-compose.yaml')):
        try:
            import yaml
            compose_file = os.path.join(clone_dir, 'docker-compose.yml')
            if not os.path.exists(compose_file):
                compose_file = os.path.join(clone_dir, 'docker-compose.yaml')
            with open(compose_file, 'r') as f:
                compose_data = yaml.safe_load(f)
                if compose_data and 'services' in compose_data:
                    services = compose_data['services']
                    if 'postgres' in services or 'postgresql' in services:
                        detected_deps.append('PostgreSQL')
                    if 'mysql' in services:
                        detected_deps.append('MySQL')
                    if 'mongo' in services or 'mongodb' in services:
                        detected_deps.append('MongoDB')
                    if 'redis' in services:
                        detected_deps.append('Redis')
        except Exception as e:
            print(f"Warning: Could not parse docker-compose: {e}")

    # Remove duplicates while preserving order
    seen = set()
    unique_deps = []
    for dep in detected_deps:
        dep_lower = dep.lower().split()[0]  # Compare base package name
        if dep_lower not in seen:
            seen.add(dep_lower)
            unique_deps.append(dep)
    
    final_deps = unique_deps if unique_deps else sorted(list(detected_langs))
    logger.info(f"Final dependencies detected: {final_deps}")
    return final_deps

def build_project_context(clone_dir):
    """Build comprehensive context about the project by reading actual files.
    
    HOW THE LLM SEES THE REPO:
    1. Reads ALL .md files (README, docs, etc.) - this is the primary source
    2. Scans file structure (up to 2 levels deep) to understand project layout
    3. Identifies entry points (index.html, main.py, etc.)
    4. Reads sample code from main files (first 2000 chars)
    5. Lists config files (package.json, requirements.txt, etc.)
    
    All this context is then passed to the LLM in the prompts!
    """
    logger.info(f"Building comprehensive project context for: {clone_dir}")
    context = {
        'readme': '',
        'file_structure': [],
        'code_samples': {},
        'config_files': [],
        'main_files': []
    }
    
    # 1. Read all markdown files
    logger.info("Reading all markdown files...")
    md_count = 0
    for file_path in glob(f'{clone_dir}/**/*.md', recursive=True):
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    relative_path = os.path.relpath(file_path, clone_dir)
                    content = f.read()
                    context['readme'] += f'## {relative_path}\n{content}\n\n'
                    md_count += 1
                    logger.debug(f"Read markdown file: {relative_path} ({len(content)} chars)")
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
    
    logger.info(f"Read {md_count} markdown files, total {len(context['readme'])} characters")
    
    # 2. Get file structure (top level and important subdirs)
    logger.info("Scanning file structure...")
    for root, dirs, files in os.walk(clone_dir):
        # Skip hidden and build directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'vendor', 'dist', 'build', '.next']]
        
        depth = root[len(clone_dir):].count(os.sep)
        if depth <= 2:  # Only go 2 levels deep
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), clone_dir)
                context['file_structure'].append(rel_path)
    
    logger.info(f"Found {len(context['file_structure'])} files in structure")
    
    # 3. Identify main/entry files
    logger.info("Identifying main entry files...")
    entry_patterns = ['index.html', 'index.js', 'index.ts', 'main.py', 'app.py', 'server.js', 'main.go', 'index.tsx']
    for pattern in entry_patterns:
        for file_path in glob(f'{clone_dir}/**/{pattern}', recursive=True):
            if os.path.isfile(file_path):
                rel_path = os.path.relpath(file_path, clone_dir)
                context['main_files'].append(rel_path)
                logger.info(f"Found entry file: {rel_path}")
    
    # 4. Read sample code from main files (limited)
    logger.info("Reading sample code from main files...")
    for main_file in context['main_files'][:3]:  # Only first 3
        full_path = os.path.join(clone_dir, main_file)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                # Read first 50 lines or 2000 chars
                content = f.read(2000)
                context['code_samples'][main_file] = content
                logger.info(f"Read code sample from {main_file}: {len(content)} chars")
        except Exception as e:
            logger.warning(f"Could not read {main_file}: {e}")
    
    # 5. Identify config files
    logger.info("Identifying configuration files...")
    config_patterns = ['package.json', 'requirements.txt', 'Cargo.toml', 'go.mod', 'pom.xml', 
                      'docker-compose.yml', '.env.example', 'tsconfig.json', 'vite.config.js']
    for pattern in config_patterns:
        file_path = os.path.join(clone_dir, pattern)
        if os.path.exists(file_path):
            context['config_files'].append(pattern)
            logger.info(f"Found config file: {pattern}")
    
    logger.info(f"Project context built: {len(context['readme'])} chars of docs, "
                f"{len(context['file_structure'])} files, {len(context['main_files'])} entry points, "
                f"{len(context['config_files'])} config files")
    
    return context

@app.route('/')
def index():
    return jsonify({ 'msg': 'Hello World' })

@app.route('/ingest')
def ingest():
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] New ingest request received")
    
    llm = ChatOpenAI(
        # model='nemotron:70b',
        model='nemo',
        base_url="http://204.52.27.251:11434/v1",
        api_key='HACKATHON SAVE OUR SOULS',
        temperature=0
    )

    repo_url = request.args.get('repo_url')
    if not repo_url:
        logger.error(f"[{request_id}] No repo_url provided")
        return jsonify({ 'error': 'repo_url parameter is required' }), 400

    # Strip https:// or http:// prefix if present
    repo_url = repo_url.replace('https://', '').replace('http://', '')
    logger.info(f"[{request_id}] Processing repository: {repo_url}")
    
    folder_name = uuid.uuid4()
    clone_dir = f'tmp/{folder_name}'
    
    try:
        logger.info(f"[{request_id}] Cloning repository to {clone_dir}...")
        git.Repo.clone_from(f'https://{repo_url}', clone_dir, depth=1)
        logger.info(f"[{request_id}] Repository cloned successfully")
    except Exception as e:
        logger.error(f"[{request_id}] Failed to clone repo: {e}")
        return jsonify({ 'error': 'Failed to clone repository.' }), 500

    try:
        # 1. Detect dependencies
        logger.info(f"[{request_id}] Step 1/7: Detecting dependencies...")
        dependencies = detect_dependencies(clone_dir)

        # 2. Build comprehensive project context
        logger.info(f"[{request_id}] Step 2/7: Building project context...")
        project_context = build_project_context(clone_dir)
        
        # If README is empty/minimal, build context from file structure
        if len(project_context['readme'].strip()) < 100:
            logger.warning(f"[{request_id}] README is empty or minimal ({len(project_context['readme'])} chars), analyzing entire repo structure...")
            
            # Build a detailed context from what we can see
            context_parts = []
            context_parts.append(f"Repository: {repo_url}")
            context_parts.append(f"\nDetected Technologies: {', '.join(dependencies)}")
            
            # Analyze folder structure to infer project type and purpose
            all_folders = set()
            code_files_by_type = {}
            
            for root, dirs, files in os.walk(clone_dir):
                # Skip irrelevant dirs
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'Library', 'Temp', 'Logs', 'obj', 'bin', 'dist', 'build', '.next']]
                
                # Collect folder names
                for d in dirs:
                    all_folders.add(d)
                
                # Collect code files
                for file in files:
                    ext = os.path.splitext(file)[1]
                    if ext in ['.cs', '.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala']:
                        if ext not in code_files_by_type:
                            code_files_by_type[ext] = []
                        code_files_by_type[ext].append(os.path.join(root, file))
            
            # Generic folder pattern analysis - infer purpose from common patterns
            context_parts.append("\nProject Structure Analysis:")
            
            # Count folder types
            folder_list = sorted(list(all_folders))
            context_parts.append(f"  • Total folders: {len(folder_list)}")
            context_parts.append(f"  • Main directories: {', '.join(folder_list[:20])}")
            
            # Infer architecture patterns from folder names
            architecture_hints = []
            web_keywords = ['src', 'components', 'pages', 'routes', 'views', 'public', 'static', 'api', 'controllers']
            backend_keywords = ['models', 'controllers', 'services', 'middleware', 'routes', 'api', 'handlers']
            frontend_keywords = ['components', 'views', 'pages', 'layouts', 'styles', 'css', 'assets']
            data_keywords = ['models', 'schemas', 'migrations', 'database', 'db']
            test_keywords = ['test', 'tests', '__tests__', 'spec', 'e2e']
            config_keywords = ['config', 'configuration', 'settings', 'env']
            
            if any(kw in [f.lower() for f in all_folders] for kw in web_keywords):
                architecture_hints.append("Web application structure detected")
            if any(kw in [f.lower() for f in all_folders] for kw in backend_keywords):
                architecture_hints.append("Backend/API architecture present")
            if any(kw in [f.lower() for f in all_folders] for kw in frontend_keywords):
                architecture_hints.append("Frontend components structure")
            if any(kw in [f.lower() for f in all_folders] for kw in data_keywords):
                architecture_hints.append("Database/data layer included")
            if any(kw in [f.lower() for f in all_folders] for kw in test_keywords):
                architecture_hints.append("Testing infrastructure present")
            if any(kw in [f.lower() for f in all_folders] for kw in config_keywords):
                architecture_hints.append("Configuration management")
            
            if architecture_hints:
                for hint in architecture_hints:
                    context_parts.append(f"  • {hint}")
            
            # List significant directories with file counts
            context_parts.append("\nDirectory Contents:")
            dir_stats = []
            for folder in folder_list[:30]:  # Top 30 folders
                folder_path = None
                # Find the folder in the clone_dir
                for root, dirs, files in os.walk(clone_dir):
                    if folder in dirs:
                        folder_path = os.path.join(root, folder)
                        break
                
                if folder_path:
                    try:
                        file_count = sum([len(files) for _, _, files in os.walk(folder_path)])
                        if file_count > 0:
                            dir_stats.append(f"  • {folder}/ ({file_count} files)")
                    except:
                        pass
            
            for stat in sorted(dir_stats)[:20]:
                context_parts.append(stat)
            
            # Read sample code files to understand functionality
            context_parts.append("\n\nCode Analysis (sample files):")
            total_code_read = 0
            for ext, files in sorted(code_files_by_type.items())[:3]:  # Top 3 file types
                context_parts.append(f"\n{ext} files ({len(files)} total):")
                for code_file in files[:3]:  # First 3 of each type
                    try:
                        with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                            code_content = f.read(1500)  # First 1500 chars
                            rel_path = os.path.relpath(code_file, clone_dir)
                            context_parts.append(f"\n--- {rel_path} ---")
                            # Extract meaningful lines (skip empty lines and simple brackets)
                            meaningful_lines = [
                                line for line in code_content.split('\n')[:30] 
                                if line.strip() and line.strip() not in ['{', '}', '(', ')', ';']
                            ]
                            context_parts.append('\n'.join(meaningful_lines[:20]))  # First 20 meaningful lines
                            total_code_read += 1
                            if total_code_read >= 5:  # Max 5 files total
                                break
                    except Exception as e:
                        logger.warning(f"Could not read {code_file}: {e}")
                if total_code_read >= 5:
                    break
            
            # Add file structure overview
            context_parts.append(f"\n\nProject contains {len(project_context['file_structure'])} files")
            context_parts.append("\nKey Files and Folders (first 40):")
            for file in project_context['file_structure'][:40]:
                context_parts.append(f"  - {file}")
            
            # Add config files
            if project_context['config_files']:
                context_parts.append(f"\nConfiguration Files: {', '.join(project_context['config_files'])}")
            
            project_context['readme'] = '\n'.join(context_parts)
            logger.info(f"[{request_id}] Built intelligent synthetic context from repo analysis: {len(project_context['readme'])} chars, analyzed {total_code_read} code files")
        
        # 3. Extract repo name (clean it properly)
        logger.info(f"[{request_id}] Step 3/7: Extracting repo name...")
        raw_repo_name = repo_url.rstrip('/').split('/')[-1]
        if raw_repo_name.endswith('.git'):
            raw_repo_name = raw_repo_name[:-4]
        
        # Convert to kebab-case
        repo_name = raw_repo_name.lower().replace('_', '-').replace(' ', '-')
        logger.info(f"[{request_id}] Repo name: {raw_repo_name} -> {repo_name}")
        
        # 4. Get project name and description from LLM
        logger.info(f"[{request_id}] Step 4/7: Calling LLM for project name and description...")
        project_info = get_project_name(project_context['readme'], raw_repo_name, llm)
        
        # 5. Get goal/purpose
        logger.info(f"[{request_id}] Step 5/7: Calling LLM for project goal...")
        description_obj = get_description(content=project_context['readme'], llm=llm)
        goal = description_obj.description if description_obj else "A software project"

        # 6. Get installation steps
        logger.info(f"[{request_id}] Step 6/8: Calling LLM for installation steps...")
        install_steps = get_install_process(dependencies, clone_dir, project_context, llm)

        # 7. Get documentation pages (try deep analysis first, fallback to LLM)
        logger.info(f"[{request_id}] Step 7/8: Generating documentation pages...")
        pages = {}
        use_deep_analysis = request.args.get('deep_analysis', 'false').lower() == 'true'
        
        if use_deep_analysis:
            try:
                logger.info(f"[{request_id}] Starting deep code analysis (tree-sitter + LLM)...")
                full_repo_url = f"https://{repo_url}"
                analysis_result = analysis.analyze_repo(full_repo_url, llm)
                
                # Extract pages from analysis result and validate quality
                if analysis_result and 'pages' in analysis_result and len(analysis_result['pages']) > 0:
                    pages = analysis_result['pages']
                    logger.info(f"[{request_id}] Deep analysis returned {len(pages)} pages")
                    
                    # Check if the pages are just generic/placeholder content
                    # Look for telltale signs of bad generation like "0 file(s)" or "0 function(s)"
                    first_page_desc = next(iter(pages.values())) if pages else ""
                    if "0 file(s)" in first_page_desc or "0 function(s)" in first_page_desc or len(pages) < 3:
                        logger.warning(f"[{request_id}] Deep analysis returned low-quality pages (generic/placeholder content). Falling back to LLM.")
                        pages = get_pages(project_context, dependencies, llm)
                    else:
                        logger.info(f"[{request_id}] ✓ Deep analysis generated {len(pages)} quality pages")
                else:
                    logger.warning(f"[{request_id}] Deep analysis returned but no pages found")
                    pages = get_pages(project_context, dependencies, llm)
            except Exception as e:
                logger.error(f"[{request_id}] Deep analysis failed: {e}", exc_info=True)
                logger.info(f"[{request_id}] Falling back to standard LLM-based page generation")
                pages = get_pages(project_context, dependencies, llm)
        else:
            logger.info(f"[{request_id}] Using standard LLM-based page generation (add ?deep_analysis=true for code analysis)")
            pages = get_pages(project_context, dependencies, llm)

        # 8. Construct the result
        logger.info(f"[{request_id}] Constructing final result...")
        result = SerializedDoc(
            repo_name=repo_name,
            name=project_info.name if project_info else raw_repo_name,
            description=project_info.description if project_info else goal,
            goal=goal,
            dependencies=dependencies,
            installation=install_steps,
            pages=pages
        )

        result_dict = result.model_dump(by_alias=True)
        logger.info(f"[{request_id}] Result constructed with {len(pages)} documentation pages")
        
        # 9. Send to documentation generator API
        try:
            doc_gen_url = "http://204.52.26.255:8080/generate-docs"
            logger.info(f"[{request_id}] Sending to documentation generator: {doc_gen_url}")
            
            # Increase timeout to 5 minutes for large documentation generation
            resp = requests.post(
                doc_gen_url,
                json=result_dict,
                timeout=300  # 5 minutes - doc generation can take a while
            )
            
            logger.info(f"[{request_id}] Documentation generator response status: {resp.status_code}")
            
            if resp.status_code == 200:
                try:
                    doc_response = resp.json()
                    logger.info(f"[{request_id}] Documentation generated successfully!")
                    # Add the doc generation response to our result
                    result_dict['doc_generation'] = {
                        'status': 'success',
                        'response': doc_response
                    }
                except ValueError:
                    logger.warning(f"[{request_id}] Doc generator returned non-JSON response")
                    result_dict['doc_generation'] = {
                        'status': 'success',
                        'response_text': resp.text
                    }
            else:
                logger.error(f"[{request_id}] Documentation generator returned error: {resp.status_code} - {resp.text}")
                result_dict['doc_generation'] = {
                    'status': 'error',
                    'code': resp.status_code,
                    'message': resp.text
                }
                
        except requests.RequestException as e:
            logger.error(f"[{request_id}] Failed to send to documentation generator: {e}")
            result_dict['doc_generation'] = {
                'status': 'failed',
                'error': str(e)
            }

        logger.info(f"[{request_id}] Request completed successfully")
        return jsonify(result_dict)

    except Exception as e:
        logger.error(f"[{request_id}] Error occurred during processing: {e}", exc_info=True)
        return jsonify({ "msg": "An error occurred during processing.", "error": str(e)}), 500
    finally:
        if os.path.isdir(clone_dir):
            shutil.rmtree(clone_dir)
            logger.info(f"[{request_id}] Cleaned up temporary directory: {clone_dir}")

def get_project_name(content: str, fallback_name: str, llm):
    """Extract a human-readable project name and description."""
    logger.info("LLM call: Extracting project name and description")
    logger.debug(f"Context length: {len(content)} chars")
    try:
        structured_llm = llm.with_structured_output(ProjectName)
        prompt = ChatPromptTemplate.from_messages([
            ('system', '''You are a technical writer analyzing a real GitHub repository.

Your tasks:
1. Extract the ACTUAL project name from the README, code comments, or infer from the repository
2. Write a detailed, compelling description (2-4 sentences) of what this project IS and DOES

NAME requirements:
- Use the actual name if found in README headers, package.json, or code comments
- If no clear name exists, create a human-readable name based on the project's purpose
- Use Title Case for the name

DESCRIPTION requirements:
- Write in complete, natural sentences (not fragments or lists)
- Be SPECIFIC about features, mechanics, or capabilities you can see in the code/structure
- For games: Describe genre, gameplay, mechanics, visual elements, unique features
- For apps: Describe purpose, key features, target users, and what problems it solves  
- For libraries: Describe what it does, who uses it, and key capabilities
- DO NOT use generic phrases like "A software project" or "An application"
- Reference actual code features, file names, or technologies you observe

Examples:
- Name: "Castle of Time" / Description: "A 2D adventure game built in Unity featuring time-manipulation mechanics through a card-based system. Players navigate castle environments solving puzzles, with custom character controllers and animated combat sequences."
- Name: "TaskFlow Pro" / Description: "A collaborative task management web application built with React and Node.js. Features real-time updates, team workspaces, customizable workflows, and integration with popular productivity tools."'''),
            ('human', 'Project Content:\n{content}\n\nFallback name: {fallback}')
        ])
        chain = prompt | structured_llm
        response = chain.invoke({ 'content': content[:5000], 'fallback': fallback_name })
        logger.info(f"LLM response: name='{response.name}', description='{response.description[:100]}...'")
        return response
    except Exception as e:
        logger.error(f"Could not extract project name: {e}", exc_info=True)
        return None

def get_description(content: str, llm):
    logger.info("LLM call: Extracting project goal/description")
    logger.debug(f"Context length: {len(content)} chars")
    
    # Debug: Check if content is actually empty
    if not content or len(content.strip()) < 50:
        logger.warning("WARNING: Content is empty or very short! LLM will struggle with this.")
        logger.warning(f"Content preview: '{content[:200]}'")
    
    structured_llm = llm.with_structured_output(Description)
    prompt = ChatPromptTemplate.from_messages([
     ('system', '''You are a senior software engineer writing project documentation.

Your task is to write a compelling, detailed description (2-4 sentences) of what THIS SPECIFIC project is and does.

REQUIREMENTS:
- Write in complete, natural sentences (not bullet points or lists)
- Be SPECIFIC - mention actual features, gameplay mechanics, or unique aspects you see in the code/files
- For games: Describe the genre, gameplay, mechanics, visual style, or unique features
- For web apps: Describe the purpose, key features, tech stack, and what problems it solves
- For libraries/tools: Describe what it does, who it's for, and key capabilities
- DO NOT use generic phrases like "Specific Project Analysis" or "A software project"
- DO NOT just list technologies - explain what the project DOES with them
- If you see actual code or file names, reference specific features you can infer

Example GOOD descriptions:
- "A 2D platformer game built in Unity where players navigate through time-based puzzles using a card system to manipulate the environment. Features animated character controls, combat mechanics, and a unique visual style inspired by castle aesthetics."
- "A real-time chat application built with React and WebSocket that enables secure messaging with end-to-end encryption. Includes user authentication, message history, and file sharing capabilities."
- "A Python library for parsing and analyzing log files with support for multiple formats. Provides advanced filtering, statistical analysis, and customizable export options for DevOps teams."

Example BAD descriptions (too generic):
- "Specific Project Analysis"
- "A Unity game project"
- "A web application using React"'''),
     ('human', '{content}'),
    ])
    chain = prompt | structured_llm
    response = chain.invoke({ 'content': content[:6000]})  # Increased from 4000 to give more context
    logger.info(f"LLM response: goal='{response.description[:100]}...'")
    return response

def get_pages(project_context: dict, dependencies: list, llm) -> dict:
    """Generate documentation page structure based on ACTUAL project content.
    
    The LLM receives:
    - First 3000 chars of all README files combined
    - List of first 30 files in the repo structure
    - List of all main entry files found
    - List of config files
    - First 1000 chars of code samples
    """
    logger.info("LLM call: Generating documentation page structure")
    try:
        # Build detailed context for the LLM
        context_summary = f"""PROJECT ANALYSIS:

README Content (first 4000 chars):
{project_context['readme'][:4000]}

File Structure (first 50 files):
{chr(10).join(project_context['file_structure'][:50])}

Main Entry Files Found:
{chr(10).join(project_context['main_files']) if project_context['main_files'] else 'None'}

Config Files Found:
{', '.join(project_context['config_files']) if project_context['config_files'] else 'None'}

Technologies Detected:
{', '.join(dependencies)}

Code Samples:
{json.dumps(project_context['code_samples'], indent=2)[:1500]}

IMPORTANT: Generate 7-10 SPECIFIC sections based on what you see above. Each section MUST have a meaningful description that references actual project content.
"""
        
        logger.debug(f"Context sent to LLM: {len(context_summary)} chars")
        logger.info(f"Asking LLM to generate pages with {len(project_context['readme'])} chars of readme, {len(project_context['file_structure'])} files, {len(dependencies)} dependencies")
        
        structured_llm = llm.with_structured_output(Pages)
        prompt = ChatPromptTemplate.from_messages([
            ('system', '''You are a technical documentation architect analyzing a REAL repository.

YOUR TASK: Create 7-10 comprehensive documentation sections for this project.

CRITICAL REQUIREMENTS:
- You MUST return a valid object with a "pages" field containing a dictionary
- The dictionary MUST have 7-10 key-value pairs (section name to description)
- Each section name must be a clear, plain text title (no markdown, no numbering)
- Each description MUST be EXTREMELY SPECIFIC and reference ACTUAL files, directories, or code elements you see
- DO NOT return an empty dictionary
- DO NOT return null or undefined

DESCRIPTION REQUIREMENTS (READ CAREFULLY):
- ALWAYS mention specific file names (e.g., "main.py", "frontend/README.md", "schemas/SerializedDoc.py")
- ALWAYS mention specific directory names (e.g., "backend-jude/", "schemas/", "frontend/")
- ALWAYS mention specific technologies/frameworks you see in the file structure (e.g., "Flask", "React + Vite", "langchain_openai")
- ALWAYS mention specific config files (e.g., "package.json", "requirements.txt", "eslint.config.js")
- Reference actual code features, API endpoints, schema files, or database models you can infer
- Each description should be 2-4 sentences with CONCRETE details from THIS repository

Example GOOD descriptions (specific to a repo):
- "High-level introduction to the nvidia-track project, covering its dual nature with both frontend (React + Vite in /frontend) and backend (Python Flask in /backend-jude) components, as evidenced by frontend/README.md and backend-jude/main.py."
- "In-depth explanation of the backend structure built with Flask and LangChain, highlighting API endpoints in backend-jude/main.py and Pydantic schemas in schemas/ directory (SerializedDoc.py, Dependencies.py, Pages.py)."
- "Documentation of database schema design including Serialized Documents, Dependencies, Install Processes, and Project Names as defined in backend-jude/schemas/*.py files."

Example BAD descriptions (too generic):
- "Overview of the project and its features."
- "Guide to the main features and functionality."
- "Configuration options and environment setup."

Section ideas based on project type:

For GAMES (Unity/Unreal/Godot):
- Project Overview, Getting Started, Game Features, Core Systems, Level Design, Art & Assets, Audio System, Scripts & Components, Building & Deployment, Troubleshooting

For WEB APPS (React/Vue/Next.js/Express):
- Introduction, Quick Start, Installation, Architecture, Configuration, Features, API Documentation, Components, Database, Deployment, Contributing

For LIBRARIES/TOOLS:
- Introduction, Installation, Quick Start, Usage Guide, API Reference, Configuration, Advanced Features, Examples, Troubleshooting, Contributing

REMEMBER: Every description MUST reference specific files or directories from the repository!'''),
            ('human', '{context}')
        ])
        chain = prompt | structured_llm
        
        try:
            response = chain.invoke({ 'context': context_summary })
            logger.info(f"LLM response type: {type(response)}")
            logger.info(f"LLM response: {response}")
            
            # Check if response has pages attribute
            if not hasattr(response, 'pages'):
                logger.error(f"LLM response missing 'pages' attribute! Response: {response}")
                raise ValueError("LLM did not return valid Pages schema")
            
            logger.info(f"LLM generated {len(response.pages)} documentation sections")
            logger.debug(f"Raw LLM pages: {response.pages}")
        except Exception as llm_error:
            logger.error(f"LLM invocation failed: {llm_error}", exc_info=True)
            logger.warning("Using fallback page generation due to LLM error")
            # Return generic fallback immediately
            return {
                "Introduction": f"Overview of this project built with {', '.join(dependencies[:3]) if dependencies else 'various technologies'}.",
                "Quick Start": "Getting started guide with setup instructions.",
                "Installation": "Detailed installation and setup instructions.",
                "Features": "Guide to the main features and functionality.",
                "Configuration": "Configuration options and environment setup.",
                "Usage Examples": "Practical usage examples.",
                "Contributing": "Guidelines for contributing to the project."
            }
        
        # Sanitize page titles - remove markdown formatting and filter out empty/bad pages
        sanitized_pages = {}
        for title, description in response.pages.items():
            # Remove markdown bold/italic markers and other formatting
            clean_title = title.replace('**', '').replace('__', '').replace('*', '').replace('_', '').strip()
            # Remove any leading numbers or bullets (e.g., "1. ", "- ", "• ")
            clean_title = clean_title.lstrip('0123456789.- •').strip()
            
            # Skip pages with empty descriptions or too-short titles
            if description and len(description.strip()) > 0 and len(clean_title) > 2:
                sanitized_pages[clean_title] = description
            else:
                logger.warning(f"Skipping invalid page: '{clean_title}' with description: '{description}'")
        
        logger.info(f"Sanitized page titles ({len(sanitized_pages)} valid pages): {list(sanitized_pages.keys())}")
        
        # Ensure we have at least 7 sections (add smart defaults based on project type)
        if len(sanitized_pages) < 7:
            logger.warning(f"LLM returned only {len(sanitized_pages)} pages, adding intelligent defaults")
            
            # Determine project type from dependencies
            is_web_app = any(dep.lower() in ['react', 'vue', 'angular', 'next.js', 'express', 'node.js'] for dep in dependencies)
            is_game = any(dep.lower() in ['unity', 'unreal', 'godot'] for dep in dependencies)
            is_python = any(dep.lower() in ['python', 'flask', 'django', 'fastapi'] for dep in dependencies)
            has_api = 'api' in ' '.join(project_context['file_structure']).lower() or 'express' in dependencies
            has_config = len(project_context['config_files']) > 0
            
            # Detect specific file types for better defaults
            has_scripts = any('.cs' in f or '.py' in f or '.js' in f for f in project_context['file_structure'])
            has_assets = any('assets' in f.lower() or 'sprites' in f.lower() or 'textures' in f.lower() for f in project_context['file_structure'])
            has_audio = any('.mp3' in f or '.wav' in f or '.ogg' in f for f in project_context['file_structure'])
            has_scenes = any('.unity' in f or 'scenes' in f.lower() for f in project_context['file_structure'])
            
            # Build smart default pages based on project type
            default_pages = {}
            
            # GAME PROJECT DEFAULTS (Unity/Unreal/Godot)
            if is_game:
                if "Project Overview" not in sanitized_pages and "Introduction" not in sanitized_pages:
                    tech = dependencies[0] if dependencies else 'game engine'
                    default_pages["Project Overview"] = f"Overview of this game project built with {tech}, including genre, core gameplay concept, and target platform."
                
                if "Getting Started" not in sanitized_pages and "Setup" not in sanitized_pages:
                    default_pages["Getting Started"] = "Instructions for opening the project in the game engine, including required editor version and initial configuration."
                
                if "Game Features" not in sanitized_pages and "Gameplay" not in sanitized_pages and "Features" not in sanitized_pages:
                    default_pages["Game Features"] = "Detailed description of gameplay mechanics, core systems, and unique features that make this game stand out."
                
                if has_scripts and "Core Systems" not in sanitized_pages and "Scripts" not in sanitized_pages:
                    default_pages["Core Systems"] = "Documentation of key game systems including character controllers, game managers, input handling, and physics interactions."
                
                if has_scenes and "Level Design" not in sanitized_pages and "Scenes" not in sanitized_pages:
                    default_pages["Level Design"] = "Overview of scene structure, level layouts, prefab organization, and environment design principles used in the game."
                
                if has_assets and "Art & Assets" not in sanitized_pages and "Assets" not in sanitized_pages:
                    default_pages["Art & Assets"] = "Details on the visual style, sprite organization, materials, shaders, and asset pipeline used in the project."
                
                if has_audio and "Audio System" not in sanitized_pages and "Sound" not in sanitized_pages:
                    default_pages["Audio System"] = "Documentation of sound effects, music implementation, audio mixing, and the audio management system."
                
                if "Building & Deployment" not in sanitized_pages and "Build" not in sanitized_pages and "Deployment" not in sanitized_pages:
                    default_pages["Building & Deployment"] = "Instructions for building the game for different platforms (Windows, Mac, Linux, WebGL, mobile) and deployment considerations."
                
                if "Controls" not in sanitized_pages and "Input" not in sanitized_pages:
                    default_pages["Controls"] = "Player control schemes, input mappings, keyboard/mouse/gamepad configurations, and accessibility options."
                
                if "Troubleshooting" not in sanitized_pages and "FAQ" not in sanitized_pages:
                    default_pages["Troubleshooting"] = "Common issues developers may encounter when working with the project and their solutions."
            
            # WEB APP DEFAULTS (React/Vue/Next.js/Express)
            elif is_web_app:
                if "Introduction" not in sanitized_pages and "Overview" not in sanitized_pages:
                    tech_list = ', '.join(dependencies[:3]) if dependencies else 'modern web technologies'
                    default_pages["Introduction"] = f"Overview of this web application built with {tech_list}, its purpose, and key features."
                
                if "Quick Start" not in sanitized_pages and "Getting Started" not in sanitized_pages:
                    default_pages["Quick Start"] = "The fastest way to get the application running locally for development."
                
                if "Installation" not in sanitized_pages and "Setup" not in sanitized_pages:
                    default_pages["Installation"] = "Detailed installation instructions including all prerequisites, dependencies, and environment setup."
                
                if "Architecture" not in sanitized_pages and "Project Structure" not in sanitized_pages:
                    default_pages["Architecture"] = "Overview of the project's architecture, directory structure, design patterns, and key organizational principles."
                
                if has_config and "Configuration" not in sanitized_pages:
                    config_files = ', '.join(project_context['config_files'][:3])
                    default_pages["Configuration"] = f"Configuration options, environment variables, and settings using {config_files}."
                
                if "Features" not in sanitized_pages and "Usage Guide" not in sanitized_pages:
                    default_pages["Features"] = "Comprehensive guide to all features and functionality with usage examples and code snippets."
                
                if has_api and "API Documentation" not in sanitized_pages and "API" not in sanitized_pages:
                    default_pages["API Documentation"] = "Complete API reference including all endpoints, request/response formats, authentication, and examples."
                
                if "Components" not in sanitized_pages and "UI Components" not in sanitized_pages:
                    default_pages["Components"] = "Documentation of reusable UI components, their props, usage examples, and styling guidelines."
                
                if "Deployment" not in sanitized_pages and "Production" not in sanitized_pages:
                    default_pages["Deployment"] = "Instructions for deploying to production, including hosting options, CI/CD pipelines, and environment configuration."
                
                if "Contributing" not in sanitized_pages and "Development" not in sanitized_pages:
                    default_pages["Contributing"] = "Guidelines for contributing to the project, including development workflow, code standards, and pull request process."
            
            # PYTHON PROJECT DEFAULTS
            elif is_python:
                if "Introduction" not in sanitized_pages and "Overview" not in sanitized_pages:
                    default_pages["Introduction"] = "Overview of this Python project, its purpose, and key capabilities."
                
                if "Installation" not in sanitized_pages and "Setup" not in sanitized_pages:
                    default_pages["Installation"] = "Installation instructions including Python version requirements and dependency installation."
                
                if "Quick Start" not in sanitized_pages and "Getting Started" not in sanitized_pages:
                    default_pages["Quick Start"] = "Quick start guide with basic usage examples to get up and running immediately."
                
                if "Usage Guide" not in sanitized_pages and "Usage" not in sanitized_pages:
                    default_pages["Usage Guide"] = "Comprehensive usage guide with detailed examples and common use cases."
                
                if has_api and "API Reference" not in sanitized_pages and "API" not in sanitized_pages:
                    default_pages["API Reference"] = "Complete API documentation including all functions, classes, methods, and their parameters."
                
                if "Configuration" not in sanitized_pages and has_config:
                    default_pages["Configuration"] = "Configuration options, settings files, and environment variable documentation."
                
                if "Examples" not in sanitized_pages and "Code Examples" not in sanitized_pages:
                    default_pages["Examples"] = "Real-world examples demonstrating various use cases and advanced features."
                
                if "Contributing" not in sanitized_pages:
                    default_pages["Contributing"] = "Guidelines for contributing including development setup, testing, and code style."
            
            # GENERIC PROJECT DEFAULTS
            else:
                if "Introduction" not in sanitized_pages and "Overview" not in sanitized_pages:
                    tech_list = ', '.join(dependencies[:3]) if dependencies else 'various technologies'
                    default_pages["Introduction"] = f"Overview of this project built with {tech_list}."
                
                if "Installation" not in sanitized_pages and "Setup" not in sanitized_pages:
                    default_pages["Installation"] = "Step-by-step installation and setup instructions."
                
                if "Usage Guide" not in sanitized_pages and "Quick Start" not in sanitized_pages:
                    default_pages["Usage Guide"] = "Guide to using the main features of this project."
                
                if has_config and "Configuration" not in sanitized_pages:
                    default_pages["Configuration"] = "Configuration options and settings."
                
                if "Examples" not in sanitized_pages:
                    default_pages["Examples"] = "Practical usage examples and code snippets."
                
                if "Contributing" not in sanitized_pages:
                    default_pages["Contributing"] = "Guidelines for contributing to the project."
                
                if "Deployment" not in sanitized_pages:
                    default_pages["Deployment"] = "Deployment instructions and best practices."
            
            # Merge defaults with existing pages (existing pages take precedence)
            merged_pages = {**default_pages, **sanitized_pages}
            
            logger.info(f"Added {len(default_pages)} default pages. Total pages: {len(merged_pages)}")
            logger.info(f"Final page titles: {list(merged_pages.keys())}")
            
            return merged_pages
        
        return sanitized_pages
    except Exception as e:
        logger.error(f"Could not generate pages: {e}", exc_info=True)
        return {
            "Introduction": "Overview of the project and its features.",
            "Quick Start": "Getting started quickly.",
            "Installation": "Detailed setup instructions.",
            "Configuration": "Environment and configuration details.",
            "Usage Examples": "Practical usage examples."
        }

def get_install_process(dependencies: list, clone_dir: str, project_context: dict, llm) -> list:
    """Generate installation steps as a list based on ACTUAL project structure.
    
    The LLM receives:
    - Detected dependencies
    - Config files present
    - Main files found
    - First 2000 chars of README (looking for installation instructions)
    """
    logger.info("LLM call: Generating installation steps")
    if not dependencies:
        logger.info("No dependencies found, returning minimal steps")
        return ["Clone the repository", "Refer to the project's documentation for setup instructions"]
    
    try:
        # Build rich context
        context = f"""ACTUAL PROJECT DETAILS:

Dependencies Detected: {', '.join(dependencies)}

Config Files Present: {', '.join(project_context['config_files'])}

Main Files: {', '.join(project_context['main_files'])}

README Installation Section:
{project_context['readme'][:2000]}
"""
        
        logger.debug(f"Context sent to LLM: {len(context)} chars")
        
        structured_llm = llm.with_structured_output(InstallProcess)
        prompt = ChatPromptTemplate.from_messages([
            ('system', '''You are a senior software engineer writing installation documentation for a REAL project.

Generate 4-7 clear, actionable installation steps based on the ACTUAL files and structure you see.

REQUIREMENTS:
- Be SPECIFIC to this project - reference actual files you see (package.json, requirements.txt, etc.)
- Keep steps concise 
- Use actual commands (npm install, pip install -r requirements.txt, etc.)
- Order: clone → install toolchain → install deps → configure → run
- DO NOT write paragraphs or use markdown formatting
- Each step should be a plain string, one action

Example good steps:
- "Clone the repository: git clone <url>"
- "Install Node.js 18+ from nodejs.org"
- "Run npm install to install dependencies"
- "Copy .env.example to .env and configure your API keys"
- "Start the dev server: npm run dev"

Example BAD steps (too verbose):
- "**1. Clone/Download the Repository** Using Git: Open your terminal..."'''),
            ('human', '{context}')
        ])
        chain = prompt | structured_llm
        response = chain.invoke({ 'context': context })
        logger.info(f"LLM generated {len(response.installation)} installation steps")
        return response.installation
    except Exception as e:
        logger.error(f"Could not generate install process via LLM: {e}", exc_info=True)
        
        # Fallback based on what we actually detected
        logger.info("Using fallback installation steps")
        steps = ["Clone the repository"]
        
        if 'package.json' in project_context['config_files']:
            steps.append("Install Node.js from nodejs.org")
            steps.append("Run: npm install")
            steps.append("Run: npm start or npm run dev")
        elif 'requirements.txt' in project_context['config_files']:
            steps.append("Install Python 3.8+")
            steps.append("Run: pip install -r requirements.txt")
            steps.append("Run: python main.py or python app.py")
        else:
            steps.append("Refer to README.md for setup instructions")
        
        return steps

app.run(debug=True, host='0.0.0.0', port=3333)

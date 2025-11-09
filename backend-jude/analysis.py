import os
import json
import git
import importlib
import warnings
from tree_sitter import Language, Parser
import time
import shutil
import uuid

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Dict

# --- Pydantic Models for Enrichment ---
class FunctionInput(BaseModel):
    name: str
    description: str

class FunctionSummary(BaseModel):
    purpose: str = Field(description="A concise, one-sentence summary of what this function's primary goal is.")
    inputs: List[FunctionInput] = Field(description="An array of objects. Each object should have 'name' and 'description'. If no inputs, return an empty array.")
    outputs: str = Field(description="A string describing what this function returns. If it returns nothing (void), describe that.")
    dependencies: List[str] = Field(description="An array of strings, listing any key libraries or modules used within this function.")

# --- Logic from 1_build_skeleton.py ---

LANGUAGE_CONFIG = {
    'python': {
        'extensions': ['py'],
        'grammar_name': 'python',
        'function_node_type': 'function_definition',
        'function_name_field': 'name',
        'call_node_type': 'call',
        'call_function_field': 'function'
    },
    'javascript': {
        'extensions': ['js', 'jsx', 'ts', 'tsx'],
        'grammar_name': 'javascript',
        'function_node_types': ['function_declaration', 'method_definition', 'arrow_function'],
        'function_name_field': 'name',
        'call_node_type': 'call_expression',
        'call_function_field': 'function'
    },
    'java': {
        'extensions': ['java'],
        'grammar_name': 'java',
        'function_node_type': 'method_declaration',
        'function_name_field': 'name',
        'call_node_type': 'method_invocation',
        'call_function_field': 'name'
    }
}

class MultiLanguageParser:
    def __init__(self, config):
        self.config = config
        self.extension_map = {}

    def load_languages(self):
        print("Loading languages from installed packages...")
        for lang, conf in self.config.items():
            lang_name = conf['grammar_name']
            package_name = f"tree_sitter_{lang_name}"
            try:
                lang_module = importlib.import_module(package_name)
                language_func = getattr(lang_module, 'language')
                language_capsule = language_func()
                language_object = Language(language_capsule)
                parser = Parser(language_object)
                
                parser_tuple = (parser, language_object, conf)
                for ext in conf['extensions']:
                    self.extension_map[f".{ext}"] = parser_tuple
                print(f"  Successfully loaded '{lang_name}' (from {package_name})")
            except ImportError:
                print(f" WARNING: Failed to import '{package_name}'.")
                print(f" Did you run: pip install {package_name.replace('_', '-')}")
            except Exception as e:
                print(f" ERROR: Failed to load '{lang_name}': {e}")

    def get_parser(self, file_extension):
        return self.extension_map.get(file_extension)

def traverse_tree(node, node_type):
    if node.type == node_type:
        yield node
    for child in node.children:
        yield from traverse_tree(child, node_type)

def get_node_text(node):
    try:
        return node.text.decode('utf-8')
    except:
        return ""

def get_function_name(func_node, name_field):
    try:
        name_node = func_node.child_by_field_name(name_field)
        if name_node:
            return get_node_text(name_node)
        for child in func_node.children:
            if child.type == 'identifier' or child.type == 'property_identifier':
                return get_node_text(child)
    except:
        pass
    return None

def get_calls_in_function(func_node, call_node_type, call_function_field):
    calls = []
    for call_node in traverse_tree(func_node, call_node_type):
        try:
            func_name_node = call_node.child_by_field_name(call_function_field)
            if func_name_node:
                if func_name_node.type == 'identifier':
                    call_name = get_node_text(func_name_node)
                    if call_name:
                        calls.append(call_name)
            else:
                for child in call_node.children:
                    if child.type == 'identifier':
                        call_name = get_node_text(child)
                        if call_name:
                            calls.append(call_name)
                            break
        except:
            pass
    return calls

def parse_file(file_path, parser, language_object, config):
    functions = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        code_bytes = bytes(code, "utf8")
    except Exception as e:
        print(f" Skipping (could not read): {e}")
        return {}

    try:
        tree = parser.parse(code_bytes)
        root = tree.root_node
    except Exception as e:
        print(f" Skipping (parsing error): {e}")
        return {}

    try:
        func_node_types = config.get('function_node_types', [config.get('function_node_type')])
        if isinstance(func_node_types, str):
            func_node_types = [func_node_types]
        
        for func_type in func_node_types:
            if not func_type:
                continue
                
            for func_node in traverse_tree(root, func_type):
                func_name = get_function_name(func_node, config.get('function_name_field', 'name'))
                
                if not func_name:
                    continue
                
                code_snippet = get_node_text(func_node)
                
                calls = get_calls_in_function(
                    func_node, 
                    config.get('call_node_type', 'call'),
                    config.get('call_function_field', 'function')
                )
                
                functions[func_name] = {
                    "code_snippet": code_snippet,
                    "calls": list(set(calls))
                }
    except Exception as e:
        print(f"Could not parse functions: {e}")
    
    return functions

def build_skeleton_graph(repo_url, clone_dir):
    parser_manager = MultiLanguageParser(LANGUAGE_CONFIG)
    parser_manager.load_languages()

    graph = {
        "repository_url": repo_url,
        "file_system_map": {},
        "functions": {}
    }

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for root, dirs, files in os.walk(clone_dir, topdown=True):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
            relative_root = os.path.relpath(root, clone_dir)
            if relative_root == '.':
                relative_root = '/'
            else:
                relative_root = f"/{relative_root.replace(os.sep, '/')}"
            if files:
                graph["file_system_map"][relative_root] = files
            for file in files:
                file_path = os.path.join(root, file)
                _, file_ext = os.path.splitext(file)
                parser_tuple = parser_manager.get_parser(file_ext)
                if parser_tuple:
                    relative_path = os.path.relpath(file_path, clone_dir).replace('\\', '/')
                    parser, lang_obj, config = parser_tuple
                    file_functions = parse_file(file_path, parser, lang_obj, config)
                    for func_name, func_data in file_functions.items():
                        function_key = f"{relative_path}::{func_name}"
                        if function_key in graph["functions"]:
                            i = 2
                            while f"{function_key}_{i}" in graph["functions"]:
                                i += 1
                            function_key = f"{function_key}_{i}"
                        graph["functions"][function_key] = {
                            "file_path": relative_path,
                            "function_name": func_name,
                            "code_snippet": func_data["code_snippet"],
                            "calls": func_data["calls"],
                            "summary": None
                        }
    return graph

# --- Logic from 2_enrich_graph.py ---

SYSTEM_PROMPT = """
You are an expert senior software architect. Your task is to analyze a code snippet
and provide a structured JSON analysis. Your response MUST be a single, minified JSON
object. Do not include any preamble, postamble, or markdown code blocks.
The JSON object must have these exact keys:
- "purpose": A concise, one-sentence summary of what this function's primary goal is.
- "inputs": An array of objects. Each object should have "name" and "description". If no inputs, return an empty array.
- "outputs": A string describing what this function returns. If it returns nothing (void), describe that.
- "dependencies": An array of strings, listing any key libraries or modules used within this function.
"""

def enrich_graph(graph_data, llm):
    # It's better to pass the LLM from main.py so we can configure it there
    structured_llm = llm.with_structured_output(FunctionSummary)
    prompt = ChatPromptTemplate.from_messages([
        ('system', SYSTEM_PROMPT),
        ('human', "Code Snippet:\n```\n{code_snippet}\n```")
    ])
    chain = prompt | structured_llm

    functions_to_process = [
        (key, info) for key, info in graph_data["functions"].items()
        if info.get("summary") is None
    ]
    
    total_count = len(functions_to_process)
    print(f"\nFound {total_count} functions to process")
    
    for i, (function_key, function_info) in enumerate(functions_to_process):
        print(f"[{i+1}/{total_count}] {function_key}")
        code_snippet = function_info["code_snippet"]
        
        try:
            # Truncate very long snippets
            if len(code_snippet) > 3000:
                code_snippet = code_snippet[:3000] + "\n... (truncated for token limit)"
            
            summary_object = chain.invoke({'code_snippet': code_snippet})
            graph_data["functions"][function_key]["summary"] = summary_object.dict()
            print(f"  ✓ Success")
            
        except Exception as e:
            print(f"  ✗ FAILED to enrich {function_key}: {str(e)[:100]}")
            
    return graph_data

def generate_pages_from_graph(enriched_graph):
    """
    Generate a pages dictionary from the enriched graph.
    Groups functions by file and creates comprehensive summaries.
    """
    pages = {}
    
    # Group functions by file
    file_functions = {}
    for func_key, func_info in enriched_graph.get("functions", {}).items():
        file_path = func_info.get("file_path", "unknown")
        if file_path not in file_functions:
            file_functions[file_path] = []
        file_functions[file_path].append((func_key, func_info))
    
    # Generate page summaries for each file
    for file_path, functions in file_functions.items():
        # Create a readable page title from file path
        page_title = file_path.replace('/', ' > ').replace('.py', '').replace('.js', '').replace('.java', '')
        
        # Build comprehensive summary for this file
        summary_parts = []
        summary_parts.append(f"This file contains {len(functions)} function(s):")
        
        for func_key, func_info in functions:
            func_name = func_info.get("function_name", "unknown")
            summary = func_info.get("summary", {})
            
            if summary:
                purpose = summary.get("purpose", "No description available")
                inputs = summary.get("inputs", [])
                outputs = summary.get("outputs", "No return value")
                dependencies = summary.get("dependencies", [])
                
                func_summary = f"\n\n**{func_name}**: {purpose}"
                
                if inputs:
                    input_desc = ", ".join([f"{inp.get('name', 'param')} ({inp.get('description', 'no desc')})" for inp in inputs])
                    func_summary += f" Takes inputs: {input_desc}."
                
                func_summary += f" Returns: {outputs}."
                
                if dependencies:
                    func_summary += f" Uses: {', '.join(dependencies)}."
                
                summary_parts.append(func_summary)
            else:
                summary_parts.append(f"\n\n**{func_name}**: Function analysis pending or failed.")
        
        pages[page_title] = " ".join(summary_parts)
    
    # Add a high-level overview page
    total_functions = len(enriched_graph.get("functions", {}))
    total_files = len(file_functions)
    overview = f"This project contains {total_files} file(s) with a total of {total_functions} function(s). "
    overview += f"The codebase has been analyzed to understand the purpose, inputs, outputs, and dependencies of each function. "
    overview += f"The analysis covers the complete project structure and provides detailed insights into each component."
    
    pages["Project Overview"] = overview
    
    return pages

# --- Orchestrator Function ---

def analyze_repo(repo_url, llm):
    """
    Analyzes a repository and returns a dictionary with enriched graph and generated pages.
    Returns a dict with keys: 'graph' (the enriched graph) and 'pages' (the generated pages dict)
    """
    folder_name = uuid.uuid4()
    clone_dir = f'tmp/{folder_name}'
    
    try:
        print(f"Cloning {repo_url} into {clone_dir}...")
        git.Repo.clone_from(repo_url, clone_dir, depth=1)
        
        print("\nBuilding skeleton graph...")
        skeleton_graph = build_skeleton_graph(repo_url, clone_dir)
        
        print("\nEnriching graph with LLM summaries...")
        enriched_graph = enrich_graph(skeleton_graph, llm)
        
        print("\nGenerating pages from enriched graph...")
        pages = generate_pages_from_graph(enriched_graph)
        
        print("\nAnalysis complete.")
        return {
            'graph': enriched_graph,
            'pages': pages
        }

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        # Re-raise the exception to be handled by the caller
        raise
    finally:
        # Clean up the cloned repo
        if os.path.isdir(clone_dir):
            print(f"Cleaning up {clone_dir}...")
            shutil.rmtree(clone_dir)
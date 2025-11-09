import sys
import os
import json
import git
import importlib
import warnings
from tree_sitter import Language, Parser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_CLONE_DIR = os.path.join(SCRIPT_DIR, 'temp_repo')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'skeleton_graph.json')

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
    """Recursively find all nodes of a given type."""
    if node.type == node_type:
        yield node
    for child in node.children:
        yield from traverse_tree(child, node_type)

def get_node_text(node):
    """Safely get text from a node."""
    try:
        return node.text.decode('utf-8')
    except:
        return ""

def get_function_name(func_node, name_field):
    """Extract function name from a function node."""
    try:
        # Try to get the name via field
        name_node = func_node.child_by_field_name(name_field)
        if name_node:
            return get_node_text(name_node)
        
        # Fallback: look for identifier in children
        for child in func_node.children:
            if child.type == 'identifier' or child.type == 'property_identifier':
                return get_node_text(child)
    except:
        pass
    return None

def get_calls_in_function(func_node, call_node_type, call_function_field):
    """Find all function calls within a function node."""
    calls = []
    for call_node in traverse_tree(func_node, call_node_type):
        try:
            # Try to get the function name via field
            func_name_node = call_node.child_by_field_name(call_function_field)
            if func_name_node:
                if func_name_node.type == 'identifier':
                    call_name = get_node_text(func_name_node)
                    if call_name:
                        calls.append(call_name)
            else:
                # Fallback: look for identifier in children
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
        # Get function node type(s)
        func_node_types = config.get('function_node_types', [config.get('function_node_type')])
        if isinstance(func_node_types, str):
            func_node_types = [func_node_types]
        
        # Find all function definitions
        for func_type in func_node_types:
            if not func_type:
                continue
                
            for func_node in traverse_tree(root, func_type):
                func_name = get_function_name(func_node, config.get('function_name_field', 'name'))
                
                if not func_name:
                    continue
                
                # Get the code snippet
                code_snippet = get_node_text(func_node)
                
                # Find all calls within this function
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
        import traceback
        traceback.print_exc()
        return {}
    
    return functions

def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        print(f"Pulling latest changes in {clone_dir}...")
        try:
            repo = git.Repo(clone_dir)
            repo.remotes.origin.pull()
        except Exception as e:
            print(f"Could not pull repo: {e}. Using existing files.")
    else:
        print(f"Cloning {repo_url} into {clone_dir}...")
        try:
            git.Repo.clone_from(repo_url, clone_dir)
        except Exception as e:
            print(f"Could not clone repo: {e}")
            return False
    return True

def main(repo_url):
    parser_manager = MultiLanguageParser(LANGUAGE_CONFIG)
    parser_manager.load_languages()
    print("\nParser setup complete.")
    print(f"Loaded parsers for extensions: {list(parser_manager.extension_map.keys())}")

    if not clone_repo(repo_url, TEMP_CLONE_DIR):
        print("Failed to clone repo. Aborting.")
        return

    graph = {
        "repository_url": repo_url,
        "file_system_map": {},
        "functions": {}
    }

    print(f"\nStarting file scan in {TEMP_CLONE_DIR}...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for root, dirs, files in os.walk(TEMP_CLONE_DIR, topdown=True):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
            relative_root = os.path.relpath(root, TEMP_CLONE_DIR)
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
                    relative_path = os.path.relpath(file_path, TEMP_CLONE_DIR).replace('\\', '/')
                    print(f"  Parsing [{file_ext}]: {relative_path}")
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
    print(f"\nParsing complete. Saving skeleton graph to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2)
    print(f"Done. Found {len(graph['functions'])} functions.")
    print(f"Next step: Run '2_enrich_graph.py' to add summaries.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 1_build_skeleton.py <repo_url>")
        sys.exit(1)
    repo_url_arg = sys.argv[1]
    main(repo_url_arg)
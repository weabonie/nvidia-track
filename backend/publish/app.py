# app.py
import os, json, re, subprocess, shutil, socket, logging
from pathlib import Path
from typing import Dict, Any
from flask import Flask, request, jsonify
import requests
from portmap import PortMap

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Loaded .env file")
except ImportError:
    logger.warning("python-dotenv not installed, using environment variables only")
    pass

# ---- Config ----
OLLAMA_MODEL  = os.getenv("OLLAMA_MODEL", "llama3.1")
OLLAMA_URL    = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
SITES_ROOT    = Path(os.getenv("SITES_ROOT", "./generated_sites")).resolve()
DOCKER_NETWORK = os.getenv("DOCKER_NETWORK", "docs_net")  # optional, will create if absent
BASE_DOMAIN   = os.getenv("BASE_DOMAIN", "siru.dev")      # e.g., repo-name-doc.siru.dev

# NPM (Nginx Proxy Manager) API config
NPM_ENABLED   = os.getenv("NPM_ENABLED", "false").lower() == "true"
NPM_HOST      = os.getenv("NPM_HOST", "http://npm-server.example.com")  # NPM server URL
NPM_EMAIL     = os.getenv("NPM_EMAIL", "admin@example.com")
NPM_PASSWORD  = os.getenv("NPM_PASSWORD", "changeme")
DOCS_SERVER_IP = os.getenv("DOCS_SERVER_IP", "127.0.0.1")  # This server's IP that NPM will forward to

logger.info(f"Config loaded:")
logger.info(f"  OLLAMA_MODEL: {OLLAMA_MODEL}")
logger.info(f"  OLLAMA_URL: {OLLAMA_URL}")
logger.info(f"  SITES_ROOT: {SITES_ROOT}")
logger.info(f"  BASE_DOMAIN: {BASE_DOMAIN}")
logger.info(f"  NPM_ENABLED: {NPM_ENABLED}")
logger.info(f"  DOCS_SERVER_IP: {DOCS_SERVER_IP}")

app = Flask(__name__)
ports = PortMap(SITES_ROOT / ".ports.json", base=18080, limit=2000)

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")

def require_keys(obj: Dict[str, Any], ks):
    miss = [k for k in ks if k not in obj]
    if miss: raise ValueError("Missing keys: " + ", ".join(miss))

def ensure_net(name: str):
    subprocess.run(["docker", "network", "inspect", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if _.returncode if (_:=subprocess.CompletedProcess(args=[], returncode=0)) else False:  # dummy
        pass
    # Re-run properly (above trick to quiet linters)
    res = subprocess.run(["docker", "network", "inspect", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        subprocess.check_call(["docker", "network", "create", name])

def call_ollama(payload: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = """You are a precise Docusaurus documentation generator. 
    
CRITICAL RULES:
1. Output ONLY valid JSON - no markdown, no code fences, no commentary
2. All files MUST have YAML front matter with id, title, and sidebar_position
3. File paths must be docs/SLUG.md where SLUG is lowercase-with-dashes
4. Create comprehensive, well-structured documentation content
5. ABSOLUTELY NO SPECIAL CHARACTERS for placeholders - MDX/React interprets them as code
   - For API paths with parameters, use UPPERCASE: /api/users/USER_ID or /api/users/USERID
   - For placeholders: use UPPERCASE_WORDS like PROJECT_ID, USER_NAME, etc.
   - NEVER use: {}, <>, :, or any symbols OUTSIDE code blocks - ONLY letters, numbers, underscore, hyphen
6. CODE BLOCKS: CRITICAL FORMATTING
   - Use EXACTLY three backticks (```) at start of code block on its own line
   - NEVER write "code```" or "Example:```" or put ANY text before the backticks
   - Put backticks on their OWN line: text here, then newline, then ```
   - Format: ```language on one line, then code, then ``` on its own line
   - Always close code blocks properly with three backticks on their own line
   - Inside code blocks, write COMPLETE, VALID code - no incomplete JSX attributes
   - If showing JSX/React: use COMPLETE props like data={{}} or options={{}} not data= or options=
7. Never use malformed code fences or incomplete code examples
8. Keep it simple - use plain text and UPPERCASE for placeholders OUTSIDE code blocks

JSON SCHEMA (FOLLOW EXACTLY):
{
  "files": [
    {"path": "docs/intro.md", "content": "---\\nid: intro\\ntitle: Introduction\\nsidebar_position: 1\\n---\\n\\n# Title\\n\\nContent here"}
  ]
}"""

    # Build file list from pages input
    pages = payload.get('pages', {})
    file_instructions = []
    for i, (page_name, page_desc) in enumerate(pages.items(), 1):
        file_slug = slugify(page_name)
        file_instructions.append(f"""
{i}. docs/{file_slug}.md (id: {file_slug}, sidebar_position: {i})
   Page Title: "{page_name}"
   Content Focus: {page_desc}
   - Use project info to create relevant content
   - Include code examples where appropriate
   - Make it comprehensive and useful""")

    user_prompt = f"""Generate Docusaurus documentation for this project:

PROJECT INFO:
- Name: {payload.get('name')}
- Description: {payload.get('description')}
- Goal: {payload.get('goal')}
- Dependencies: {', '.join(payload.get('dependencies', []))}
- Installation Steps: {', '.join(payload.get('installation', []))}

CREATE EXACTLY {len(pages)} FILES:
{''.join(file_instructions)}

IMPORTANT:
- First file ({list(pages.keys())[0]}) is the HOMEPAGE
- Use YAML front matter: id, title, sidebar_position
- Make content detailed and useful based on page description
- Include code blocks with proper syntax highlighting
- Use Markdown formatting (headers, lists, links, etc.)

OUTPUT: JSON with "files" array only. No other text."""

    r = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "messages": [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        "format":"json",
        "stream":False
    }, timeout=120)
    r.raise_for_status()
    content = r.json().get("message",{}).get("content")
    if not content: raise RuntimeError("Ollama returned empty content")
    
    # Log raw response for debugging
    logger.debug(f"Raw Ollama response: {content[:500]}...")
    
    try:
        bundle = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Ollama JSON: {e}")
        logger.error(f"Content was: {content[:1000]}")
        raise RuntimeError(f"Ollama returned invalid JSON: {e}")
    
    if "files" not in bundle or not isinstance(bundle["files"], list):
        logger.error(f"Bundle structure: {bundle}")
        raise RuntimeError('Model JSON missing "files" array')
    
    # Validate file structure
    for i, f in enumerate(bundle["files"]):
        if isinstance(f, str):
            logger.error(f"File {i} is a string, not an object: {f[:100]}")
            raise RuntimeError(f"File {i} is malformed - expected object with 'path' and 'content'")
        if not isinstance(f, dict):
            raise RuntimeError(f"File {i} is not a dict: {type(f)}")
        if "path" not in f or "content" not in f:
            raise RuntimeError(f"File {i} missing required keys. Has: {list(f.keys())}")
    
    logger.info(f"Files to be created: {[f.get('path') for f in bundle['files']]}")
    return bundle

def write_minimal_docusaurus(site_dir: Path, site_title: str, site_base_url: str, pages: dict):
    # Minimal classic preset scaffold
    (site_dir / "docs").mkdir(parents=True, exist_ok=True)
    (site_dir / "static").mkdir(parents=True, exist_ok=True)
    (site_dir / "src").mkdir(parents=True, exist_ok=True)
    (site_dir / "src" / "css").mkdir(parents=True, exist_ok=True)

    (site_dir / "package.json").write_text(json.dumps({
        "name": site_title.lower().replace(" ", "-"),
        "private": True,
        "scripts": {
            "build": "docusaurus build",
            "serve": "docusaurus serve --host 0.0.0.0 --port 3000",
            "start": "docusaurus start --host 0.0.0.0 --port 3000"
        },
        "dependencies": {
            "@docusaurus/core": "3.5.2",
            "@docusaurus/preset-classic": "3.5.2",
            "prism-react-renderer": "^2.3.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        }
    }, indent=2), encoding="utf-8")

    (site_dir / "docusaurus.config.js").write_text(f"""\
import {{themes as prismThemes}} from 'prism-react-renderer';

/** @type {{import('@docusaurus/types').Config}} */
const config = {{
  title: '{site_title}',
  url: 'https://{site_base_url}',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'docs', 
  projectName: '{site_title}',
  
  presets: [
    [
      'classic',
      /** @type {{import('@docusaurus/preset-classic').Options}} */
      ({{
        docs: {{
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
        }},
        blog: false,
        theme: {{
          customCss: './src/css/custom.css',
        }},
      }}),
    ],
  ],

  themeConfig:
    /** @type {{import('@docusaurus/preset-classic').ThemeConfig}} */
    ({{
      colorMode: {{
        defaultMode: 'dark',
        respectPrefersColorScheme: true,
      }},
      navbar: {{
        title: '{site_title}',
        items: [],
      }},
      prism: {{
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      }},
    }}),
}};

export default config;
""", encoding="utf-8")

    # Create custom NVIDIA green theme CSS
    (site_dir / "src" / "css" / "custom.css").write_text("""/**
 * NVIDIA Green Theme for Docusaurus
 * Primary color: #76B900 (NVIDIA Green)
 */

:root {
  /* NVIDIA Green color palette */
  --ifm-color-primary: #76B900;
  --ifm-color-primary-dark: #6aa600;
  --ifm-color-primary-darker: #649d00;
  --ifm-color-primary-darkest: #528100;
  --ifm-color-primary-light: #82cc00;
  --ifm-color-primary-lighter: #88d500;
  --ifm-color-primary-lightest: #9ee116;
  
  /* Code block background */
  --ifm-code-font-size: 95%;
  
  /* Link colors */
  --ifm-link-color: #76B900;
  --ifm-link-hover-color: #6aa600;
}

/* Dark mode adjustments */
[data-theme='dark'] {
  --ifm-color-primary: #82cc00;
  --ifm-color-primary-dark: #76b900;
  --ifm-color-primary-darker: #6aa600;
  --ifm-color-primary-darkest: #5e9300;
  --ifm-color-primary-light: #88d500;
  --ifm-color-primary-lighter: #9ee116;
  --ifm-color-primary-lightest: #a8e62c;
  
  --ifm-link-color: #82cc00;
  --ifm-link-hover-color: #9ee116;
}

/* Navbar styling */
.navbar {
  background-color: #1a1a1a;
  border-bottom: 2px solid #76B900;
}

.navbar__title {
  color: #76B900 !important;
  font-weight: 600;
}

/* Sidebar active item */
.menu__link--active {
  background-color: rgba(118, 185, 0, 0.1);
  border-left: 3px solid #76B900;
}

/* Code blocks with NVIDIA accent */
.prism-code {
  border-left: 3px solid #76B900;
}

/* Buttons and interactive elements */
.button--primary {
  background-color: #76B900;
  border-color: #76B900;
}

.button--primary:hover {
  background-color: #6aa600;
  border-color: #6aa600;
}

/* Headings accent */
h1, h2, h3, h4, h5, h6 {
  color: inherit;
}

article h1 {
  border-bottom: 3px solid #76B900;
  padding-bottom: 0.5rem;
}
""", encoding="utf-8")

    # Build sidebar from pages input
    sidebar_items = []
    for i, (page_name, _) in enumerate(pages.items(), 1):
        file_slug = slugify(page_name)
        sidebar_items.append(f'    {{type: "doc", id: "{file_slug}", label: "{page_name}"}}')
    
    sidebar_content = ",\n".join(sidebar_items)
    (site_dir / "sidebars.js").write_text(f"""\
/** @type {{import('@docusaurus/plugin-content-docs').SidebarsConfig}} */
export default {{
  tutorialSidebar: [
{sidebar_content}
  ],
}};
""", encoding="utf-8")

def fix_mdx_curly_braces(content: str) -> str:
    """
    SANITIZE MDX content to prevent React/JSX parsing errors.
    - Remove problematic curly braces OUTSIDE code blocks (MDX treats them as JS expressions)
    - Replace angle brackets that look like HTML/JSX tags OUTSIDE code blocks
    - Replace :param syntax with safe UPPERCASE
    - Fix malformed code fences
    - Preserves code blocks and frontmatter completely unchanged.
    """
    lines = content.split('\n')
    result = []
    in_code_block = False
    in_frontmatter = False
    frontmatter_count = 0
    
    for i, line in enumerate(lines):
        # Track frontmatter (YAML front matter between --- markers)
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count <= 2:
                in_frontmatter = True
            if frontmatter_count == 2:
                in_frontmatter = False
            result.append(line)
            continue
        
        # Fix malformed code fences - check for ``' or other common issues
        stripped = line.strip()
        
        # CRITICAL: Fix "code```" pattern (common LLM mistake)
        if 'code```' in stripped:
            logger.warning(f"Line {i+1}: Found 'code```' pattern, fixing to '```'")
            line = stripped.replace('code```', '```')
            stripped = line.strip()
        
        # CRITICAL: Fix "Example:```" or any "text```" pattern
        if re.search(r'\w```', stripped):
            logger.warning(f"Line {i+1}: Found text immediately before ```, fixing")
            line = re.sub(r'(\w)(```)', r'\1\n\2', line)
            stripped = line.strip()
        
        if stripped.startswith('``') and not stripped.startswith('```'):
            # Likely a malformed code fence like ``' or ``
            logger.warning(f"Line {i+1}: Found malformed code fence '{stripped}', fixing to '```'")
            line = line.replace(stripped, '```')
            stripped = '```'
        
        # Track code blocks (```)
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        
        # Don't modify code blocks or frontmatter - preserve them EXACTLY
        if in_code_block or in_frontmatter:
            result.append(line)
            continue

        # Only modify text OUTSIDE code blocks
        modified_line = line
        
        # Remove curly braces that are NOT in inline code (backticks)
        # Strategy: protect inline code, then remove braces, then restore inline code
        inline_code_parts = []
        def save_inline_code(match):
            inline_code_parts.append(match.group(0))
            return f"__INLINE_CODE_{len(inline_code_parts)-1}__"
        
        # Protect inline code
        modified_line = re.sub(r'`[^`]+`', save_inline_code, modified_line)
        
        # Now remove curly braces (both matched pairs AND orphaned ones)
        modified_line = re.sub(r"\{[^}]*\}", "", modified_line)
        modified_line = modified_line.replace('{', '').replace('}', '')
        
        # Restore inline code
        for idx, code in enumerate(inline_code_parts):
            modified_line = modified_line.replace(f"__INLINE_CODE_{idx}__", code)

        # Replace :param patterns with PARAM name (drop the colon) - OUTSIDE inline code
        inline_code_parts = []
        modified_line = re.sub(r'`[^`]+`', save_inline_code, modified_line)
        modified_line = re.sub(r':([a-zA-Z_][a-zA-Z0-9_]*)', r'\1', modified_line)
        for idx, code in enumerate(inline_code_parts):
            modified_line = modified_line.replace(f"__INLINE_CODE_{idx}__", code)

        # Replace <placeholder> patterns with PLACEHOLDER (MDX thinks these are HTML tags!)
        # But NOT in inline code or if it looks like a real HTML tag
        inline_code_parts = []
        modified_line = re.sub(r'`[^`]+`', save_inline_code, modified_line)
        # Only replace simple placeholders, not complex HTML-like tags
        modified_line = re.sub(r'<([a-zA-Z][a-zA-Z0-9_-]*)>', r'\1', modified_line)
        for idx, code in enumerate(inline_code_parts):
            modified_line = modified_line.replace(f"__INLINE_CODE_{idx}__", code)

        result.append(modified_line)
    
    # Check if we ended with an unclosed code block
    if in_code_block:
        logger.warning("Unclosed code block detected at end of file, adding closing fence")
        result.append('```')
    
    return '\n'.join(result)

def write_docs(site_dir: Path, files, pages: dict):
    # Get the first page info (this will be the homepage)
    first_page_name = list(pages.keys())[0]
    first_page_slug = slugify(first_page_name)
    
    for f in files:
        rel = f.get("path"); content = f.get("content","")
        if not rel or not isinstance(rel, str): continue
        out = site_dir / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        
        # CRITICAL: Escape unescaped curly braces for MDX (outside of code blocks)
        # This prevents React/MDX errors when using {id}, {param}, etc. in text
        content = fix_mdx_curly_braces(content)
        
        # CRITICAL: Add slug: / to the first page's frontmatter so it serves as homepage
        if rel == f"docs/{first_page_slug}.md":
            # Check if content has frontmatter
            if content.startswith("---"):
                lines = content.split("\n")
                # Find the end of frontmatter
                frontmatter_end = -1
                for i in range(1, len(lines)):
                    if lines[i].strip() == "---":
                        frontmatter_end = i
                        break
                
                if frontmatter_end > 0:
                    # Check if slug already exists
                    has_slug = any("slug:" in line for line in lines[1:frontmatter_end])
                    if not has_slug:
                        # Add slug: / to frontmatter
                        lines.insert(frontmatter_end, "slug: /")
                        content = "\n".join(lines)
                        logger.info(f"Added 'slug: /' to {rel} frontmatter")
        
        out.write_text(content, encoding="utf-8")
    
    # CRITICAL: Ensure ALL expected pages exist (create fallbacks for missing ones)
    for i, (page_name, page_desc) in enumerate(pages.items(), 1):
        page_slug = slugify(page_name)
        page_file = site_dir / "docs" / f"{page_slug}.md"
        
        if not page_file.exists():
            logger.warning(f"{page_slug}.md not found! Creating fallback page...")
            is_homepage = (i == 1)
            page_file.write_text(f"""---
id: {page_slug}
title: {page_name}
sidebar_position: {i}
{('slug: /' if is_homepage else '')}
---

# {page_name}

{page_desc}

This page is under construction and will be updated soon.
""", encoding="utf-8")
            logger.info(f"Created fallback page: {page_slug}.md")

def write_docker(site_dir: Path):
    (site_dir / "Dockerfile").write_text("""\
FROM node:18-alpine
WORKDIR /site

# Install dependencies first (better layer caching)
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* .npmrc* ./
RUN npm ci || npm i && npm i -g http-server

# Copy site source
COPY . .

# Ensure any previous caches are gone and build static site
RUN rm -rf .docusaurus node_modules/.cache || true \
 && npx docusaurus build

EXPOSE 3000
# Serve the static build with a simple static server (no config needed at runtime)
CMD ["http-server", "build", "-p", "3000", "-a", "0.0.0.0"]
""", encoding="utf-8")

    (site_dir / "docker-compose.yml").write_text("""\
services:
  web:
    build: .
    image: ${IMAGE_NAME}
    container_name: ${CONTAINER_NAME}
    restart: unless-stopped
    networks: [docs_net]
    ports:
      - "${PORT}:3000"

networks:
  docs_net:
    external: true
""", encoding="utf-8")

def docker_up(site_dir: Path, image: str, container: str, port: int):
    ensure_net(DOCKER_NETWORK)
    
    # Build with --no-cache to ensure completely fresh build (no cached layers)
    logger.info(f"Building fresh Docker image with --no-cache...")
    # Remove any local build caches before building
    for cache_dir in [site_dir / '.docusaurus', site_dir / 'node_modules' / '.cache']:
        if cache_dir.exists():
            try:
                shutil.rmtree(cache_dir)
                logger.info(f"Removed local cache directory: {cache_dir}")
            except Exception as cache_err:
                logger.warning(f"Failed to remove cache {cache_dir}: {cache_err}")
    subprocess.check_call([
        "docker", "build",
        "--no-cache",
        "-t", image,
        str(site_dir)
    ])
    
    # Start container with docker-compose
    logger.info(f"Starting container on port {port}...")
    env = os.environ.copy()
    env.update({
        "IMAGE_NAME": image,
        "CONTAINER_NAME": container,
        "PORT": str(port)
    })
    subprocess.check_call([
        "docker", "compose", 
        "-f", str(site_dir / "docker-compose.yml"),
        "up", "-d", "--force-recreate"
    ], cwd=site_dir, env=env)

@app.route("/generate-docs", methods=["POST"])
def generate_docs():
    try:
        logger.info("=== NEW REQUEST: /generate-docs ===")
        payload = request.get_json(force=True)
        logger.info(f"Received payload: {json.dumps(payload, indent=2)}")
        
        require_keys(payload, ["name","description","goal","dependencies","installation","pages","repo-name"])
        slug = slugify(payload["repo-name"])
        if not slug: raise ValueError("Invalid repo-name")
        fqdn = f"doc-{slug}.{BASE_DOMAIN}"
        logger.info(f"Generated slug: {slug}, FQDN: {fqdn}")

        # CRITICAL: If site exists, completely nuke it and its container first
        site_dir = SITES_ROOT / slug
        image = f"docusite:{slug}"
        container = f"docusite_{slug}"
        
        if site_dir.exists():
            logger.info(f"Existing site detected! Performing NUCLEAR cleanup...")
            # Stop and remove container
            logger.info(f"Stopping and removing container: {container}")
            subprocess.run(["docker", "stop", container], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["docker", "rm", "-f", container], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Remove image to force rebuild
            logger.info(f"Removing Docker image: {image}")
            subprocess.run(["docker", "rmi", "-f", image], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Prune build cache to remove all cached layers
            logger.info("Pruning Docker build cache...")
            subprocess.run(["docker", "builder", "prune", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Remove site directory
            logger.info(f"Removing site directory: {site_dir}")
            shutil.rmtree(site_dir)
            logger.info("Nuclear cleanup complete!")
        
        site_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created fresh site directory: {site_dir}")

        # 1) Get files from Ollama
        logger.info("Step 1: Calling Ollama to generate docs...")
        bundle = call_ollama(payload)
        logger.info(f"Ollama returned {len(bundle.get('files', []))} files")

        # 2) Minimal docusaurus scaffold
        logger.info("Step 2: Writing Docusaurus scaffold...")
        write_minimal_docusaurus(site_dir, site_title=payload["name"], site_base_url=fqdn, pages=payload["pages"])

        # 3) Write docs
        logger.info("Step 3: Writing generated docs...")
        write_docs(site_dir, bundle["files"], payload["pages"])

        # 4) Dockerize and run
        logger.info("Step 4: Creating Docker files and building...")
        write_docker(site_dir)
        port = ports.assign(slug)        # deterministic per slug
        logger.info(f"Assigned port: {port}")
        image = f"docusite:{slug}"
        container = f"docusite_{slug}"
        logger.info(f"Building and starting container: {container}")
        docker_up(site_dir, image, container, port)
        logger.info(f"Container started successfully on port {port}")

        # 5) Auto-configure NPM if enabled
        npm_result = None
        if NPM_ENABLED:
            logger.info("Step 5: Configuring NPM proxy...")
            try:
                token = npm_login()
                npm_result = npm_create_proxy(token, fqdn, DOCS_SERVER_IP, port)
                logger.info(f"NPM proxy created: {npm_result}")
            except Exception as npm_err:
                # Don't fail the whole request if NPM fails
                logger.error(f"NPM configuration failed: {npm_err}")
                npm_result = {"error": str(npm_err)}

        response = {
            "status":"ok",
            "slug": slug,
            "dir": str(site_dir),
            "port": port,
            "proxy_target": f"http://{DOCS_SERVER_IP}:{port}",
            "suggested_domain": fqdn,
            "url": f"https://{fqdn}" if NPM_ENABLED else f"http://{DOCS_SERVER_IP}:{port}"
        }
        
        if npm_result:
            response["npm"] = npm_result

        logger.info(f"SUCCESS! Site available at: {response['url']}")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"ERROR: {str(e)}", exc_info=True)
        return jsonify({"status":"error","error":str(e)}), 400

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def npm_login() -> str:
    """Login to NPM and get auth token"""
    r = requests.post(f"{NPM_HOST}/api/tokens", json={
        "identity": NPM_EMAIL,
        "secret": NPM_PASSWORD
    }, timeout=10)
    r.raise_for_status()
    return r.json()["token"]

def npm_create_proxy(token: str, domain: str, forward_ip: str, forward_port: int):
    """Create or update NPM proxy host with SSL"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Check if proxy already exists
    r = requests.get(f"{NPM_HOST}/api/nginx/proxy-hosts", headers=headers, timeout=10)
    r.raise_for_status()
    existing = [p for p in r.json() if domain in p.get("domain_names", [])]
    
    # Get SSL certificate (should be CloudFlare Siru.Dev wildcard)
    cert_id = 0
    try:
        certs_r = requests.get(f"{NPM_HOST}/api/nginx/certificates", headers=headers, timeout=10)
        certs_r.raise_for_status()
        # Look for CloudFlare cert or wildcard cert
        for cert in certs_r.json():
            cert_name = cert.get("nice_name", "").lower()
            cert_domains = cert.get("domain_names", [])
            # Match CloudFlare cert or wildcard
            if "cloudflare" in cert_name or "siru.dev" in cert_name or "*.siru.dev" in cert_domains:
                cert_id = cert["id"]
                logger.info(f"Using SSL cert: {cert.get('nice_name', 'Unknown')} (ID: {cert_id})")
                break
        
        if cert_id == 0:
            logger.warning("No SSL certificate found! Proxy will use HTTP only.")
    except Exception as e:
        logger.error(f"Could not fetch certificates: {e}")
    
    if existing:
        # Update existing - only send the exact fields NPM expects
        host_id = existing[0]["id"]
        existing_data = existing[0]
        
        # Build minimal update payload with only allowed fields
        payload = {
            "domain_names": existing_data.get("domain_names", [domain]),
            "forward_scheme": existing_data.get("forward_scheme", "http"),
            "forward_host": forward_ip,
            "forward_port": forward_port,
            "access_list_id": existing_data.get("access_list_id", 0),
            "certificate_id": cert_id,
            "ssl_forced": True if cert_id > 0 else False,
            "caching_enabled": existing_data.get("caching_enabled", False),
            "block_exploits": existing_data.get("block_exploits", True),
            "advanced_config": existing_data.get("advanced_config", ""),
            "meta": existing_data.get("meta", {}),
            "allow_websocket_upgrade": existing_data.get("allow_websocket_upgrade", True),
            "http2_support": existing_data.get("http2_support", True),
            "hsts_enabled": existing_data.get("hsts_enabled", False),
            "hsts_subdomains": existing_data.get("hsts_subdomains", False)
        }
        
        logger.info(f"Updating existing proxy host ID {host_id}: {forward_ip}:{forward_port}")
        r = requests.put(f"{NPM_HOST}/api/nginx/proxy-hosts/{host_id}", 
                        headers=headers, json=payload, timeout=10)
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"NPM update failed with status {r.status_code}")
            logger.error(f"Response: {r.text}")
            raise
    else:
        # Create new
        payload = {
            "domain_names": [domain],
            "forward_scheme": "http",
            "forward_host": forward_ip,
            "forward_port": forward_port,
            "access_list_id": 0,
            "certificate_id": cert_id,
            "ssl_forced": True if cert_id > 0 else False,
            "caching_enabled": False,
            "block_exploits": True,
            "advanced_config": "",
            "allow_websocket_upgrade": True,
            "http2_support": True,
            "hsts_enabled": False,
            "hsts_subdomains": False
        }
        
        logger.info(f"Creating new proxy host for {domain}")
        r = requests.post(f"{NPM_HOST}/api/nginx/proxy-hosts", 
                         headers=headers, json=payload, timeout=10)
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"NPM create failed with status {r.status_code}")
            logger.error(f"Response: {r.text}")
            raise
    
    return r.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT","8080")))

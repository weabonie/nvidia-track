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
    system_prompt = "You are a precise docs generator that outputs ONLY JSON per the required schema."
    user_prompt = f"""You are a docs generator for Docusaurus.

INPUT (repo spec):
<JSON>
{json.dumps(payload, indent=2)}
</JSON>

TASK:
- Produce Docusaurus-ready Markdown files from the spec.
- Every file must include front matter:
  ---
  title: ...
  sidebar_position: ...
  ---
- Target files to create if applicable:
  docs/intro.md
  docs/install.md
  docs/how-to-use.md
  docs/support.md
  docs/dependencies.md
  README.md

RULES:
- Output JSON ONLY with:
  {{
    "files": [{{"path":"docs/intro.md","content":"<md>"}}, ...]
  }}
- No extra keys. No commentary. No code fences.
- Use clear steps for Node/React; use lists and code blocks when helpful.
"""
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
    logger.debug(f"Raw Ollama response: {{content[:500]}}...")
    
    try:
        bundle = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Ollama JSON: {{e}}")
        logger.error(f"Content was: {{content[:1000]}}")
        raise RuntimeError(f"Ollama returned invalid JSON: {{e}}")
    
    if "files" not in bundle or not isinstance(bundle["files"], list):
        logger.error(f"Bundle structure: {{bundle}}")
        raise RuntimeError('Model JSON missing "files" array')
    
    # Validate file structure
    for i, f in enumerate(bundle["files"]):
        if isinstance(f, str):
            logger.error(f"File {{i}} is a string, not an object: {{f[:100]}}")
            raise RuntimeError(f"File {{i}} is malformed - expected object with 'path' and 'content'")
        if not isinstance(f, dict):
            raise RuntimeError(f"File {{i}} is not a dict: {{type(f)}}")
        if "path" not in f or "content" not in f:
            raise RuntimeError(f"File {{i}} missing required keys. Has: {{list(f.keys())}}")
    
    return bundle

def write_minimal_docusaurus(site_dir: Path, site_title: str, site_base_url: str):
    # Minimal classic preset scaffold
    (site_dir / "docs").mkdir(parents=True, exist_ok=True)
    (site_dir / "static").mkdir(parents=True, exist_ok=True)
    (site_dir / "src").mkdir(parents=True, exist_ok=True)

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
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        }
    }, indent=2), encoding="utf-8")

    (site_dir / "docusaurus.config.js").write_text(f"""\
/** @type {{import('@docusaurus/types').Config}} */
export default {{
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
      {{
        docs: {{
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
        }},
        blog: false,
        theme: {{}}
      }}
    ]
  ],
  themeConfig: {{
    navbar: {{
      title: '{site_title}',
      items: []
    }}
  }}
}};
""", encoding="utf-8")

    (site_dir / "sidebars.js").write_text("""\
/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
export default {
  tutorialSidebar: [{type: 'autogenerated', dirName: '.'}],
};
""", encoding="utf-8")

def write_docs(site_dir: Path, files):
    for f in files:
        rel = f.get("path"); content = f.get("content","")
        if not rel or not isinstance(rel, str): continue
        out = site_dir / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")

def write_docker(site_dir: Path):
    (site_dir / "Dockerfile").write_text("""\
# Build stage
FROM node:18-alpine AS build
WORKDIR /site
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* .npmrc* ./
RUN npm ci || npm i
COPY . .
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=build /site/build /usr/share/nginx/html
EXPOSE 80
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
      - "${PORT}:80"

networks:
  docs_net:
    external: true
""", encoding="utf-8")

def docker_up(site_dir: Path, image: str, container: str, port: int):
    # .env per service
    (site_dir / ".env").write_text(f"IMAGE_NAME={image}\nCONTAINER_NAME={container}\nPORT={port}\n", encoding="utf-8")
    ensure_net(DOCKER_NETWORK)
    subprocess.check_call(["docker", "compose", "-f", str(site_dir / "docker-compose.yml"), "up", "-d"], cwd=site_dir)

@app.route("/generate-docs", methods=["POST"])
def generate_docs():
    try:
        logger.info("=== NEW REQUEST: /generate-docs ===")
        payload = request.get_json(force=True)
        logger.info(f"Received payload: {json.dumps(payload, indent=2)}")
        
        require_keys(payload, ["name","description","goal","dependencies","installation","pages","repo-name"])
        slug = slugify(payload["repo-name"])
        if not slug: raise ValueError("Invalid repo-name")
        fqdn = f"{slug}-doc.{BASE_DOMAIN}"
        logger.info(f"Generated slug: {slug}, FQDN: {fqdn}")

        site_dir = SITES_ROOT / slug
        if site_dir.exists(): 
            logger.info(f"Removing existing site dir: {site_dir}")
            shutil.rmtree(site_dir)
        site_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created site directory: {site_dir}")

        # 1) Get files from Ollama
        logger.info("Step 1: Calling Ollama to generate docs...")
        bundle = call_ollama(payload)
        logger.info(f"Ollama returned {len(bundle.get('files', []))} files")

        # 2) Minimal docusaurus scaffold
        logger.info("Step 2: Writing Docusaurus scaffold...")
        write_minimal_docusaurus(site_dir, site_title=payload["name"], site_base_url=fqdn)

        # 3) Write docs
        logger.info("Step 3: Writing generated docs...")
        write_docs(site_dir, bundle["files"])

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
    """Create or update NPM proxy host"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Check if proxy already exists
    r = requests.get(f"{NPM_HOST}/api/nginx/proxy-hosts", headers=headers, timeout=10)
    r.raise_for_status()
    existing = [p for p in r.json() if domain in p.get("domain_names", [])]
    
    payload = {
        "domain_names": [domain],
        "forward_scheme": "http",
        "forward_host": forward_ip,
        "forward_port": forward_port,
        "access_list_id": 0,
        "certificate_id": 0,
        "ssl_forced": False,
        "caching_enabled": False,
        "block_exploits": True,
        "advanced_config": "",
        "meta": {"letsencrypt_agree": False, "dns_challenge": False},
        "allow_websocket_upgrade": True,
        "http2_support": True,
        "forward_host_header": True,
        "hsts_enabled": False,
        "hsts_subdomains": False
    }
    
    if existing:
        # Update existing
        host_id = existing[0]["id"]
        payload["id"] = host_id
        r = requests.put(f"{NPM_HOST}/api/nginx/proxy-hosts/{host_id}", 
                        headers=headers, json=payload, timeout=10)
    else:
        # Create new
        r = requests.post(f"{NPM_HOST}/api/nginx/proxy-hosts", 
                         headers=headers, json=payload, timeout=10)
    
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT","8080")))

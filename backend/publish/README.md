# Docusaurus Auto-Generator Backend

Flask API that generates Docusaurus documentation sites from JSON specs using Ollama, then builds and deploys each as a standalone Docker container.

## Setup

### 1. Prerequisites
```bash
# Install Ollama and pull model
ollama pull llama3.1

# Create directory for generated sites
sudo mkdir -p /srv/docs
sudo chown -R $USER:$USER /srv/docs

# Create Docker network (optional, will auto-create if not exists)
docker network create docs_net || true
```

### 2. Python Environment
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration
```bash
# Copy example env
cp .env.example .env

# Edit .env - REQUIRED values:
export OLLAMA_MODEL=llama3.1
export OLLAMA_URL=http://localhost:11434/api/chat
export SITES_ROOT=/srv/docs
export BASE_DOMAIN=siru.dev
export DOCKER_NETWORK=docs_net

# OPTIONAL: Auto-configure Nginx Proxy Manager
export NPM_ENABLED=true
export NPM_HOST=http://192.168.1.50:81        # Your NPM server
export NPM_EMAIL=admin@example.com            # NPM login email
export NPM_PASSWORD=changeme                  # NPM login password
export DOCS_SERVER_IP=192.168.1.100           # THIS server's IP (where containers run)
```

### 4. Run
```bash
python app.py
```

Server runs on `http://localhost:8080`

## Usage

### Generate Docs
```bash
curl -s http://localhost:8080/generate-docs \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Serialized Doe Class",
    "description":"My example repo",
    "goal":"Toy Project",
    "dependencies":["Node 17","React"],
    "installation":["install node","install react"],
    "pages":{"Intro":"more desc","Install":"more desc","How to use":"more desc","Support":"more desc"},
    "repo-name":"repo-name"
  }' | jq
```

### Response (NPM Disabled)
```json
{
  "status": "ok",
  "slug": "repo-name",
  "dir": "/srv/docs/repo-name",
  "port": 18123,
  "proxy_target": "http://192.168.1.100:18123",
  "suggested_domain": "repo-name-doc.siru.dev",
  "url": "http://192.168.1.100:18123"
}
```

### Response (NPM Enabled)
```json
{
  "status": "ok",
  "slug": "repo-name",
  "dir": "/srv/docs/repo-name",
  "port": 18123,
  "proxy_target": "http://192.168.1.100:18123",
  "suggested_domain": "repo-name-doc.siru.dev",
  "url": "https://repo-name-doc.siru.dev",
  "npm": {
    "id": 12,
    "created_on": "2025-11-09 12:34:56",
    "modified_on": "2025-11-09 12:34:56",
    "domain_names": ["repo-name-doc.siru.dev"]
  }
}
```

## Nginx Proxy Manager Setup

### Automatic (Recommended)

Set these environment variables and NPM proxy hosts will be created automatically:

```bash
export NPM_ENABLED=true
export NPM_HOST=http://192.168.1.50:81        # Your NPM server URL
export NPM_EMAIL=admin@example.com            # NPM admin email
export NPM_PASSWORD=changeme                  # NPM admin password
export DOCS_SERVER_IP=192.168.1.100           # This server's IP
```

**DNS**: Point `*.siru.dev` A record to your NPM server IP (not this server)

When you call `/generate-docs`, it will:
1. Generate the docs
2. Build and start the Docker container
3. Automatically create NPM proxy host
4. Return the live URL: `https://repo-name-doc.siru.dev`

### Manual (If NPM_ENABLED=false)

1. **DNS**: Point `*.siru.dev` A record to your NPM server IP
2. **NPM Proxy Host**:
   - Domain Names: `repo-name-doc.siru.dev`
   - Forward Hostname/IP: `<DOCS_SERVER_IP>` (where containers run)
   - Forward Port: `18123` (from API response)
   - Enable SSL with Let's Encrypt

## Generated Structure

Each repo gets:
```
/srv/docs/<slug>/
  ├── docs/                  # Ollama-generated docs
  ├── package.json
  ├── docusaurus.config.js
  ├── sidebars.js
  ├── Dockerfile            # Two-stage: build + nginx
  ├── docker-compose.yml
  └── .env                  # IMAGE_NAME, CONTAINER_NAME, PORT
```

## Re-generation

Calling `/generate-docs` again with the same `repo-name` will:
- Delete old site directory
- Rebuild with new content
- Reuse same port (deterministic from slug)
- Restart container

## Port Management

Ports are assigned deterministically per slug using `portmap.py`:
- Base: 18080
- Range: 2000 ports (18080-20079)
- Stored in `/srv/docs/.ports.json`

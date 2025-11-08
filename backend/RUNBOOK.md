# Documentation Generation System - Runbook

## Overview

This system generates comprehensive Docusaurus documentation from a JSON project specification using NVIDIA NIM with Nemotron (running locally). The pipeline includes planning, content generation, site building, and containerization.

## Prerequisites

### Required Software

- **Linux** with NVIDIA GPU (A100 80GB recommended)
- **NVIDIA Drivers** and GPU runtime installed
- **Docker** with GPU support
- **Node.js 20+** and npm
- **Python 3.9+**

### One-Time Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Deploy NVIDIA NIM locally:**
   - Follow NVIDIA's instructions to run NIM for Nemotron Instruct
   - Ensure it exposes an OpenAI-compatible endpoint at `http://localhost:8000/v1`
   - Verify with: `curl http://localhost:8000/v1/models`

3. **Verify prerequisites:**
   ```bash
   # Check Node.js
   node --version  # Should be 20+
   
   # Check Docker
   docker --version
   docker ps  # Should work without errors
   
   # Check GPU runtime
   docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
   ```

## Quick Start

### 1. Create Your Project Spec

Create a JSON file describing your project. See `spec_schema.py` for the schema and `EXAMPLE_SPEC` for a complete example.

Minimal example (`my-project-spec.json`):

```json
{
  "project_name": "My API Service",
  "description": "A REST API for managing users with authentication. Built for developers who need a scalable backend.",
  "tech_stack": ["Python 3.11", "FastAPI", "PostgreSQL"],
  "setup": {
    "tools": ["Python 3.11+", "Docker", "PostgreSQL 15+"]
  },
  "env_variables": [
    {
      "name": "DATABASE_URL",
      "purpose": "PostgreSQL connection string",
      "required": true
    }
  ],
  "apis": [
    {
      "name": "Get User",
      "path": "/api/v1/users/{id}",
      "method": "GET",
      "purpose": "Retrieve user by ID",
      "request_shape": {},
      "response_shape": {"id": "string", "name": "string"}
    }
  ],
  "modules": [],
  "deployment": [],
  "faq": []
}
```

### 2. Generate Documentation

Run the full pipeline:

```bash
python generate_docs.py my-project-spec.json \
  --site-dir ./my-docs \
  --nim-url http://localhost:8000/v1
```

This will:
- ✓ Check NIM health
- ✓ Plan documentation IA (6-12 pages across 2-4 sections)
- ✓ Scaffold Docusaurus site
- ✓ Generate all pages with Nemotron
- ✓ Generate sidebar
- ✓ Run quality checks
- ✓ Build static site

Output: `./my-docs/` with a complete Docusaurus site

### 3. Preview Locally

```bash
cd my-docs
npm run start
```

Visit `http://localhost:3000`

## CLI Reference

### Main Command

```bash
python generate_docs.py <spec-file> [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--site-dir DIR` | Target site directory (default: `./docs-site`) |
| `--nim-url URL` | NIM endpoint URL (default: `http://localhost:8000/v1`) |
| `--replan` | Regenerate IA plan (ignore cached plan) |
| `--regenerate` | Regenerate all pages (ignore existing content) |
| `--no-build` | Skip building static site |
| `--containerize` | Build Docker image |
| `--run` | Build and run Docker container (port 3000) |

### Common Workflows

**Initial generation:**
```bash
python generate_docs.py spec.json --site-dir ./docs
```

**Update existing docs (only generate missing pages):**
```bash
python generate_docs.py spec.json --site-dir ./docs
```

**Full regeneration:**
```bash
python generate_docs.py spec.json --site-dir ./docs --regenerate
```

**Rebuild with new plan:**
```bash
python generate_docs.py spec.json --site-dir ./docs --replan --regenerate
```

**Generate and containerize:**
```bash
python generate_docs.py spec.json --containerize
```

**Generate, containerize, and run:**
```bash
python generate_docs.py spec.json --run
```

## Rebuilding the Site

### Rebuild Static Site Only

```bash
cd my-docs
npm run build
```

Output: `./build/` directory

### Rebuild Docker Container

From the backend directory:

```bash
docker build -t my-docs:latest ./my-docs
```

### Run Container

```bash
docker run -d -p 3000:80 --name my-docs my-docs:latest
```

Access at: `http://localhost:3000`

### Using Docker Compose

Update `docker-compose.yml` context path, then:

```bash
docker-compose up -d
```

## Iteration Loop

When your project evolves:

1. **Update spec JSON** with new APIs, modules, env vars, etc.

2. **Decide scope:**
   - Minor changes (new API, FAQ): run without flags
   - Major changes (new modules/sections): use `--replan`
   - Content quality issues: use `--regenerate`

3. **Regenerate:**
   ```bash
   python generate_docs.py updated-spec.json --site-dir ./docs
   ```

4. **Review changes:**
   ```bash
   cd docs
   npm run start
   ```

5. **Run quality checks manually:**
   Quality gates run automatically, but you can also inspect:
   - Broken links in console output
   - H1/title mismatches
   - Missing pages in sidebar

6. **Rebuild and deploy:**
   ```bash
   python generate_docs.py updated-spec.json --site-dir ./docs --containerize
   ```

## Troubleshooting

### NIM Endpoint Not Reachable

**Symptom:** `✗ NIM endpoint is not reachable or has no models`

**Fix:**
- Verify NIM is running: `curl http://localhost:8000/v1/models`
- Check NIM logs for errors
- Ensure firewall allows localhost:8000
- Try `--nim-url http://127.0.0.1:8000/v1` instead

### No Nemotron Model Found

**Symptom:** `RuntimeError: No models available from NIM endpoint`

**Fix:**
- List available models: `curl http://localhost:8000/v1/models`
- Ensure at least one model is loaded in NIM
- Restart NIM with correct model configuration

### Docusaurus Build Fails

**Symptom:** Build command exits with errors

**Fix:**
- Check `node_modules/` exists: run `npm install` in site directory
- Check for broken Markdown syntax in generated pages
- Review build output for specific error (missing file, invalid link, etc.)
- Delete `.docusaurus/` and `build/` directories, then retry

### Docker Build Fails

**Symptom:** `docker build` command fails

**Fix:**
- Ensure Dockerfile is in site directory
- Check `package.json` exists
- Verify `npm run build` works standalone
- Check disk space: `df -h`

### Container Runs But Site Not Loading

**Symptom:** Container starts but `http://localhost:3000` doesn't load

**Fix:**
- Check container logs: `docker logs <container-name>`
- Verify port mapping: `docker ps` (should show `0.0.0.0:3000->80/tcp`)
- Check if port 3000 is already in use: `lsof -i :3000`
- Try different port: `docker run -p 8080:80 ...`

### Quality Checks Failing

**Symptom:** Quality gates report failures

**Fix:**
- **Broken links:** Check generated pages for incorrect relative paths
- **H1 mismatches:** Regenerate pages with `--regenerate`
- **Missing pages:** Check for errors in content generation step
- **Spec fidelity:** Update spec to match what's actually in your project

### Content Generation Hangs

**Symptom:** Pipeline stops during content generation

**Fix:**
- Check NIM is still responsive: test with `curl`
- Increase timeout in `nim_client.py` (default: 120s)
- Check GPU memory: `nvidia-smi`
- Try smaller spec (fewer pages) to isolate issue

### Sidebar Not Matching Plan

**Symptom:** Sidebar shows wrong pages or structure

**Fix:**
- Delete `sidebars.js` and regenerate
- Check that all page files exist in `docs/<Section>/<slug>.md`
- Verify `plan.json` has correct structure
- Use `--replan` to regenerate the entire plan

## Common Gotchas

### 🚫 DON'T: Invent new environment variable names

**Wrong:** Content mentions `API_SECRET_KEY` when spec has `SECRET_KEY`

**Fix:** Ensure spec has ALL env vars your project uses

### 🚫 DON'T: Change slugs or section names after planning

**Wrong:** Manually editing `sidebars.js` or renaming files

**Fix:** Update plan JSON and regenerate, or use `--replan`

### 🚫 DON'T: Place files at wrong directory depth

**Wrong:** `docs/guides/guides/setup.md` (nested sections)

**Fix:** Structure should be `docs/<Section>/<page>.md` (flat sections)

### 🚫 DON'T: Reference commands not in prerequisites

**Wrong:** Page mentions `kubectl` but spec doesn't list Kubernetes

**Fix:** Add to `setup.tools` in spec

### 🚫 DON'T: Forget to link homepage to key pages

**Wrong:** Homepage with no navigation links

**Fix:** System generates these automatically, but verify in output

### 🚫 DON'T: Bloat container with dev dependencies

**Wrong:** Dockerfile includes `node_modules/` in final stage

**Fix:** Use provided multi-stage Dockerfile (dev deps only in stage 1)

### 🚫 DON'T: Skip quality checks

**Wrong:** Deploying without reviewing quality gate output

**Fix:** Always review quality report, fix critical issues

## File Structure Reference

```
backend/
├── generate_docs.py          # Main CLI entrypoint
├── nim_client.py             # NIM API client
├── spec_schema.py            # Spec validation
├── ia_planner.py             # IA planning agent
├── content_generator.py      # Content generation
├── docusaurus_scaffolder.py  # Site scaffolding
├── sidebar_generator.py      # Sidebar config
├── quality_checker.py        # Quality gates
├── requirements.txt          # Python deps
├── Dockerfile                # Multi-stage build
├── docker-compose.yml        # Container orchestration
└── .dockerignore            # Docker ignore rules

docs-site/                    # Generated site (example)
├── docs/
│   ├── index.md             # Homepage
│   ├── Guides/
│   │   ├── setup.md
│   │   └── quickstart.md
│   ├── Reference/
│   │   ├── api.md
│   │   └── configuration.md
│   └── ...
├── docusaurus.config.js     # Site config
├── sidebars.js              # Sidebar config
├── package.json             # NPM config
└── build/                   # Static output (after build)
```

## Support

### Where to Look When Things Fail

1. **Spec issues:** Check console output for validation warnings
2. **NIM issues:** Check NIM logs and endpoint health
3. **Content issues:** Review quality gates report
4. **Build issues:** Check npm error output and Node.js version
5. **Container issues:** Check Docker logs and image layers

### Logs and Outputs

- **Pipeline logs:** Console output from `generate_docs.py`
- **Quality report:** Printed at end of pipeline
- **Plan file:** `<site-dir>_plan.json` (inspect IA)
- **Build logs:** `npm run build` output
- **Container logs:** `docker logs <container-name>`

## Next Steps

- Add OpenAPI integration for automatic API reference generation
- Implement changelog parsing from git tags
- Set up CI/CD pipeline for automated regeneration
- Add versioned docs support for breaking releases
- Integrate local doc search

---

**Questions?** Review the spec schema in `spec_schema.py` for all available options.

**Pro tip:** Start with a small spec (3-4 sections, 6-8 pages) to validate the pipeline, then expand.

# Documentation Generator with NVIDIA NIM + Nemotron

Complete end-to-end documentation generation system that uses **NVIDIA NIM** (running locally) with **Nemotron** to automatically create production-ready Docusaurus documentation from a JSON project specification.

## 🎯 What This Does

**Input:** A single JSON file describing your project (APIs, modules, setup, FAQs, etc.)

**Process:** Agent uses Nemotron (via local NIM) to:
1. Plan documentation information architecture
2. Generate comprehensive pages with proper structure
3. Scaffold and build a Docusaurus site
4. Package everything in a Docker container

**Output:** A working Docusaurus site + Docker image ready to deploy

## 🚀 Quick Start

### Prerequisites

- Linux with NVIDIA A100 80GB (or similar GPU)
- NVIDIA NIM running locally with Nemotron model
- Docker with GPU support
- Node.js 20+
- Python 3.9+

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start NVIDIA NIM

Follow NVIDIA's instructions to deploy NIM locally with Nemotron. Ensure it's running at `http://localhost:8000/v1`.

Verify:
```bash
curl http://localhost:8000/v1/models
```

### 3. Create Your Project Spec

See `example-spec.json` for a complete example. Minimal version:

```json
{
  "project_name": "My Project",
  "description": "What it does and who it's for (2-4 sentences).",
  "tech_stack": ["Python 3.11", "FastAPI"],
  "setup": {
    "tools": ["Python 3.11+", "Docker"]
  },
  "env_variables": [],
  "apis": [],
  "modules": [],
  "deployment": [],
  "faq": []
}
```

### 4. Generate Documentation

```bash
python generate_docs.py my-spec.json --site-dir ./my-docs
```

This runs the full pipeline:
- ✓ Validates spec
- ✓ Plans IA (6-12 pages, 2-4 sections)
- ✓ Scaffolds Docusaurus site
- ✓ Generates all content with Nemotron
- ✓ Builds static site
- ✓ Runs quality checks

### 5. Preview

```bash
cd my-docs
npm run start
```

Visit `http://localhost:3000`

### 6. Containerize (Optional)

```bash
python generate_docs.py my-spec.json --containerize --run
```

Site will be available at `http://localhost:3000`

## 📋 CLI Reference

```bash
python generate_docs.py <spec-file> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--site-dir DIR` | Output directory (default: `./docs-site`) |
| `--nim-url URL` | NIM endpoint (default: `http://localhost:8000/v1`) |
| `--replan` | Regenerate documentation plan |
| `--regenerate` | Regenerate all content |
| `--no-build` | Skip static build |
| `--containerize` | Build Docker image |
| `--run` | Build and run container |

### Examples

**First generation:**
```bash
python generate_docs.py spec.json
```

**Update after spec changes:**
```bash
python generate_docs.py spec.json  # Only generates missing pages
```

**Full regeneration:**
```bash
python generate_docs.py spec.json --regenerate
```

**New plan + full regen:**
```bash
python generate_docs.py spec.json --replan --regenerate
```

**Generate and deploy:**
```bash
python generate_docs.py spec.json --containerize --run
```

## 📁 Project Structure

```
backend/
├── generate_docs.py          # Main CLI entrypoint
├── nim_client.py             # NVIDIA NIM API client
├── spec_schema.py            # Spec validation (Pydantic models)
├── ia_planner.py             # IA planning agent
├── content_generator.py      # Content generation with Nemotron
├── docusaurus_scaffolder.py  # Docusaurus site setup
├── sidebar_generator.py      # Sidebar configuration
├── quality_checker.py        # Quality gates
├── requirements.txt          # Python dependencies
├── Dockerfile                # Multi-stage container build
├── docker-compose.yml        # Container orchestration
├── .dockerignore            # Docker ignore rules
├── example-spec.json         # Example project spec
├── RUNBOOK.md               # Detailed operations guide
└── README.md                # This file
```

## 🔧 Spec Format

See `spec_schema.py` for the complete schema. Key sections:

```json
{
  "project_name": "string (required)",
  "description": "string (required, 2-4 sentences)",
  "repo_url": "string (optional)",
  "tech_stack": ["list of technologies"],
  "setup": {
    "os_constraints": ["OS requirements"],
    "tools": ["Required tools with versions"],
    "hardware": ["Hardware requirements"]
  },
  "env_variables": [
    {
      "name": "VAR_NAME",
      "purpose": "What it does",
      "required": true,
      "default": "optional default"
    }
  ],
  "apis": [
    {
      "name": "Endpoint Name",
      "path": "/api/v1/resource",
      "method": "GET",
      "purpose": "What it does",
      "request_shape": {},
      "response_shape": {},
      "auth_required": true
    }
  ],
  "modules": [
    {
      "name": "Module Name",
      "path": "src/module/",
      "summary": "2-3 sentences",
      "dependencies": ["Other Module"]
    }
  ],
  "deployment": [
    {
      "platform": "Docker",
      "description": "How deployment works",
      "config_files": ["Dockerfile"]
    }
  ],
  "faq": [
    {
      "question": "Common question?",
      "answer": "Solution or explanation",
      "category": "Troubleshooting"
    }
  ],
  "extras": {
    "openapi_spec": "path/to/spec.yaml"
  }
}
```

## 📖 Generated Documentation Structure

The system generates:

1. **Homepage** (`docs/index.md`)
   - Project overview
   - Quick start steps
   - Links to key pages

2. **Section Pages** (e.g., `docs/Guides/setup.md`)
   - H1 title
   - Introduction paragraph
   - Prerequisites
   - Step-by-step procedures
   - Configuration details
   - Verification steps
   - Troubleshooting

3. **Navigation** (`sidebars.js`)
   - Organized by sections
   - Categories for logical grouping

## 🎨 Content Quality

Every generated page includes:

- ✓ Clear H1 matching planned title
- ✓ Practical, copy-paste friendly code examples
- ✓ Step-by-step procedures in chronological order
- ✓ Configuration tables with explanations
- ✓ Verification steps
- ✓ Troubleshooting section
- ✓ Cross-links to related pages

Quality gates check for:

- ✓ IA sanity (section count, page distribution)
- ✓ H1/title consistency
- ✓ Spec fidelity (no hallucinated names)
- ✓ Broken internal links
- ✓ Page structure completeness
- ✓ Duplicate content

## 🔄 Iteration Workflow

When your project evolves:

1. **Update** `spec.json` with changes
2. **Regenerate** (only missing pages created by default)
   ```bash
   python generate_docs.py spec.json
   ```
3. **Review** quality report output
4. **Preview** changes locally
5. **Rebuild** container if needed

For major changes:
```bash
python generate_docs.py spec.json --replan --regenerate
```

## 🐳 Docker Deployment

### Build Image

```bash
# Via CLI
python generate_docs.py spec.json --containerize

# Or manually
cd docs-site
docker build -t my-docs:latest .
```

### Run Container

```bash
docker run -d -p 3000:80 my-docs:latest
```

### Docker Compose

Update `docker-compose.yml` context path:

```yaml
services:
  docs:
    build:
      context: ./docs-site
    ports:
      - "3000:80"
```

Then:
```bash
docker-compose up -d
```

## 📚 Documentation

- **[RUNBOOK.md](RUNBOOK.md)** - Complete operational guide
  - Prerequisites and setup
  - CLI reference
  - Troubleshooting
  - Common gotchas
  - File structure reference

- **[spec_schema.py](spec_schema.py)** - Spec format and validation
  - Pydantic models
  - Validation rules
  - Example spec

## 🔍 Troubleshooting

### NIM not reachable

```bash
# Check NIM is running
curl http://localhost:8000/v1/models

# Check for models
curl http://localhost:8000/v1/models | jq '.data[].id'
```

### Build fails

```bash
# Clear cache
cd docs-site
rm -rf node_modules .docusaurus build
npm install
npm run build
```

### Quality checks fail

Review the quality report output and:
- Check for broken links
- Verify H1 titles match planned titles
- Ensure all pages exist

See [RUNBOOK.md](RUNBOOK.md) for comprehensive troubleshooting.

## ⚠️ Common Gotchas

1. **Don't** invent env var names - use exact names from spec
2. **Don't** change slugs after planning - regenerate plan instead
3. **Don't** place files at wrong depth - use `docs/<Section>/<page>.md`
4. **Don't** reference tools not in prerequisites
5. **Don't** skip quality checks before deploying

## 🎯 Future Enhancements

Potential additions:

- [ ] OpenAPI ingestion for automatic API reference
- [ ] Changelog parsing from git tags
- [ ] Code sample sync from repo
- [ ] Doc search integration
- [ ] CI/CD pipeline templates
- [ ] Versioned docs support

## 📝 License

This is an internal tool. Adjust licensing as needed for your organization.

## 🤝 Contributing

1. Update spec schema if adding new fields
2. Add validation in `ProjectSpec.validate_spec()`
3. Update example spec
4. Document in RUNBOOK.md

## 💡 Tips

- Start small (6-8 pages) to validate pipeline
- Use `--regenerate` sparingly (wastes LLM calls)
- Review quality gates before production
- Keep spec version controlled
- Generate example spec from template: see `spec_schema.EXAMPLE_SPEC`

---

**Ready to generate docs?**

```bash
python generate_docs.py example-spec.json --site-dir ./demo-docs
```

# Documentation Generator - System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: Project Spec (JSON)                   │
│                                                                 │
│  {                                                              │
│    "project_name": "My API",                                    │
│    "description": "...",                                        │
│    "tech_stack": [...],                                         │
│    "apis": [...],                                               │
│    "modules": [...],                                            │
│    ...                                                          │
│  }                                                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 1: Validate Spec (spec_schema.py)             │
│                                                                 │
│  ✓ Check required fields                                       │
│  ✓ Validate data types                                         │
│  ✓ Run sanity checks                                           │
│  ✓ Report warnings                                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│            STEP 2: Plan IA (ia_planner.py + NIM)                │
│                                                                 │
│  ┌──────────────┐       ┌───────────────────────────┐          │
│  │ Spec Context │  ───▶ │  NVIDIA NIM (Nemotron)    │          │
│  └──────────────┘       │  http://localhost:8000/v1 │          │
│                         └───────────┬───────────────┘          │
│                                     │                           │
│                                     ▼                           │
│                         ┌─────────────────────┐                │
│                         │ Documentation Plan  │                │
│                         │ - 2-4 Sections      │                │
│                         │ - 6-12 Pages        │                │
│                         │ - Slugs & Scope     │                │
│                         └─────────────────────┘                │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│       STEP 3: Scaffold Site (docusaurus_scaffolder.py)         │
│                                                                 │
│  ┌────────────────────────────────────────┐                    │
│  │  npx create-docusaurus classic         │                    │
│  │  ├── Configure docs-only mode          │                    │
│  │  ├── Set project name                  │                    │
│  │  ├── Create section directories        │                    │
│  │  └── Clear default content             │                    │
│  └────────────────────────────────────────┘                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│        STEP 4: Generate Content (content_generator.py + NIM)   │
│                                                                 │
│  For each page in plan:                                        │
│  ┌──────────────────┐     ┌─────────────────────┐             │
│  │ Page Plan +      │ ──▶ │ NVIDIA NIM          │             │
│  │ Spec Context     │     │ (Nemotron)          │             │
│  └──────────────────┘     └──────────┬──────────┘             │
│                                       │                         │
│                                       ▼                         │
│                           ┌───────────────────────┐            │
│                           │ Markdown Page:        │            │
│                           │ - H1 Title            │            │
│                           │ - Introduction        │            │
│                           │ - Prerequisites       │            │
│                           │ - Steps               │            │
│                           │ - Configuration       │            │
│                           │ - Verification        │            │
│                           │ - Troubleshooting     │            │
│                           └───────────────────────┘            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│         STEP 5: Generate Sidebar (sidebar_generator.py)        │
│                                                                 │
│  Plan ──▶ sidebars.js                                          │
│           {                                                     │
│             tutorialSidebar: [                                  │
│               { type: "doc", id: "index" },                     │
│               {                                                 │
│                 type: "category",                               │
│                 label: "Guides",                                │
│                 items: [...]                                    │
│               }                                                 │
│             ]                                                   │
│           }                                                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│          STEP 6: Quality Checks (quality_checker.py)           │
│                                                                 │
│  ✓ IA Sanity          - Section/page count reasonable          │
│  ✓ H1/Title Match     - Titles match plan exactly              │
│  ✓ Spec Fidelity      - No hallucinated names                  │
│  ✓ Dead Links         - All internal links valid               │
│  ✓ Page Structure     - Required sections present              │
│  ✓ Uniqueness         - No duplicate slugs/titles              │
│                                                                 │
│  Report: X/6 gates passed                                      │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│         STEP 7: Build Site (docusaurus_scaffolder.py)          │
│                                                                 │
│  npm install                                                    │
│  npm run build                                                  │
│                                                                 │
│  ──▶  build/ directory (static HTML/CSS/JS)                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│        STEP 8: Containerize (Dockerfile - optional)            │
│                                                                 │
│  ┌──────────────────────────────────────┐                      │
│  │ STAGE 1: Build                       │                      │
│  │  FROM node:20-alpine                 │                      │
│  │  COPY package*.json ./               │                      │
│  │  RUN npm ci                          │                      │
│  │  COPY . .                            │                      │
│  │  RUN npm run build                   │                      │
│  └──────────────────────────────────────┘                      │
│                    │                                            │
│                    ▼                                            │
│  ┌──────────────────────────────────────┐                      │
│  │ STAGE 2: Serve                       │                      │
│  │  FROM nginx:alpine                   │                      │
│  │  COPY --from=builder build/ /html/   │                      │
│  │  EXPOSE 80                           │                      │
│  │  CMD ["nginx"]                       │                      │
│  └──────────────────────────────────────┘                      │
│                    │                                            │
│                    ▼                                            │
│          Docker Image: my-docs:latest                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                   OUTPUT: Docusaurus Site                      │
│                                                                 │
│  docs-site/                                                     │
│  ├── docs/                                                      │
│  │   ├── index.md                                              │
│  │   ├── Guides/                                               │
│  │   │   ├── setup.md                                          │
│  │   │   └── quickstart.md                                     │
│  │   ├── Reference/                                            │
│  │   │   ├── api.md                                            │
│  │   │   └── configuration.md                                  │
│  │   └── Troubleshooting/                                      │
│  │       └── common-issues.md                                  │
│  ├── docusaurus.config.js                                      │
│  ├── sidebars.js                                               │
│  ├── package.json                                              │
│  └── build/  ◀── Static site ready to deploy                   │
│                                                                 │
│  + Docker image (if --containerize)                            │
│  + Running container at localhost:3000 (if --run)              │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Core Modules

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `nim_client.py` | NIM API wrapper | `list_models()`, `chat_completion()`, `check_health()` |
| `spec_schema.py` | Spec validation | `ProjectSpec.from_json_file()`, `validate_spec()` |
| `ia_planner.py` | IA planning | `plan_documentation()` |
| `content_generator.py` | Content gen | `generate_homepage()`, `generate_page()` |
| `docusaurus_scaffolder.py` | Site setup | `scaffold_site()`, `build_site()` |
| `sidebar_generator.py` | Navigation | `generate_sidebar()` |
| `quality_checker.py` | Validation | `run_all_checks()` |
| `generate_docs.py` | Orchestration | `run_full_pipeline()` |

### Data Flow

```
Spec JSON
   │
   ├─▶ spec_schema.py ──▶ ProjectSpec object
   │
   ├─▶ ia_planner.py ──▶ DocumentationPlan object
   │                      (saved as JSON)
   │
   ├─▶ content_generator.py ──▶ Markdown files
   │                             (docs/*.md)
   │
   ├─▶ sidebar_generator.py ──▶ sidebars.js
   │
   ├─▶ quality_checker.py ──▶ Quality report
   │
   └─▶ docusaurus_scaffolder.py ──▶ Static build
                                     (build/)
```

## CLI Parameter Flow

```
python generate_docs.py spec.json [options]
                          │
                          ├─▶ --site-dir        → DocsOrchestrator.site_dir
                          ├─▶ --nim-url         → NIMClient(base_url)
                          ├─▶ --replan          → plan_documentation(reuse_plan=False)
                          ├─▶ --regenerate      → generate_content(regenerate_all=True)
                          ├─▶ --no-build        → skip build_site()
                          ├─▶ --containerize    → build_container()
                          └─▶ --run             → run_container()
```

## State Management

```
File System State:
  
  <site-dir>/                  # Docusaurus site
  <site-dir>_plan.json         # Cached IA plan
  
Stateless Operations (safe to rerun):
  - Spec validation
  - IA planning (if --replan)
  - Content generation (if --regenerate)
  - Sidebar generation
  - Quality checks
  - Site build
  
Idempotent Operations (check before creating):
  - Scaffold site (reuses if exists)
  - Generate content (skips existing pages unless --regenerate)
  - Plan (reuses cached unless --replan)
```

## External Dependencies

```
┌─────────────────┐
│  NVIDIA NIM     │  ← Must be running locally
│  (Nemotron)     │     Port: 8000
│  localhost:8000 │     Protocol: OpenAI-compatible REST
└─────────────────┘

┌─────────────────┐
│  Node.js 20+    │  ← For Docusaurus
│  npm            │     Build & dev server
└─────────────────┘

┌─────────────────┐
│  Docker         │  ← For containerization
│  (optional)     │     Multi-stage builds
└─────────────────┘
```

## Error Handling Strategy

```
Layer 1: Input Validation
  ├─▶ Spec file exists?
  ├─▶ Valid JSON?
  ├─▶ Pydantic validation passes?
  └─▶ Sanity checks pass?
  
Layer 2: Runtime Checks
  ├─▶ NIM endpoint reachable?
  ├─▶ Nemotron model available?
  ├─▶ Node.js installed?
  └─▶ Sufficient disk space?
  
Layer 3: Generation Validation
  ├─▶ Pages generated successfully?
  ├─▶ Markdown valid?
  ├─▶ Links not broken?
  └─▶ Quality gates pass?
  
Layer 4: Build Validation
  ├─▶ npm install succeeds?
  ├─▶ npm build succeeds?
  ├─▶ Build directory created?
  └─▶ Container builds (if requested)?
```

## Performance Characteristics

```
Typical Pipeline Timing (8-page docs):

Spec Validation:     < 1s
IA Planning:         5-15s   (1 LLM call)
Site Scaffold:       10-20s  (npm operations)
Content Generation:  60-120s (8-10 LLM calls)
Sidebar Generation:  < 1s
Quality Checks:      1-3s
Site Build:          20-40s  (npm build)
Container Build:     30-60s  (if requested)
───────────────────────────────
Total:               ~2-4 min

Bottlenecks:
- LLM inference (content generation)
- npm operations (install, build)

Optimizations:
- Reuse plan (--replan only when needed)
- Skip regeneration (only new pages)
- Parallel LLM calls (not implemented)
```

---

**Ready to generate?**

```bash
./quickstart.sh
python generate_docs.py example-spec.json
```

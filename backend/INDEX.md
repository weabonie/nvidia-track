# Documentation Generator - File Index

## Quick Navigation

| What You Need | Go To |
|---------------|-------|
| 🚀 **Get Started** | [quickstart.sh](quickstart.sh) or [README.md](README.md) |
| 📖 **Usage Guide** | [README.md](README.md) |
| 🔧 **Operations** | [RUNBOOK.md](RUNBOOK.md) |
| 🏗️ **Architecture** | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 📋 **Project Overview** | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| 📝 **Example Spec** | [example-spec.json](example-spec.json) |

---

## All Files (20 total)

### 🎯 Entry Points

| File | Purpose | Usage |
|------|---------|-------|
| **generate_docs.py** | Main CLI orchestrator | `python generate_docs.py spec.json [options]` |
| **quickstart.sh** | Setup & prerequisites check | `./quickstart.sh` |
| **validate_spec.py** | Validate spec files | `python validate_spec.py spec.json -v` |

### 🧩 Core Modules (Python)

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| **nim_client.py** | NVIDIA NIM API client | `NIMClient`, `chat_completion()` |
| **spec_schema.py** | Spec schema & validation | `ProjectSpec`, `validate_spec()` |
| **ia_planner.py** | IA planning agent | `IAPlanner`, `DocumentationPlan` |
| **content_generator.py** | Content generation | `ContentGenerator`, `generate_page()` |
| **docusaurus_scaffolder.py** | Site scaffolding | `DocusaurusScaffolder`, `build_site()` |
| **sidebar_generator.py** | Sidebar config | `SidebarGenerator` |
| **quality_checker.py** | Quality gates | `QualityChecker`, `run_all_checks()` |

### 🐳 Docker & Deployment

| File | Purpose | Usage |
|------|---------|-------|
| **Dockerfile** | Multi-stage container build | `docker build -t my-docs .` |
| **docker-compose.yml** | Container orchestration | `docker-compose up` |
| **.dockerignore** | Docker build optimization | (automatic) |

### 📚 Documentation

| File | Purpose | Audience |
|------|---------|----------|
| **README.md** | Main documentation & quick start | All users |
| **RUNBOOK.md** | Comprehensive operations guide | Operators |
| **ARCHITECTURE.md** | System architecture & flow | Developers |
| **PROJECT_SUMMARY.md** | Project overview & summary | Stakeholders |
| **INDEX.md** | This file - navigation hub | All users |

### 📦 Configuration

| File | Purpose |
|------|---------|
| **requirements.txt** | Python dependencies |
| **example-spec.json** | Example project specification |
| **.gitignore** | Git ignore rules |

---

## File Dependency Graph

```
generate_docs.py (main orchestrator)
  │
  ├─▶ nim_client.py
  ├─▶ spec_schema.py
  ├─▶ ia_planner.py ──▶ nim_client.py
  ├─▶ content_generator.py ──▶ nim_client.py
  ├─▶ docusaurus_scaffolder.py
  ├─▶ sidebar_generator.py
  └─▶ quality_checker.py

validate_spec.py
  └─▶ spec_schema.py

quickstart.sh
  (standalone)
```

## Documentation Hierarchy

```
START HERE
  │
  ├─▶ New User? ──▶ README.md ──▶ quickstart.sh
  │
  ├─▶ Need Details? ──▶ RUNBOOK.md
  │                      │
  │                      ├─▶ Prerequisites
  │                      ├─▶ Troubleshooting
  │                      └─▶ Common Gotchas
  │
  ├─▶ Understanding System? ──▶ ARCHITECTURE.md
  │                              │
  │                              ├─▶ Component Flow
  │                              ├─▶ Data Flow
  │                              └─▶ Error Handling
  │
  └─▶ Quick Overview? ──▶ PROJECT_SUMMARY.md
                           │
                           ├─▶ What Was Built
                           ├─▶ How It Works
                           └─▶ Key Features
```

## Lines of Code Summary

| Category | Files | Approx. Lines |
|----------|-------|---------------|
| Python Code | 8 files | ~2,500 lines |
| Documentation | 5 files | ~1,500 lines |
| Config/Docker | 4 files | ~100 lines |
| Scripts | 2 files | ~150 lines |
| Example Data | 1 file | ~150 lines |
| **TOTAL** | **20 files** | **~4,400 lines** |

## Usage Patterns

### First Time User
```bash
1. Read: README.md (10 min)
2. Run: ./quickstart.sh
3. Validate: python validate_spec.py example-spec.json -v
4. Generate: python generate_docs.py example-spec.json
5. Preview: cd docs-site && npm run start
```

### Regular User (Update Docs)
```bash
1. Update: my-spec.json
2. Validate: python validate_spec.py my-spec.json
3. Generate: python generate_docs.py my-spec.json --site-dir ./my-docs
4. Review: quality report output
5. Deploy: python generate_docs.py my-spec.json --containerize
```

### Developer/Contributor
```bash
1. Read: ARCHITECTURE.md
2. Understand: PROJECT_SUMMARY.md
3. Reference: RUNBOOK.md (troubleshooting)
4. Modify: Core modules (*.py)
5. Test: validate_spec.py + generate_docs.py
```

### Operator/DevOps
```bash
1. Read: RUNBOOK.md (focus on Prerequisites & Troubleshooting)
2. Setup: ./quickstart.sh
3. Deploy: Use Dockerfile or docker-compose.yml
4. Monitor: Check quality gates output
5. Debug: Refer to RUNBOOK.md troubleshooting section
```

## Key Concepts

| Concept | Where to Learn More |
|---------|---------------------|
| Project Spec Format | spec_schema.py, example-spec.json |
| IA Planning | ARCHITECTURE.md, ia_planner.py |
| Content Generation | content_generator.py |
| Quality Gates | quality_checker.py, RUNBOOK.md |
| Containerization | Dockerfile, docker-compose.yml, RUNBOOK.md |

## File Sizes (Approximate)

```
Documentation:
  README.md           ~500 lines
  RUNBOOK.md          ~450 lines
  ARCHITECTURE.md     ~350 lines
  PROJECT_SUMMARY.md  ~300 lines
  INDEX.md            ~250 lines

Python Modules:
  generate_docs.py          ~400 lines
  content_generator.py      ~350 lines
  quality_checker.py        ~300 lines
  ia_planner.py             ~280 lines
  spec_schema.py            ~280 lines
  docusaurus_scaffolder.py  ~250 lines
  sidebar_generator.py      ~180 lines
  nim_client.py             ~150 lines
  validate_spec.py          ~80 lines

Config/Scripts:
  example-spec.json   ~150 lines
  quickstart.sh       ~80 lines
  Dockerfile          ~30 lines
  docker-compose.yml  ~20 lines
  requirements.txt    ~5 lines
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-08 | Initial complete implementation |

## Contact & Support

For issues, see:
- **Common problems:** RUNBOOK.md → Troubleshooting
- **How-to questions:** README.md
- **Architecture questions:** ARCHITECTURE.md

---

**🚀 Ready to start?**

```bash
./quickstart.sh
```

**📖 Need help?**

```bash
python generate_docs.py --help
```

**✅ Validate your spec:**

```bash
python validate_spec.py your-spec.json -v
```

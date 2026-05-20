# 🚀 SAIS Phase 1: Core Kernel - Implementation Guide

**Status:** Phase 1 Complete - Ready for Testing  
**Version:** 1.0.0  
**Last Updated:** April 3, 2026  

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Installation & Setup](#installation--setup)
4. [Component Descriptions](#component-descriptions)
5. [Running SAIS](#running-sais)
6. [API Reference](#api-reference)
7. [Development Roadmap](#development-roadmap)
8. [Platform Deployment](#platform-deployment)

---

## Overview

**SAIS** (Sovereign Adaptive Intelligence System) is a personal AI operating system designed to:

✅ Run **locally-first** with zero cloud dependency  
✅ **Learn new capabilities** on demand  
✅ **Persistently improve** under user control  
✅ Operate with **Jarvis/Friday/Edith-class** intelligence  
✅ Support **AIMO 2026** competition-level reasoning  

### Phase 1 Deliverables

This is **Phase 1: Core Kernel**—the foundation of everything.

**What's included:**
- ✅ **Orchestrator**: Central decision engine
- ✅ **Personality Manager**: 5 distinct personas (Jarvis, Friday, Edith, TARS, Cortana)
- ✅ **Capability Manager**: Store and retrieve learned skills
- ✅ **Memory System**: Short-term + long-term persistent storage
- ✅ **Logging & Monitoring**: Full execution tracking

**Not yet included:**
- ❌ LLM integration (Phase 4)
- ❌ Advanced UI (Phase 4)
- ❌ Tool execution (Phase 3)
- ❌ Evolution engine (Phase 2)
- ❌ Vector embeddings (Phase 5)

---

## Project Structure

```
sais/
├── README.md                          # This file
├── SAIS_Master_Specification.md       # Complete BRD + LLD + Omega Architecture
│
├── phase1_orchestrator.py             # Core decision engine
├── phase1_personality_manager.py      # Persona system
├── phase1_capability_manager.py       # Capability repository
├── phase1_memory.py                   # Memory system
├── phase1_sais_kernel.py              # Main integration
│
├── tests/
│   ├── test_orchestrator.py
│   ├── test_personality.py
│   ├── test_capabilities.py
│   ├── test_memory.py
│   └── test_integration.py
│
├── data/
│   ├── memory/                        # Persistent memory storage
│   │   └── index.json
│   ├── capabilities/                  # Capability repository
│   │   └── index.json
│   └── logs/                          # Execution logs
│
├── ui/
│   ├── web/
│   │   ├── index.html                 # Web interface (Phase 4)
│   │   ├── app.js
│   │   └── style.css
│   ├── mobile/
│   │   └── app.tsx                    # Mobile app (Phase 4)
│   └── desktop/
│       └── main.py                    # Desktop app (Phase 4)
│
├── backends/
│   ├── python/                        # Python FastAPI backend
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── javascript/                    # JavaScript/Node.js backend
│   │   ├── index.js
│   │   └── package.json
│   └── webgpu/                        # Browser-based (Phase 4)
│       └── kernel.js
│
└── docs/
    ├── API.md
    ├── ARCHITECTURE.md
    ├── DEVELOPMENT.md
    └── DEPLOYMENT.md
```

---

## Installation & Setup

### Prerequisites

- Python 3.9+
- Optional: Node.js 16+ (for JavaScript ports)
- Optional: Docker (for containerization)

### Step 1: Clone & Setup

```bash
# Clone repository
git clone <repo-url> sais
cd sais

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (Phase 1 has minimal deps)
pip install -r requirements.txt
```

### Step 2: Quick Test

```bash
# Run the Phase 1 kernel
python3 phase1_sais_kernel.py

# Or test individual components
python3 phase1_orchestrator.py          # Test orchestrator
python3 phase1_memory.py                # Test memory
python3 phase1_capability_manager.py    # Test capabilities
python3 phase1_personality_manager.py   # Test personas
```

### Step 3: Verify Installation

```bash
# Check all components import correctly
python3 -c "
from phase1_orchestrator import Orchestrator
from phase1_memory import MemorySystem
from phase1_capability_manager import CapabilityManager
from phase1_personality_manager import PersonalityManager
from phase1_sais_kernel import SAISKernel
print('✓ All components loaded successfully')
"
```

---

## Component Descriptions

### 1. **Orchestrator** (`phase1_orchestrator.py`)

The **central decision engine** of SAIS.

**Responsibilities:**
- Parse user intent from natural language
- Generate execution plans
- Route to appropriate executors
- Reflect on results for learning

**Key Classes:**
- `Orchestrator`: Main orchestrator
- `Intent`: Parsed user intent
- `Plan`: Execution plan
- `ExecutionResult`: Result of execution

**Usage:**
```python
from phase1_orchestrator import Orchestrator

orch = Orchestrator()
result = orch.handle_request("What is machine learning?")
print(result.status)  # "success", "partial", "failed"
```

### 2. **Personality Manager** (`phase1_personality_manager.py`)

Manages **5 distinct personas** with different reasoning styles.

**Personas:**
- **JARVIS**: Wise, proactive mentor (default)
- **FRIDAY**: Terse, tactical, math-focused
- **EDITH**: System-level, direct access
- **TARS**: Brutally honest, calls out errors
- **CORTANA**: Strategic, high-level planning

**Usage:**
```python
from phase1_personality_manager import PersonalityManager, Persona

pm = PersonalityManager()
pm.switch_persona(Persona.FRIDAY)  # Switch to FRIDAY
prompt = pm.get_system_prompt()    # Get LLM system prompt
```

### 3. **Capability Manager** (`phase1_capability_manager.py`)

Manages **learned capabilities** (skills SAIS has acquired).

**Key Features:**
- Create new capabilities
- Store and retrieve capabilities
- Track usage and performance
- Search by name, tag, category
- Record improvements

**Usage:**
```python
from phase1_capability_manager import CapabilityManager, CapabilityCategory

cm = CapabilityManager()
cap_id = cm.create_capability(
    name="Generate Lean 4 Proofs",
    code="def generate_proof(...): pass",
    category=CapabilityCategory.MATH,
    tags=["math", "proof", "lean4"]
)
```

### 4. **Memory System** (`phase1_memory.py`)

Dual-layer memory (short-term session + long-term persistent).

**Features:**
- Store any type of data
- Semantic search (Phase 1: keyword; Phase 2: embeddings)
- Automatic importance scoring
- Link related memories
- Export/import data

**Usage:**
```python
from phase1_memory import MemorySystem, MemoryType

mem = MemorySystem()
record_id = mem.store(
    content="User learned about XYZ",
    record_type=MemoryType.KNOWLEDGE,
    tags=["learning"],
    importance=0.8
)

results = mem.search("learning", limit=5)
```

### 5. **SAIS Kernel** (`phase1_sais_kernel.py`)

**Main integration point** that coordinates all components.

**Responsibilities:**
- Initialize subsystems
- Route requests to orchestrator
- Manage state
- Provide unified API

**Usage:**
```python
from phase1_sais_kernel import SAISKernel

sais = SAISKernel(name="SAIS Alpha")
response = sais.process_request("Teach me about AI")

status = sais.get_status()
print(f"Total requests: {status['total_requests']}")
```

---

## Running SAIS

### Interactive Mode

```bash
python3 phase1_sais_kernel.py
```

This launches an interactive REPL where you can:
- Type requests (e.g., "What is machine learning?")
- Check status: `status`
- List capabilities: `capabilities`
- View pending approvals: `approvals`
- Switch personas: `persona friday`
- Export data: `export`

### Programmatic Mode

```python
from phase1_sais_kernel import SAISKernel

# Initialize
sais = SAISKernel(name="MyAI")

# Process requests
response = sais.process_request("Learn about deep learning")

# Check pending approvals
approvals = sais.get_pending_approvals()
if approvals:
    sais.approve_plan(approvals[0]['plan_id'])

# Get status
print(sais.get_status())

# Export all data
sais.export_all_data("/tmp/sais_export.json")
```

### As HTTP API (Future)

Phase 4 will include FastAPI wrapper:

```bash
# Run API server
python3 backends/python/main.py

# Usage
curl -X POST http://localhost:8000/request \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello SAIS"}'
```

---

## API Reference

### SAISKernel

#### `process_request(user_input: str) → Dict[str, Any]`

Main method to submit requests.

**Request:**
```python
response = sais.process_request("Tell me about machine learning")
```

**Response:**
```json
{
  "request_id": "REQ_0001",
  "status": "success",
  "persona": "jarvis",
  "result": {
    "status": "success",
    "output": {...},
    "execution_time": 2.5,
    "errors": []
  },
  "metadata": {
    "intent_type": "query",
    "confidence": 0.85,
    "timestamp": "2026-04-03T10:00:00"
  }
}
```

#### `get_status() → Dict[str, Any]`

Get system status and statistics.

```python
status = sais.get_status()
# Returns: uptime, request_count, memory stats, capabilities stats, etc.
```

#### `switch_persona(persona_name: str) → Dict[str, Any]`

Switch to a different persona.

```python
result = sais.switch_persona("friday")
# Returns: confirmation, new persona, greeting
```

#### `list_capabilities(category: Optional[str]) → Dict[str, Any]`

List available capabilities.

```python
caps = sais.list_capabilities(category="math")
# Returns: count, list of capabilities with stats
```

#### `get_pending_approvals() → List[Dict]`

Get plans awaiting user approval.

```python
approvals = sais.get_pending_approvals()
for approval in approvals:
    sais.approve_plan(approval['plan_id'])
```

#### `export_all_data(output_file: str) → Dict[str, Any]`

Export all system data.

```python
sais.export_all_data("/tmp/backup.json")
# Creates: backup.json, backup_memory.json, backup_capabilities.json
```

---

## Development Roadmap

### Phase 1: ✅ Core Kernel (Current)

- [x] Orchestrator engine
- [x] Personality system
- [x] Capability manager
- [x] Memory system
- [x] Integration & testing

**Deliverables:** `phase1_*.py` files, tests, documentation

---

### Phase 2: Self-Evolution Engine

**Timeline:** 2-3 weeks

**Deliverables:**
- Evolution detection system
- Change proposal generation
- User approval workflow
- Rollback system
- Continuous monitoring

**Key Files:**
- `phase2_evolution_engine.py`
- `phase2_proposal_validator.py`
- `phase2_rollback_manager.py`

---

### Phase 3: Tool Integration

**Timeline:** 2-3 weeks

**Deliverables:**
- Web scraping tool
- Code execution sandbox
- File operations
- Math tools (Lean 4 integration)
- Tool registry & routing

**Key Files:**
- `phase3_web_tool.py`
- `phase3_code_executor.py`
- `phase3_file_tool.py`
- `phase3_math_tool.py`

---

### Phase 4: UI System

**Timeline:** 3-4 weeks

**Deliverables:**
- Jarvis-style web interface
- Real-time inference visualization
- Three.js 3D dashboard
- Mobile responsive design
- LLM integration (Ollama)

**Key Files:**
- `ui/web/index.html`
- `ui/web/app.js`
- `backends/python/main.py` (FastAPI)

---

### Phase 5: Vector Memory & Embeddings

**Timeline:** 2 weeks

**Deliverables:**
- Embedding generation (Phase 1: keywords only)
- Semantic search
- Similarity matching
- Vector storage optimization

**Key Files:**
- `phase5_embedding_system.py`
- `phase5_vector_store.py`

---

### Phase 6: AIMO Engine

**Timeline:** 4 weeks

**Deliverables:**
- Lean 4 proof generation
- Formal verification
- Competitive problem-solving
- Learning path generation
- Mathematics reasoning module

**Key Files:**
- `phase6_lean4_integrator.py`
- `phase6_aimo_solver.py`
- `phase6_math_reasoner.py`

---

## Platform Deployment

### Python Backend (Reference Implementation)

```bash
# Run directly
python3 phase1_sais_kernel.py

# Or as service with FastAPI (Phase 4)
python3 backends/python/main.py
```

### JavaScript/Browser (Phase 4)

```bash
cd ui/web
npm install
npm run dev

# Or with WebLLM for local LLM inference
```

### Mobile App (Phase 4)

```bash
cd ui/mobile
npm install
npm run android    # or ios
```

### Docker Container (Phase 4)

```bash
docker build -t sais:phase1 .
docker run -it -p 8000:8000 sais:phase1
```

---

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Test Individual Components

```bash
python3 -m pytest tests/test_orchestrator.py -v
python3 -m pytest tests/test_memory.py -v
python3 -m pytest tests/test_capabilities.py -v
```

### Manual Component Tests

```bash
python3 phase1_orchestrator.py          # Test orchestrator
python3 phase1_memory.py                # Test memory
python3 phase1_capability_manager.py    # Test capabilities
python3 phase1_personality_manager.py   # Test personalities
```

---

## Configuration

### Storage Directories

Edit `phase1_sais_kernel.py`:

```python
sais = SAISKernel(
    name="MyAI",
    storage_dir="/custom/path/sais",  # Change storage location
    verbose=True
)
```

### Logging

Edit logging config in any component:

```python
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'phase1_...'"

**Solution:** Make sure you're in the correct directory:
```bash
cd /path/to/sais
python3 phase1_sais_kernel.py
```

### Issue: "Permission denied" when creating storage directories

**Solution:** Ensure write permissions:
```bash
mkdir -p /tmp/sais
chmod 755 /tmp/sais
```

### Issue: Memory/Capabilities not persisting

**Solution:** Check storage directory exists and is writable:
```bash
ls -la /tmp/sais/memory/
ls -la /tmp/sais/capabilities/
```

---

## Next Steps

1. **Test Phase 1:** Run all components and verify they work
2. **Customize:** Modify system prompts, personas, categories to fit your needs
3. **Integrate LLM:** In Phase 4, wire up Ollama or WebLLM
4. **Add Tools:** In Phase 3, implement tool execution
5. **Deploy:** Choose deployment target (web, mobile, desktop)

---

## Contributing

Contributions are welcome!

1. Create feature branch: `git checkout -b feature/my-feature`
2. Write tests for new code
3. Run tests: `pytest tests/ -v`
4. Submit PR with clear description

---

## License

MIT License - See LICENSE.txt

---

## Resources

- **Master Specification:** `SAIS_Master_Specification.md`
- **Architecture:** See component docs
- **API Reference:** See above
- **Roadmap:** See Development Roadmap section

---

## Support

For issues, questions, or suggestions:
- Check existing documentation
- Review component tests
- Check component docstrings
- Create an issue with details

---

**Happy building! 🚀**

*SAIS Phase 1 - Foundation of your personal AI operating system*

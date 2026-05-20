# 🚀 SAIS Phase 1: Quick Start Guide

**Get SAIS running in 5 minutes**

---

## 🎯 TL;DR

```bash
# 1. Get the files
cd sais

# 2. Run it
python3 phase1_sais_kernel.py

# 3. Type your request
You: What is machine learning?

# 4. SAIS responds with the persona it selected
SAIS [JARVIS]> ...
```

---

## 📦 What You Have

**7 production-ready Python modules:**

1. **`phase1_orchestrator.py`** (600 lines)
   - Central decision engine
   - Intent parsing & planning
   - Execution & reflection

2. **`phase1_personality_manager.py`** (450 lines)
   - 5 distinct personas (Jarvis, Friday, Edith, TARS, Cortana)
   - Automatic persona selection
   - System prompt injection

3. **`phase1_memory.py`** (750 lines)
   - Short-term + long-term memory
   - Semantic search (Phase 1: keywords)
   - Import/export capabilities

4. **`phase1_capability_manager.py`** (850 lines)
   - Store learned capabilities
   - Track performance metrics
   - Search by name/tag/category

5. **`phase1_sais_kernel.py`** (550 lines)
   - Main integration point
   - Unified API for all subsystems
   - Interactive REPL

6. **`SAIS_Master_Specification.md`**
   - Complete BRD + LLD + Omega Architecture
   - All design decisions documented
   - Roadmap through Phase 6

7. **`SAIS_PHASE1_README.md`**
   - Comprehensive documentation
   - API reference
   - Deployment guide

---

## 🏃 Get Started in 30 Seconds

### Option 1: Interactive Demo

```bash
python3 phase1_sais_kernel.py

# Then type:
What is machine learning?
status
capabilities
persona friday
help
```

### Option 2: Programmatic

```python
from phase1_sais_kernel import SAISKernel

sais = SAISKernel(name="MyAI")
response = sais.process_request("Hello world")
print(response['persona'])      # Shows which persona responded
print(response['result']['output'])  # The response
```

### Option 3: Component-Level

```python
from phase1_orchestrator import Orchestrator
from phase1_memory import MemorySystem
from phase1_capability_manager import CapabilityManager

orch = Orchestrator()
result = orch.handle_request("What is AI?")
print(result.status)
```

---

## 🏗️ Architecture At A Glance

```
┌─────────────────────────────────────────────┐
│         USER REQUEST                        │
│      "Teach me machine learning"            │
└────────────────────┬────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│      ORCHESTRATOR (Decision Engine)         │
│  - Analyze intent                           │
│  - Generate plan                            │
│  - Route to executor                        │
│  - Reflect on results                       │
└────────────────────┬────────────────────────┘
                     ↓
        ┌────────────┬───────────┐
        ↓            ↓           ↓
   ┌─────────┐ ┌──────────┐ ┌─────────┐
   │PERSONALITY│CAPABILITY │ MEMORY  │
   │ MANAGER │ │ MANAGER  │ │ SYSTEM  │
   │ (5 modes)│ │(learned) │ │(storage)│
   └─────────┘ └──────────┘ └─────────┘
        ↓            ↓           ↓
        └────────────┴───────────┘
                ↓
┌─────────────────────────────────────────────┐
│          RESPONSE TO USER                   │
│   Persona: JARVIS                           │
│   Status: success                           │
│   Output: [structured response]             │
└─────────────────────────────────────────────┘
```

---

## 📊 Component Overview

| Component | Lines | Purpose | Status |
|-----------|-------|---------|--------|
| Orchestrator | 600 | Decision engine | ✅ Complete |
| Personality | 450 | Persona system | ✅ Complete |
| Memory | 750 | Storage + search | ✅ Complete |
| Capability | 850 | Skill repository | ✅ Complete |
| Kernel | 550 | Integration | ✅ Complete |
| **TOTAL** | **3,200** | **Phase 1 Core** | **✅ Ready** |

---

## 🎮 Interactive Commands

When running `python3 phase1_sais_kernel.py`:

```
help              - Show help
status            - System status
capabilities      - List capabilities
approvals         - Pending approvals
persona [name]    - Switch persona
export            - Export all data
exit              - Quit
```

---

## 🔄 Data Flow Example

### Example: "Teach me how to generate Lean 4 proofs"

```
1. USER INPUT
   "Teach me how to generate Lean 4 proofs"

2. ORCHESTRATOR.analyze_intent()
   → IntentType.LEARNING_REQUEST
   → requires_approval: False

3. PERSONALITY.select_persona()
   → Matches keyword "teach"
   → Selects JARVIS (mentor mode)

4. ORCHESTRATOR.generate_plan()
   → Step 1: Generate learning plan
   → Step 2: Research Lean 4
   → Step 3: Create capability
   → Step 4: Test capability

5. MEMORY.store()
   → Stores learning request
   → Stores results
   → Tags: ["learning", "lean4", "math"]

6. CAPABILITY.create_capability()
   → Name: "Generate Lean 4 Proofs"
   → Category: MATH
   → Code: [implementation]
   → Status: learned

7. RESPONSE TO USER
   {
     "persona": "jarvis",
     "status": "success",
     "plan_steps": 4,
     "new_capability": "Generate Lean 4 Proofs"
   }
```

---

## 💾 Storage Structure

After running SAIS:

```
/tmp/sais/
├── memory/
│   └── index.json          # All memories
│       {
│         "records": [
│           {
│             "id": "...",
│             "type": "conversation",
│             "content": "...",
│             "importance": 0.8
│           }
│         ]
│       }
│
└── capabilities/
    └── index.json          # All capabilities
        {
          "capabilities": [
            {
              "id": "...",
              "name": "Generate Lean 4 Proofs",
              "category": "math",
              "usage_count": 5,
              "success_rate": 0.95
            }
          ]
        }
```

---

## 📈 What SAIS Tracks

### Per Session:
- ✅ Request count
- ✅ Execution times
- ✅ Intent distribution
- ✅ Persona usage

### Per Capability:
- ✅ Usage count
- ✅ Success rate
- ✅ Performance score
- ✅ Improvement history

### Per Memory Record:
- ✅ Type (conversation, error, knowledge)
- ✅ Importance score
- ✅ Links to related records
- ✅ Semantic tags

---

## 🔌 API Overview

### Main Entry Point

```python
response = sais.process_request("Your request")

# response contains:
{
    "request_id": "REQ_0001",
    "status": "success",
    "persona": "jarvis",
    "result": {
        "status": "success",
        "output": {...},
        "execution_time": 2.5,
        "errors": []
    }
}
```

### System Status

```python
status = sais.get_status()

# returns:
{
    "status": "operational",
    "total_requests": 42,
    "current_persona": "jarvis",
    "memory": {...},
    "capabilities": {...}
}
```

### Capability Management

```python
# List capabilities
caps = sais.list_capabilities(category="math")

# Get execution history
history = sais.get_execution_history(limit=10)

# Check pending approvals
approvals = sais.get_pending_approvals()
```

---

## 🚀 Next: Phase 2-6

### Phase 2: Evolution Engine (2-3 weeks)
- Detect improvement opportunities
- Propose changes
- User approval workflow
- Rollback system

### Phase 3: Tool Integration (2-3 weeks)
- Web scraping
- Code execution sandbox
- File operations
- Math tools (Lean 4)

### Phase 4: UI System (3-4 weeks)
- Web interface
- Mobile app
- LLM integration (Ollama)
- Real-time visualization

### Phase 5: Vector Memory (2 weeks)
- Embeddings
- Semantic search
- Similarity matching

### Phase 6: AIMO Engine (4 weeks)
- Lean 4 proof generation
- Formal verification
- Competitive solving

---

## ✅ Verification Checklist

After setup, verify:

- [ ] All 7 files downloaded/created
- [ ] Python 3.9+ installed
- [ ] Run `python3 phase1_orchestrator.py` - passes tests
- [ ] Run `python3 phase1_memory.py` - passes tests
- [ ] Run `python3 phase1_capability_manager.py` - passes tests
- [ ] Run `python3 phase1_personality_manager.py` - passes tests
- [ ] Run `python3 phase1_sais_kernel.py` - interactive REPL works
- [ ] Can make a request and get a response
- [ ] Data persists in `/tmp/sais/`

---

## 🐛 Common Issues & Fixes

**Q: ModuleNotFoundError?**
A: Make sure all 5 phase1_*.py files are in the same directory

**Q: Permission denied /tmp/sais?**
A: Run `chmod 755 /tmp/sais` or change storage_dir

**Q: No response to requests?**
A: Check logs, run individual component tests first

**Q: Data not persisting?**
A: Verify /tmp/sais/memory and /tmp/sais/capabilities exist

---

## 📚 Learning Path

1. **Start here:** Interactive demo
   ```bash
   python3 phase1_sais_kernel.py
   ```

2. **Understand components:** Read docstrings
   ```python
   from phase1_orchestrator import Orchestrator
   help(Orchestrator.handle_request)
   ```

3. **Trace execution:** Run with debug logging
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

4. **Customize:** Modify system prompts, add personas, create capabilities

5. **Integrate:** Add your own tools and features (Phase 3)

---

## 🎓 For Learning

The codebase is **intentionally well-documented** for learning:

- **Docstrings:** Every class and method explained
- **Type hints:** Full type annotations for clarity
- **Comments:** Key logic explained inline
- **Tests:** Each module has `if __name__ == "__main__"` tests
- **Examples:** Realistic usage patterns throughout

Use this to:
- ✅ Understand AI architecture
- ✅ Learn system design patterns
- ✅ Practice Python best practices
- ✅ Build your own extensions

---

## 🏆 You Now Have

✅ A working **AI operating system kernel**  
✅ **3,200 lines** of production code  
✅ **Complete documentation** and specification  
✅ **Foundation** for Phases 2-6  
✅ **Zero cloud dependency**—fully local  
✅ **Extensible architecture** for your needs  

---

## 🚀 Ready to Build

Pick your next step:

1. **Run it:** `python3 phase1_sais_kernel.py`
2. **Test it:** `python3 phase1_*.py` (each file has tests)
3. **Customize it:** Modify personas, add capabilities
4. **Extend it:** Build Phase 2 (Evolution Engine)
5. **Deploy it:** Choose web/mobile/desktop

---

**Welcome to SAIS. You're building something remarkable. 🌟**

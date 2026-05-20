# SAIS: Sovereign Adaptive Intelligence System
> A modular, local-first artificial intelligence operating system designed for dynamic capability generation, multi-persona orchestration, and structured task execution.

## 📑 Table of Contents
1. [Overview](#-overview)
2. [Supported AI Models](#-supported-ai-models)
3. [Key Features](#-key-features)
4. [The Persona System](#-the-persona-system)
5. [Architecture](#-architecture)
6. [Quickstart](#-quickstart)
7. [Development Roadmap](#-development-roadmap)
8. [UI Screenshots](#-ui-screenshots)
9. [Disclaimer](#-disclaimer)

---

## 🔬 Overview

The **Sovereign Adaptive Intelligence System (SAIS)** is a locally hosted AI ecosystem. Built entirely independent of cloud APIs, SAIS processes all data locally on the host machine to ensure absolute privacy and data sovereignty. 

SAIS is designed to move beyond standard conversational interfaces into functional automation. It can dynamically learn new tasks by writing and saving its own code logic, store long-term context, and switch between specialized reasoning modes to handle different types of user requests effectively.

<h3>SAIS Kernel Interface : the Llama 3 8B Model (~4.5GB)</h3>
<img width="1400" height="786" alt="image" src="https://github.com/user-attachments/assets/be4785e0-85ce-44d1-9aed-af7dcea2494e" />
<br/>

---

## 🧠 Supported AI Models

SAIS is built to leverage local inference engines (such as WebLLM, Ollama, or ggml) and provides the user with the flexibility to choose the appropriate model based on their hardware capabilities and task complexity. 

The system natively supports and allows seamless switching between:

* **Llama 3.2 1B (~700MB):** Highly efficient and lightweight. Ideal for rapid task execution, basic system commands, and operation on machines with limited GPU memory.
* **Llama 3 8B (~4.5GB):** A more robust model suited for deep reasoning, complex mathematical analysis, extended code generation, and sophisticated pedagogical tasks. 

---

## ✨ Key Features

* **Local-First Privacy:** All processing, memory storage, and capability generation occur entirely on your local hardware.
* **Dynamic Capability Expansion:** When presented with a novel task, the system can write physical `.js` or `.py` modules, save them locally, and mount them as new tools for future use.
* **Dual-Layer Memory:** Utilizes a short-term session context for active conversations and a persistent long-term JSON storage system (with tagging and importance scoring) for continuous learning.
* **Live Telemetry:** A transparent dashboard that logs every system thought process, hardware allocation, and tool execution in real-time.
* **User-Gated Evolution:** The system proposes code optimizations and improvements, which are placed in an Approval Queue. No system evolution occurs without explicit user authorization.

---

## 🎭 The Persona System

SAIS dynamically analyzes the user's intent and routes the prompt to one of five specialized reasoning engines, optimizing the output for the specific task at hand.

| Persona | Role | Optimized For |
| :--- | :--- | :--- |
| **JARVIS** | *The Mentor* (Default) | General guidance, learning, and proactive assistance. |
| **FRIDAY** | *The Tactician* | Data processing, logic, and rapid mathematical problem-solving. |
| **EDITH** | *The Hacker* | Direct system commands, DOM manipulation, and code execution. |
| **TARS** | *The Critic* | Debugging, error analysis, and validating logical consistency. |
| **CORTANA** | *The Strategist* | High-level planning, structural organization, and long-term goals. |

---

## 🏗️ Architecture

SAIS utilizes a clean, modular architecture that separates decision-making from execution and interface layers.

```text
┌─────────────────────────────────────────────┐
│              USER INTERFACE                 │
│      (WebUI / Local API Dashboard)          │
└────────────────────┬────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│        ORCHESTRATOR (Decision Engine)       │
│  - Parses Intent & Validates Dependencies   │
│  - Generates Step-by-Step Execution Plans   │
└────────────────────┬────────────────────────┘
                     ↓
        ┌────────────┼───────────┐
        ↓            ↓           ↓
   ┌─────────┐ ┌──────────┐ ┌─────────┐
   │ PERSONA │ │CAPABILITY│ │ MEMORY  │
   │ ROUTER  │ │ REPOSITORY │ │ ENGINE  │
   └─────────┘ └──────────┘ └─────────┘
```

---

## 🚀 Quickstart

### Prerequisites
* Python 3.9+
* Local inference engine setup (e.g., Ollama or WebLLM dependencies)

### Installation

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/sais-kernel.git](https://github.com/yourusername/sais-kernel.git)
cd sais-kernel
```

2. Boot the core kernel:
```bash
python3 phase1_sais_kernel.py
```

### Core Commands
Once the system is active, you can interact naturally or use the following system commands:
* `status` - View active memory, hardware uptime, and system diagnostics.
* `capabilities` - List all locally learned logic modules.
* `approvals` - View the queue of self-evolution tasks awaiting user authorization.
* `persona [name]` - Manually override the active persona.

---

## 🗺️ Development Roadmap

* **Phase 1: Core Kernel** - Orchestration, Memory, Personas, Capabilities (Completed).
* **Phase 2: Self-Evolution Engine** - Improvement detection, proposal generation, and rollback systems.
* **Phase 3: Tool Integration** - Local web scraping, sandboxed code execution, and file I/O operations.
* **Phase 4: UI + API Bridge** - FastAPI integration linking the Python backend to the local WebGL interface.
* **Phase 5: Vector Memory** - Semantic embeddings and vector search for expanded context retention.
* **Phase 6: AIMO Engine** - Lean 4 formal verification integration for structured mathematical problem-solving.

---

## 📷 UI Screenshots

<h3>SAIS Kernel Interface : the Llama 3.2 1B Model (~700MB)</h3>
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/7b90bdcc-42f0-44a2-981c-0341ba8ee88d" />
<br/>
<br/>

<h3>Loading the Llama 3 8B Model</h3>
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/dfcb64f1-794b-48b6-b53f-9368604c3539" />
<br/>
<br/>

<h3>The Llama 3 8B Model is Ready for Use</h3>
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/0a3f1109-6ee9-4b72-b5cd-ba7eb4b0701d" />

---


## ⚠️ Disclaimer

SAIS is a powerful system designed with local-first execution capabilities, including direct system-level access and physical codebase generation. 
The owner of this repository, along with any developers and contributors to this repository, assume no liability and are not responsible for any misuse, damage, data loss, or unauthorized access caused by utilizing this software. Users are solely responsible for managing the Approval Queue, reviewing AI-generated logic before execution, and ensuring the secure operation of their local environments.

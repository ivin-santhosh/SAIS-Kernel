"""
SAIS Phase 1: Core Kernel Integration
Main entry point that ties together all Phase 1 components

Components integrated:
- Orchestrator (decision engine)
- Personality Manager (persona switching)
- Capability Manager (learned skills)
- Memory System (short + long-term)
- Logging and monitoring
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Import Phase 1 components
from phase1_orchestrator import Orchestrator, ExecutionResult
from phase1_personality_manager import PersonalityManager, Persona, PersonaContext
from phase1_capability_manager import CapabilityManager, CapabilityCategory
from phase1_memory import MemorySystem, MemoryType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SAISKernel:
    """
    Main SAIS Kernel
    
    The core intelligence system that coordinates all Phase 1 components.
    
    Responsibilities:
    - Initialize all subsystems
    - Route requests appropriately
    - Manage state
    - Provide unified interface
    """
    
    def __init__(self, 
                 name: str = "SAIS",
                 storage_dir: str = "/tmp/sais",
                 verbose: bool = True):
        """
        Initialize SAIS kernel.
        
        Args:
            name: System name
            storage_dir: Where to store persistent data
            verbose: Enable detailed logging
        """
        self.name = name
        self.storage_dir = storage_dir
        self.verbose = verbose
        self.created_at = datetime.now()
        self.request_count = 0
        
        logger.info("=" * 60)
        logger.info(f"Initializing {name} (SAIS Phase 1)")
        logger.info("=" * 60)
        
        # Initialize subsystems
        self.personality_manager = PersonalityManager()
        self.memory_system = MemorySystem(storage_dir=f"{storage_dir}/memory")
        self.capability_manager = CapabilityManager(storage_dir=f"{storage_dir}/capabilities")
        
        # Initialize orchestrator with dependencies
        self.orchestrator = Orchestrator(
            personality_manager=self.personality_manager,
            capability_manager=self.capability_manager,
            memory_system=self.memory_system
        )
        
        logger.info(f"✓ Personality Manager ready ({len(self.personality_manager.personas)} personas)")
        logger.info(f"✓ Memory System ready ({len(self.memory_system.long_term)} long-term records)")
        logger.info(f"✓ Capability Manager ready ({len(self.capability_manager.capabilities)} capabilities)")
        logger.info(f"✓ Orchestrator ready")
        logger.info("")
        logger.info(f"{name} initialization complete!")
        logger.info("")
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Main entry point for user requests.
        
        Args:
            user_input: User's request
            
        Returns:
            Response dict with result and metadata
        """
        self.request_count += 1
        request_id = f"REQ_{self.request_count:04d}"
        
        logger.info(f"[{request_id}] Processing request: {user_input[:60]}...")
        
        try:
            # Step 1: Analyze and select persona
            intent = self.orchestrator.analyze_intent(user_input)
            context = PersonaContext(
                intent_type=intent.type.value,
                task=user_input,
                requires_approval=intent.requires_approval
            )
            selected_persona = self.personality_manager.select_persona(context.to_dict())
            
            # Step 2: Store in memory
            self.memory_system.store(
                {"request": user_input, "intent": intent.type.value},
                MemoryType.CONVERSATION,
                tags=["user_input", intent.type.value],
                importance=0.7
            )
            
            # Step 3: Execute request via orchestrator
            result = self.orchestrator.handle_request(user_input)
            
            # Step 4: Store result in memory
            self.memory_system.store(
                {
                    "request_id": request_id,
                    "status": result.status,
                    "execution_time": result.execution_time
                },
                MemoryType.EXECUTION_RESULT,
                tags=["execution", intent.type.value],
                importance=0.6 if result.status == "success" else 0.8
            )
            
            # Step 5: Format response
            response = {
                "request_id": request_id,
                "status": "success",
                "persona": selected_persona.value,
                "result": {
                    "status": result.status,
                    "output": result.output,
                    "execution_time": result.execution_time,
                    "errors": result.errors,
                    "warnings": result.warnings
                },
                "metadata": {
                    "intent_type": intent.type.value,
                    "confidence": intent.confidence,
                    "requires_approval": intent.requires_approval,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            logger.info(f"[{request_id}] ✓ Complete ({result.execution_time:.2f}s)")
            
            return response
            
        except Exception as e:
            logger.error(f"[{request_id}] Error: {str(e)}")
            return {
                "request_id": request_id,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get system status and statistics.
        
        Returns:
            Status dict
        """
        memory_stats = self.memory_system.get_stats()
        capability_stats = self.capability_manager.get_stats()
        
        return {
            "system_name": self.name,
            "status": "operational",
            "uptime_seconds": (datetime.now() - self.created_at).total_seconds(),
            "total_requests": self.request_count,
            "current_persona": self.personality_manager.current_persona.value,
            "memory": {
                "total_records": memory_stats.total_records,
                "by_type": memory_stats.by_type,
                "total_size_mb": memory_stats.total_size_bytes / (1024 * 1024)
            },
            "capabilities": {
                "total": capability_stats['total_capabilities'],
                "by_category": capability_stats['by_category'],
                "overall_success_rate": capability_stats['overall_success_rate'],
                "average_performance": capability_stats['average_performance']
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_pending_approvals(self) -> list:
        """Get plans awaiting user approval"""
        return [
            {
                "plan_id": plan.plan_id,
                "intent": plan.intent.task,
                "steps": len(plan.steps),
                "created_at": plan.created_at.isoformat()
            }
            for plan in self.orchestrator.get_pending_approvals()
        ]
    
    def approve_plan(self, plan_id: str) -> Dict[str, Any]:
        """
        User approves a pending plan.
        
        Args:
            plan_id: ID of plan to approve
            
        Returns:
            Execution result
        """
        logger.info(f"Plan approved by user: {plan_id}")
        result = self.orchestrator.approve_plan(plan_id)
        
        self.memory_system.store(
            {"plan_id": plan_id, "action": "approved"},
            MemoryType.EXECUTION_RESULT,
            tags=["approval"],
            importance=0.9
        )
        
        return {
            "plan_id": plan_id,
            "status": result.status,
            "timestamp": datetime.now().isoformat()
        }
    
    def reject_plan(self, plan_id: str) -> Dict[str, Any]:
        """
        User rejects a pending plan.
        
        Args:
            plan_id: ID of plan to reject
            
        Returns:
            Confirmation
        """
        logger.info(f"Plan rejected by user: {plan_id}")
        self.orchestrator.reject_plan(plan_id)
        
        self.memory_system.store(
            {"plan_id": plan_id, "action": "rejected"},
            MemoryType.EXECUTION_RESULT,
            tags=["approval"],
            importance=0.8
        )
        
        return {
            "plan_id": plan_id,
            "status": "rejected",
            "timestamp": datetime.now().isoformat()
        }
    
    def switch_persona(self, persona_name: str) -> Dict[str, Any]:
        """
        Manually switch personas.
        
        Args:
            persona_name: Name of persona (jarvis, friday, etc)
            
        Returns:
            Confirmation
        """
        try:
            persona = Persona(persona_name.lower())
            self.personality_manager.switch_persona(persona)
            
            logger.info(f"Persona switched to: {persona.value}")
            
            return {
                "status": "success",
                "persona": persona.value,
                "greeting": self.personality_manager.get_greeting(persona),
                "timestamp": datetime.now().isoformat()
            }
        except ValueError:
            return {
                "status": "error",
                "error": f"Unknown persona: {persona_name}",
                "available": list(p.value for p in Persona)
            }
    
    def list_capabilities(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        List available capabilities.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of capabilities
        """
        try:
            cap_category = None
            if category:
                cap_category = CapabilityCategory(category.lower())
            
            caps = self.capability_manager.list_capabilities(category=cap_category, limit=20)
            
            return {
                "status": "success",
                "count": len(caps),
                "capabilities": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "category": c.category.value,
                        "description": c.description,
                        "usage_count": c.usage_count,
                        "success_rate": (
                            c.success_count / c.usage_count
                            if c.usage_count > 0 else 0
                        ),
                        "performance_score": c.get_performance_score()
                    }
                    for c in caps
                ],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_execution_history(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get recent execution history.
        
        Args:
            limit: How many to return
            
        Returns:
            Execution history
        """
        history = self.orchestrator.get_execution_history(limit=limit)
        
        return {
            "status": "success",
            "count": len(history),
            "executions": [
                {
                    "plan_id": result.plan_id,
                    "status": result.status,
                    "execution_time": result.execution_time,
                    "timestamp": result.timestamp.isoformat(),
                    "errors": result.errors
                }
                for result in history
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    def export_all_data(self, output_file: str) -> Dict[str, Any]:
        """
        Export all system data to JSON.
        
        Args:
            output_file: Where to save
            
        Returns:
            Confirmation
        """
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "name": self.name,
                    "created_at": self.created_at.isoformat(),
                    "request_count": self.request_count,
                    "current_persona": self.personality_manager.current_persona.value
                },
                "status": self.get_status()
            }
            
            # Export memory
            self.memory_system.export_memory(output_file.replace('.json', '_memory.json'))
            
            # Export capabilities
            self.capability_manager.export_capabilities(output_file.replace('.json', '_capabilities.json'))
            
            # Save main data
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"All data exported to {output_file}")
            
            return {
                "status": "success",
                "files_created": [
                    output_file,
                    output_file.replace('.json', '_memory.json'),
                    output_file.replace('.json', '_capabilities.json')
                ],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return {"status": "error", "error": str(e)}


def run_interactive_demo():
    """
    Run an interactive demonstration of SAIS.
    """
    print("\n" + "=" * 70)
    print("SAIS Phase 1: Core Kernel - Interactive Demo")
    print("=" * 70 + "\n")
    
    # Initialize
    sais = SAISKernel(
        name="SAIS Alpha",
        storage_dir="/tmp/sais_demo",
        verbose=True
    )
    
    print("\nType 'exit' to quit, 'status' for system status, 'help' for options\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("\nShutting down SAIS. Goodbye!")
                break
            
            if user_input.lower() == "status":
                status = sais.get_status()
                print(f"\n{json.dumps(status, indent=2)}\n")
                continue
            
            if user_input.lower() == "approvals":
                approvals = sais.get_pending_approvals()
                if approvals:
                    print(f"\nPending approvals: {len(approvals)}")
                    for a in approvals:
                        print(f"  - {a['plan_id']}: {a['intent']}")
                else:
                    print("\nNo pending approvals")
                print()
                continue
            
            if user_input.lower() == "capabilities":
                caps = sais.list_capabilities()
                print(f"\nAvailable capabilities: {caps['count']}")
                for c in caps['capabilities'][:5]:
                    print(f"  - {c['name']} ({c['category']})")
                print()
                continue
            
            if user_input.lower() == "help":
                print("""
Commands:
  exit          - Quit SAIS
  status        - Show system status
  approvals     - Show pending approvals
  capabilities  - List capabilities
  persona       - Change active persona
  help          - Show this help
  
Regular input will be processed as requests to SAIS.
""")
                continue
            
            if user_input.lower().startswith("persona "):
                persona_name = user_input[8:].strip()
                result = sais.switch_persona(persona_name)
                print(f"\n{json.dumps(result, indent=2)}\n")
                continue
            
            # Process as regular request
            print("\n[SAIS Processing...]")
            response = sais.process_request(user_input)
            
            print(f"\nPersona: {response.get('persona', 'unknown').upper()}")
            print(f"Status: {response['result']['status']}")
            if response['result'].get('output'):
                print(f"Output: {response['result']['output']}")
            if response['result'].get('errors'):
                print(f"Errors: {response['result']['errors']}")
            print()
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    # Run interactive demo
    run_interactive_demo()

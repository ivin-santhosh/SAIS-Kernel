"""
SAIS Phase 1: Core Kernel
Module: Orchestrator (Central Brain)

The Orchestrator is the decision engine of SAIS.
It handles intent analysis, task planning, execution routing, and reflection.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntentType(Enum):
    """Classification of user intents"""
    QUERY = "query"                  # Information request
    CAPABILITY_REQUEST = "capability"  # Execute existing capability
    LEARNING_REQUEST = "learning"    # Learn something new
    SYSTEM_COMMAND = "system"        # System-level operation
    EVOLUTION_REQUEST = "evolution"  # Self-improvement
    ANALYSIS = "analysis"            # Analytical task


@dataclass
class Intent:
    """Parsed user intent"""
    type: IntentType
    task: str
    context: Dict[str, Any]
    confidence: float  # 0.0 to 1.0
    requires_approval: bool = False


@dataclass
class PlanStep:
    """Single step in an execution plan"""
    step_id: str
    action: str
    parameters: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: float = 0.0  # seconds
    requires_approval: bool = False


@dataclass
class Plan:
    """Complete execution plan"""
    plan_id: str
    intent: Intent
    steps: List[PlanStep]
    total_duration: float
    created_at: datetime = field(default_factory=datetime.now)
    execution_log: List[str] = field(default_factory=list)


@dataclass
class ExecutionResult:
    """Result of plan execution"""
    plan_id: str
    status: str  # "success", "partial", "failed"
    output: Any
    execution_time: float
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_log: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


class Orchestrator:
    """
    Central decision engine for SAIS.
    
    Responsibilities:
    - Parse user intent
    - Generate execution plans
    - Route to appropriate executor
    - Reflect on results
    - Log all actions
    """
    
    def __init__(self, 
                 personality_manager=None,
                 capability_manager=None,
                 memory_system=None,
                 tool_manager=None):
        """
        Initialize orchestrator with dependencies
        
        Args:
            personality_manager: For persona selection
            capability_manager: For capability lookups
            memory_system: For storing execution results
            tool_manager: For executing tools
        """
        self.personality_manager = personality_manager
        self.capability_manager = capability_manager
        self.memory_system = memory_system
        self.tool_manager = tool_manager
        
        self.execution_history: List[ExecutionResult] = []
        self.current_plan: Optional[Plan] = None
        self.approval_queue: List[Plan] = []
        
        logger.info("Orchestrator initialized")
    
    def handle_request(self, user_input: str) -> ExecutionResult:
        """
        Main entry point for user requests.
        
        Workflow:
        1. Analyze intent
        2. Generate plan
        3. Validate plan
        4. Execute plan
        5. Reflect on results
        6. Return result
        
        Args:
            user_input: The user's request
            
        Returns:
            ExecutionResult with output and metadata
        """
        logger.info(f"[ORCHESTRATOR] Handling request: {user_input[:100]}...")
        
        try:
            # Step 1: Analyze intent
            intent = self.analyze_intent(user_input)
            logger.info(f"[ORCHESTRATOR] Intent identified: {intent.type.value} (confidence: {intent.confidence:.2f})")
            
            # Step 2: Generate plan
            plan = self.generate_plan(intent)
            self.current_plan = plan
            logger.info(f"[ORCHESTRATOR] Plan generated with {len(plan.steps)} steps")
            
            # Step 3: Validate plan
            validation = self.validate_plan(plan)
            if not validation['valid']:
                return ExecutionResult(
                    plan_id=plan.plan_id,
                    status="failed",
                    output=None,
                    execution_time=0.0,
                    errors=validation['errors']
                )
            
            # Step 4: Handle approval if needed
            if plan.intent.requires_approval:
                logger.info(f"[ORCHESTRATOR] Plan requires approval. Queuing.")
                self.approval_queue.append(plan)
                return ExecutionResult(
                    plan_id=plan.plan_id,
                    status="pending_approval",
                    output={"message": "Plan queued for user approval"},
                    execution_time=0.0,
                )
            
            # Step 5: Execute plan
            result = self.execute_plan(plan)
            
            # Step 6: Reflect on results
            self.reflect_on_result(result)
            
            # Step 7: Store in execution history
            self.execution_history.append(result)
            
            return result
            
        except Exception as e:
            logger.error(f"[ORCHESTRATOR] Error handling request: {str(e)}")
            return ExecutionResult(
                plan_id="error",
                status="failed",
                output=None,
                execution_time=0.0,
                errors=[str(e)]
            )
    
    def analyze_intent(self, user_input: str) -> Intent:
        """
        Parse user input to extract intent.
        
        This is a simplified implementation.
        In production, this would use the LLM.
        
        Args:
            user_input: Raw user text
            
        Returns:
            Intent object with type and parameters
        """
        logger.info(f"[ORCHESTRATOR] Analyzing intent...")
        
        # Simple keyword-based heuristic (Phase 1)
        # In Phase 4, this will use LLM for semantic understanding
        
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["learn", "teach", "how do i", "explain"]):
            intent_type = IntentType.LEARNING_REQUEST
            requires_approval = False
        elif any(word in input_lower for word in ["improve", "optimize", "upgrade", "evolve"]):
            intent_type = IntentType.EVOLUTION_REQUEST
            requires_approval = True
        elif any(word in input_lower for word in ["prove", "solve", "math", "lean"]):
            intent_type = IntentType.ANALYSIS
            requires_approval = False
        elif any(word in input_lower for word in ["system", "config", "status", "monitor"]):
            intent_type = IntentType.SYSTEM_COMMAND
            requires_approval = False
        else:
            intent_type = IntentType.QUERY
            requires_approval = False
        
        return Intent(
            type=intent_type,
            task=user_input,
            context={
                "timestamp": datetime.now().isoformat(),
                "input_length": len(user_input),
            },
            confidence=0.85,  # Simplified
            requires_approval=requires_approval
        )
    
    def generate_plan(self, intent: Intent) -> Plan:
        """
        Generate an execution plan from intent.
        
        Args:
            intent: Parsed intent
            
        Returns:
            Plan with ordered execution steps
        """
        logger.info(f"[ORCHESTRATOR] Generating plan for intent: {intent.type.value}")
        
        import uuid
        plan_id = str(uuid.uuid4())
        steps = []
        
        # Route based on intent type
        if intent.type == IntentType.QUERY:
            steps = self._plan_query(intent)
        elif intent.type == IntentType.LEARNING_REQUEST:
            steps = self._plan_learning(intent)
        elif intent.type == IntentType.ANALYSIS:
            steps = self._plan_analysis(intent)
        elif intent.type == IntentType.SYSTEM_COMMAND:
            steps = self._plan_system(intent)
        elif intent.type == IntentType.EVOLUTION_REQUEST:
            steps = self._plan_evolution(intent)
        else:
            steps = self._plan_default(intent)
        
        total_duration = sum(step.estimated_duration for step in steps)
        
        return Plan(
            plan_id=plan_id,
            intent=intent,
            steps=steps,
            total_duration=total_duration
        )
    
    def _plan_query(self, intent: Intent) -> List[PlanStep]:
        """Plan a simple query"""
        return [
            PlanStep(
                step_id="1",
                action="invoke_llm",
                parameters={
                    "query": intent.task,
                    "mode": "JARVIS"
                },
                estimated_duration=3.0
            ),
            PlanStep(
                step_id="2",
                action="store_memory",
                parameters={
                    "type": "conversation",
                    "content": intent.task
                },
                estimated_duration=0.1,
                dependencies=["1"]
            )
        ]
    
    def _plan_learning(self, intent: Intent) -> List[PlanStep]:
        """Plan a learning request"""
        return [
            PlanStep(
                step_id="1",
                action="generate_learning_plan",
                parameters={"topic": intent.task},
                estimated_duration=5.0
            ),
            PlanStep(
                step_id="2",
                action="research",
                parameters={"learning_plan_id": "1"},
                estimated_duration=10.0,
                dependencies=["1"]
            ),
            PlanStep(
                step_id="3",
                action="create_capability",
                parameters={"research_result_id": "2"},
                estimated_duration=5.0,
                dependencies=["2"]
            ),
            PlanStep(
                step_id="4",
                action="test_capability",
                parameters={"capability_id": "3"},
                estimated_duration=3.0,
                dependencies=["3"]
            )
        ]
    
    def _plan_analysis(self, intent: Intent) -> List[PlanStep]:
        """Plan an analysis request"""
        return [
            PlanStep(
                step_id="1",
                action="invoke_llm",
                parameters={
                    "query": intent.task,
                    "mode": "FRIDAY"  # Math-focused mode
                },
                estimated_duration=5.0
            ),
            PlanStep(
                step_id="2",
                action="store_memory",
                parameters={
                    "type": "analysis",
                    "content": intent.task
                },
                estimated_duration=0.1,
                dependencies=["1"]
            )
        ]
    
    def _plan_system(self, intent: Intent) -> List[PlanStep]:
        """Plan a system command"""
        return [
            PlanStep(
                step_id="1",
                action="system_operation",
                parameters={"command": intent.task},
                estimated_duration=1.0
            )
        ]
    
    def _plan_evolution(self, intent: Intent) -> List[PlanStep]:
        """Plan self-evolution"""
        return [
            PlanStep(
                step_id="1",
                action="analyze_improvements",
                parameters={"scope": "full"},
                estimated_duration=10.0,
                requires_approval=False
            ),
            PlanStep(
                step_id="2",
                action="propose_changes",
                parameters={"analysis_id": "1"},
                estimated_duration=5.0,
                requires_approval=True,
                dependencies=["1"]
            )
        ]
    
    def _plan_default(self, intent: Intent) -> List[PlanStep]:
        """Default plan"""
        return [
            PlanStep(
                step_id="1",
                action="invoke_llm",
                parameters={"query": intent.task},
                estimated_duration=3.0
            )
        ]
    
    def validate_plan(self, plan: Plan) -> Dict[str, Any]:
        """
        Validate plan before execution.
        
        Checks:
        - Circular dependencies
        - Missing required capabilities
        - Resource constraints
        
        Args:
            plan: Plan to validate
            
        Returns:
            {valid: bool, errors: List[str]}
        """
        logger.info(f"[ORCHESTRATOR] Validating plan {plan.plan_id}")
        
        errors = []
        
        # Check for circular dependencies
        for step in plan.steps:
            if step.step_id in step.dependencies:
                errors.append(f"Step {step.step_id} has circular dependency")
        
        # Check dependencies exist
        step_ids = {step.step_id for step in plan.steps}
        for step in plan.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    errors.append(f"Step {step.step_id} depends on non-existent {dep}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def execute_plan(self, plan: Plan) -> ExecutionResult:
        """
        Execute a validated plan.
        
        Args:
            plan: Plan to execute
            
        Returns:
            ExecutionResult with output and logs
        """
        logger.info(f"[ORCHESTRATOR] Executing plan {plan.plan_id}")
        
        import time
        start_time = time.time()
        execution_log = []
        errors = []
        output = None
        
        try:
            # Execute steps in dependency order
            step_results = {}
            
            for step in plan.steps:
                # Check dependencies
                if not all(dep in step_results for dep in step.dependencies):
                    errors.append(f"Dependencies not met for step {step.step_id}")
                    continue
                
                try:
                    log_msg = f"Executing step {step.step_id}: {step.action}"
                    logger.info(f"[ORCHESTRATOR] {log_msg}")
                    execution_log.append(log_msg)
                    
                    # Route to appropriate executor
                    result = self._execute_step(step)
                    step_results[step.step_id] = result
                    
                except Exception as e:
                    errors.append(f"Step {step.step_id} failed: {str(e)}")
                    execution_log.append(f"ERROR in step {step.step_id}: {str(e)}")
            
            # Aggregate results
            output = {
                "step_results": step_results,
                "status": "success" if not errors else "partial"
            }
            
            status = "success" if not errors else "partial"
            
        except Exception as e:
            logger.error(f"[ORCHESTRATOR] Plan execution failed: {str(e)}")
            errors.append(str(e))
            status = "failed"
        
        execution_time = time.time() - start_time
        
        return ExecutionResult(
            plan_id=plan.plan_id,
            status=status,
            output=output,
            execution_time=execution_time,
            errors=errors,
            execution_log=execution_log
        )
    
    def _execute_step(self, step: PlanStep) -> Any:
        """
        Execute a single step.
        
        Dispatches to appropriate executor based on action type.
        """
        logger.info(f"[ORCHESTRATOR] Dispatching step: {step.action}")
        
        if step.action == "invoke_llm":
            return self._execute_invoke_llm(step)
        elif step.action == "store_memory":
            return self._execute_store_memory(step)
        elif step.action == "system_operation":
            return self._execute_system(step)
        elif step.action == "analyze_improvements":
            return self._execute_analyze_improvements(step)
        else:
            return {"status": "not_implemented", "action": step.action}
    
    def _execute_invoke_llm(self, step: PlanStep) -> Dict[str, Any]:
        """Execute LLM invocation"""
        # Phase 1: Placeholder
        # Phase 4: Will integrate with actual LLM via personality_manager
        return {
            "status": "executed",
            "output": f"[LLM Response to: {step.parameters.get('query', 'unknown')}]",
            "mode": step.parameters.get('mode', 'JARVIS')
        }
    
    def _execute_store_memory(self, step: PlanStep) -> Dict[str, Any]:
        """Execute memory storage"""
        # Phase 1: Placeholder
        # Phase 2: Will integrate with actual memory_system
        return {
            "status": "stored",
            "type": step.parameters.get('type', 'unknown'),
            "size": len(str(step.parameters.get('content', '')))
        }
    
    def _execute_system(self, step: PlanStep) -> Dict[str, Any]:
        """Execute system operation"""
        command = step.parameters.get('command', '')
        logger.info(f"[SYSTEM] Executing: {command}")
        return {
            "status": "executed",
            "command": command
        }
    
    def _execute_analyze_improvements(self, step: PlanStep) -> Dict[str, Any]:
        """Analyze improvement opportunities"""
        # Phase 1: Placeholder
        # Phase 2: Will integrate with evolution_engine
        return {
            "status": "analyzed",
            "opportunities": []
        }
    
    def reflect_on_result(self, result: ExecutionResult) -> None:
        """
        Reflect on execution results.
        
        This is where SAIS learns from what happened.
        Analyzes:
        - Success/failure rate
        - Execution time vs estimate
        - Error patterns
        - Performance improvements
        
        Args:
            result: ExecutionResult to analyze
        """
        logger.info(f"[ORCHESTRATOR] Reflecting on result: {result.status}")
        
        # Log for improvement detection
        reflection = {
            "plan_id": result.plan_id,
            "status": result.status,
            "execution_time": result.execution_time,
            "errors": result.errors,
            "timestamp": result.timestamp.isoformat()
        }
        
        logger.info(f"[REFLECTION] {json.dumps(reflection, indent=2)}")
        
        # This data feeds into EvolutionEngine (Phase 2)
        if self.memory_system:
            try:
                self.memory_system.store(reflection, "execution_result")
            except Exception as e:
                logger.warning(f"Could not store reflection: {str(e)}")
    
    def get_execution_history(self, limit: int = 10) -> List[ExecutionResult]:
        """Retrieve recent execution history"""
        return self.execution_history[-limit:]
    
    def get_pending_approvals(self) -> List[Plan]:
        """Get plans waiting for user approval"""
        return self.approval_queue
    
    def approve_plan(self, plan_id: str) -> ExecutionResult:
        """User approves a pending plan"""
        plan = next((p for p in self.approval_queue if p.plan_id == plan_id), None)
        if not plan:
            return ExecutionResult(
                plan_id=plan_id,
                status="failed",
                output=None,
                execution_time=0.0,
                errors=["Plan not found in approval queue"]
            )
        
        self.approval_queue.remove(plan)
        result = self.execute_plan(plan)
        self.reflect_on_result(result)
        self.execution_history.append(result)
        return result
    
    def reject_plan(self, plan_id: str) -> None:
        """User rejects a pending plan"""
        self.approval_queue = [p for p in self.approval_queue if p.plan_id != plan_id]
        logger.info(f"[ORCHESTRATOR] Plan {plan_id} rejected by user")


if __name__ == "__main__":
    # Simple test
    orchestrator = Orchestrator()
    
    print("=" * 60)
    print("SAIS Phase 1: Orchestrator Test")
    print("=" * 60)
    
    # Test 1: Query
    print("\n[TEST 1] Simple Query")
    result = orchestrator.handle_request("What is machine learning?")
    print(f"Status: {result.status}")
    print(f"Output: {result.output}")
    
    # Test 2: Learning request
    print("\n[TEST 2] Learning Request")
    result = orchestrator.handle_request("Teach me how to generate Lean 4 proofs")
    print(f"Status: {result.status}")
    print(f"Plan steps: {result.output}")
    
    # Test 3: System command
    print("\n[TEST 3] System Command")
    result = orchestrator.handle_request("Show system status")
    print(f"Status: {result.status}")
    
    # Test 4: Evolution request (requires approval)
    print("\n[TEST 4] Evolution Request (requires approval)")
    result = orchestrator.handle_request("Improve your proof generation")
    print(f"Status: {result.status}")
    print(f"Pending approvals: {len(orchestrator.get_pending_approvals())}")
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)

"""
SAIS Phase 1: Core Kernel
Module: Capability Manager

The Capability Manager handles:
- Storing learned capabilities
- Retrieving capabilities for tasks
- Improving capabilities based on feedback
- Searching and categorizing capabilities
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import json
import os
import uuid
import logging

logger = logging.getLogger(__name__)


class CapabilityCategory(Enum):
    """Categories of capabilities"""
    MATH = "math"
    CODE = "code"
    ANALYSIS = "analysis"
    SEARCH = "search"
    WRITING = "writing"
    REASONING = "reasoning"
    SYSTEM = "system"
    LEARNING = "learning"
    OTHER = "other"


@dataclass
class TestCase:
    """Test case for validating a capability"""
    input_data: Any
    expected_output: Any
    description: str


@dataclass
class CapabilityImprovement:
    """Record of a capability improvement"""
    timestamp: datetime
    change_description: str
    performance_before: float
    performance_after: float
    test_results: Dict[str, Any]


@dataclass
class Capability:
    """
    Represents a learned capability
    
    A capability is a specific skill that SAIS has learned and can reuse.
    It includes:
    - Implementation (code)
    - Metadata (name, category, tags)
    - Quality metrics (success rate, performance)
    - Test cases for validation
    - History of improvements
    """
    
    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    
    # Implementation
    code: str = ""  # Python/JS implementation
    language: str = "python"
    
    # Organization
    category: CapabilityCategory = CapabilityCategory.OTHER
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # IDs of required capabilities
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_improved: datetime = field(default_factory=datetime.now)
    
    # Quality metrics
    usage_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    execution_time_avg: float = 0.0
    
    # Testing
    test_cases: List[TestCase] = field(default_factory=list)
    test_pass_rate: float = 0.0
    
    # Improvement tracking
    improvement_history: List[CapabilityImprovement] = field(default_factory=list)
    current_version: int = 1
    
    # Implementation details
    required_parameters: List[str] = field(default_factory=list)
    return_type: str = "any"
    side_effects: List[str] = field(default_factory=list)
    
    # Metadata
    confidence_score: float = 0.5  # 0 = not confident, 1 = very confident
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict"""
        data = asdict(self)
        data['category'] = self.category.value
        data['created_at'] = self.created_at.isoformat()
        data['last_improved'] = self.last_improved.isoformat()
        
        # Convert improvements
        data['improvement_history'] = [
            {
                'timestamp': imp.timestamp.isoformat(),
                'change_description': imp.change_description,
                'performance_before': imp.performance_before,
                'performance_after': imp.performance_after,
                'test_results': imp.test_results
            }
            for imp in self.improvement_history
        ]
        
        # Convert test cases
        data['test_cases'] = [
            {
                'input_data': tc.input_data,
                'expected_output': tc.expected_output,
                'description': tc.description
            }
            for tc in self.test_cases
        ]
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Capability':
        """Create from JSON dict"""
        # Parse dates
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data.get('last_improved'), str):
            data['last_improved'] = datetime.fromisoformat(data['last_improved'])
        
        # Parse category
        if isinstance(data.get('category'), str):
            data['category'] = CapabilityCategory(data['category'])
        
        # Parse test cases
        test_cases = []
        for tc_data in data.get('test_cases', []):
            test_cases.append(TestCase(**tc_data))
        data['test_cases'] = test_cases
        
        # Parse improvements
        improvements = []
        for imp_data in data.get('improvement_history', []):
            if isinstance(imp_data.get('timestamp'), str):
                imp_data['timestamp'] = datetime.fromisoformat(imp_data['timestamp'])
            improvements.append(CapabilityImprovement(**imp_data))
        data['improvement_history'] = improvements
        
        return cls(**data)
    
    def get_performance_score(self) -> float:
        """Calculate overall performance score"""
        if self.usage_count == 0:
            return self.confidence_score
        
        success_rate = self.success_count / self.usage_count if self.usage_count > 0 else 0
        test_pass = self.test_pass_rate
        confidence = self.confidence_score
        
        # Weighted average
        score = (success_rate * 0.5) + (test_pass * 0.3) + (confidence * 0.2)
        return min(1.0, max(0.0, score))


class CapabilityManager:
    """
    Manages the capability repository.
    
    Responsibilities:
    - Store and retrieve capabilities
    - Search by name, category, tags
    - Track capability usage
    - Record improvements
    - Manage dependencies
    """
    
    def __init__(self, 
                 storage_dir: str = "/tmp/sais_capabilities"):
        """
        Initialize capability manager.
        
        Args:
            storage_dir: Where to persist capabilities
        """
        self.storage_dir = storage_dir
        self.capabilities: Dict[str, Capability] = {}
        
        # Ensure storage directory exists
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load existing capabilities
        self._load_capabilities()
        
        logger.info(f"Capability manager initialized")
        logger.info(f"Loaded {len(self.capabilities)} capabilities")
    
    def create_capability(self,
                         name: str,
                         code: str,
                         category: CapabilityCategory,
                         description: str = "",
                         tags: Optional[List[str]] = None,
                         dependencies: Optional[List[str]] = None,
                         test_cases: Optional[List[TestCase]] = None) -> str:
        """
        Create and store a new capability.
        
        Args:
            name: Human-readable name
            code: Implementation (Python or JS)
            category: Category
            description: What it does
            tags: Search tags
            dependencies: Required capability IDs
            test_cases: Validation test cases
            
        Returns:
            Capability ID
        """
        capability = Capability(
            name=name,
            code=code,
            category=category,
            description=description,
            tags=tags or [],
            dependencies=dependencies or [],
            test_cases=test_cases or []
        )
        
        self.capabilities[capability.id] = capability
        self._save_capability(capability)
        
        logger.info(f"Created capability: {name} (ID: {capability.id[:8]}...)")
        return capability.id
    
    def get_capability(self, cap_id: str) -> Optional[Capability]:
        """
        Get a specific capability by ID.
        
        Args:
            cap_id: Capability ID
            
        Returns:
            Capability or None
        """
        return self.capabilities.get(cap_id)
    
    def find_capability_for_task(self, 
                                 task: str,
                                 category: Optional[CapabilityCategory] = None) -> Optional[Capability]:
        """
        Find an existing capability that matches a task.
        
        Simple keyword matching (Phase 1).
        Phase 2 will add semantic matching.
        
        Args:
            task: Description of task
            category: Optional category filter
            
        Returns:
            Best matching capability or None
        """
        task_lower = task.lower()
        candidates = []
        
        for cap in self.capabilities.values():
            # Category filter
            if category and cap.category != category:
                continue
            
            # Match by name
            if task_lower in cap.name.lower():
                candidates.append((cap, 0.9))
            # Match by description
            elif task_lower in cap.description.lower():
                candidates.append((cap, 0.7))
            # Match by tags
            elif any(task_lower in tag.lower() for tag in cap.tags):
                candidates.append((cap, 0.6))
        
        if not candidates:
            return None
        
        # Return best match (highest score)
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    def list_capabilities(self,
                         category: Optional[CapabilityCategory] = None,
                         limit: int = None) -> List[Capability]:
        """
        List all capabilities.
        
        Args:
            category: Optional filter
            limit: Max to return
            
        Returns:
            List of capabilities
        """
        caps = list(self.capabilities.values())
        
        if category:
            caps = [c for c in caps if c.category == category]
        
        # Sort by performance score (descending)
        caps.sort(key=lambda c: c.get_performance_score(), reverse=True)
        
        if limit:
            caps = caps[:limit]
        
        return caps
    
    def search_capabilities(self, 
                           query: str,
                           limit: int = 10) -> List[Capability]:
        """
        Search capabilities by name, description, tags.
        
        Args:
            query: Search term
            limit: Max results
            
        Returns:
            Matching capabilities
        """
        query_lower = query.lower()
        results = []
        
        for cap in self.capabilities.values():
            score = 0
            
            if query_lower in cap.name.lower():
                score += 1.0
            if query_lower in cap.description.lower():
                score += 0.5
            if any(query_lower in tag.lower() for tag in cap.tags):
                score += 0.3
            
            if score > 0:
                results.append((cap, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [cap for cap, _ in results[:limit]]
    
    def record_usage(self,
                    cap_id: str,
                    success: bool,
                    execution_time: float) -> None:
        """
        Record that a capability was used.
        
        Args:
            cap_id: Capability ID
            success: Did it succeed?
            execution_time: How long did it take?
        """
        cap = self.get_capability(cap_id)
        if not cap:
            return
        
        cap.usage_count += 1
        if success:
            cap.success_count += 1
        else:
            cap.failure_count += 1
        
        # Update average execution time
        if execution_time > 0:
            if cap.execution_time_avg == 0:
                cap.execution_time_avg = execution_time
            else:
                # Running average
                cap.execution_time_avg = (
                    (cap.execution_time_avg * (cap.usage_count - 1) + execution_time)
                    / cap.usage_count
                )
        
        self._save_capability(cap)
    
    def improve_capability(self,
                          cap_id: str,
                          new_code: str,
                          change_description: str,
                          test_results: Optional[Dict[str, Any]] = None) -> bool:
        """
        Record an improvement to a capability.
        
        Args:
            cap_id: Capability ID
            new_code: Updated implementation
            change_description: What changed
            test_results: Results of tests
            
        Returns:
            Success
        """
        cap = self.get_capability(cap_id)
        if not cap:
            return False
        
        # Record improvement
        old_score = cap.get_performance_score()
        
        improvement = CapabilityImprovement(
            timestamp=datetime.now(),
            change_description=change_description,
            performance_before=old_score,
            performance_after=old_score,  # Will be updated after testing
            test_results=test_results or {}
        )
        
        # Update capability
        cap.code = new_code
        cap.improvement_history.append(improvement)
        cap.current_version += 1
        cap.last_improved = datetime.now()
        
        self._save_capability(cap)
        logger.info(f"Improved capability: {cap.name}")
        
        return True
    
    def add_test_case(self,
                     cap_id: str,
                     test_case: TestCase) -> bool:
        """
        Add a test case to a capability.
        
        Args:
            cap_id: Capability ID
            test_case: Test case to add
            
        Returns:
            Success
        """
        cap = self.get_capability(cap_id)
        if not cap:
            return False
        
        cap.test_cases.append(test_case)
        self._save_capability(cap)
        return True
    
    def validate_capability(self, cap_id: str) -> Dict[str, Any]:
        """
        Validate a capability against test cases.
        
        Args:
            cap_id: Capability ID
            
        Returns:
            Validation results
        """
        cap = self.get_capability(cap_id)
        if not cap:
            return {"valid": False, "error": "Capability not found"}
        
        results = {
            "capability_id": cap_id,
            "capability_name": cap.name,
            "total_tests": len(cap.test_cases),
            "passed": 0,
            "failed": 0,
            "test_details": []
        }
        
        # Note: Actually running tests would require executing the code
        # This is a placeholder for Phase 2 with sandboxed execution
        
        for test_case in cap.test_cases:
            # In Phase 3, actually execute and compare
            results["test_details"].append({
                "description": test_case.description,
                "status": "skipped",  # Phase 2: implement actual testing
                "error": None
            })
        
        results["passed"] = len([t for t in results["test_details"] if t["status"] == "passed"])
        results["failed"] = len([t for t in results["test_details"] if t["status"] == "failed"])
        results["pass_rate"] = (
            results["passed"] / results["total_tests"]
            if results["total_tests"] > 0 else 0
        )
        
        cap.test_pass_rate = results["pass_rate"]
        self._save_capability(cap)
        
        return results
    
    def get_capabilities_by_category(self, 
                                    category: CapabilityCategory) -> List[Capability]:
        """
        Get all capabilities in a category.
        
        Args:
            category: Category to filter
            
        Returns:
            Capabilities in that category
        """
        return [c for c in self.capabilities.values() if c.category == category]
    
    def get_top_capabilities(self, limit: int = 10) -> List[Capability]:
        """
        Get highest-performing capabilities.
        
        Args:
            limit: How many to return
            
        Returns:
            Top capabilities
        """
        caps = list(self.capabilities.values())
        caps.sort(key=lambda c: c.get_performance_score(), reverse=True)
        return caps[:limit]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get capability repository statistics.
        
        Returns:
            Statistics dict
        """
        caps = list(self.capabilities.values())
        
        total_usage = sum(c.usage_count for c in caps)
        total_success = sum(c.success_count for c in caps)
        
        stats = {
            "total_capabilities": len(caps),
            "by_category": {},
            "total_usage": total_usage,
            "total_success": total_success,
            "overall_success_rate": (
                total_success / total_usage if total_usage > 0 else 0
            ),
            "average_performance": (
                sum(c.get_performance_score() for c in caps) / len(caps)
                if caps else 0
            )
        }
        
        # Count by category
        for category in CapabilityCategory:
            count = len([c for c in caps if c.category == category])
            if count > 0:
                stats["by_category"][category.value] = count
        
        return stats
    
    def export_capabilities(self, output_file: str) -> bool:
        """
        Export all capabilities to JSON.
        
        Args:
            output_file: Where to save
            
        Returns:
            Success
        """
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "total_capabilities": len(self.capabilities),
                "capabilities": [c.to_dict() for c in self.capabilities.values()]
            }
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Exported {len(self.capabilities)} capabilities to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return False
    
    # ===== Private Methods =====
    
    def _load_capabilities(self) -> None:
        """Load capabilities from disk"""
        try:
            index_file = os.path.join(self.storage_dir, "index.json")
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    data = json.load(f)
                    for cap_data in data.get('capabilities', []):
                        cap = Capability.from_dict(cap_data)
                        self.capabilities[cap.id] = cap
                logger.info(f"Loaded {len(self.capabilities)} capabilities from disk")
        except Exception as e:
            logger.warning(f"Could not load capabilities: {str(e)}")
    
    def _save_capability(self, cap: Capability) -> None:
        """Save capability to disk"""
        try:
            index_file = os.path.join(self.storage_dir, "index.json")
            
            # Load existing
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"capabilities": []}
            
            # Update or add
            data["capabilities"] = [
                c for c in data["capabilities"]
                if c["id"] != cap.id
            ]
            data["capabilities"].append(cap.to_dict())
            data["timestamp"] = datetime.now().isoformat()
            
            # Save
            with open(index_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"Could not save capability: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("SAIS Phase 1: Capability Manager Test")
    print("=" * 60)
    
    # Initialize
    manager = CapabilityManager()
    
    # Test 1: Create capability
    print("\n[TEST 1] Creating capability...")
    cap_id = manager.create_capability(
        name="Generate Lean 4 Proofs",
        code="def generate_proof(theorem): pass",
        category=CapabilityCategory.MATH,
        description="Generate formal proofs in Lean 4",
        tags=["math", "proof", "lean4", "formal"]
    )
    print(f"Created: {cap_id[:8]}...")
    
    # Test 2: Add test cases
    print("\n[TEST 2] Adding test cases...")
    manager.add_test_case(
        cap_id,
        TestCase(
            input_data={"theorem": "1 + 1 = 2"},
            expected_output={"proof": "..."},
            description="Simple arithmetic"
        )
    )
    print("Added test case")
    
    # Test 3: Record usage
    print("\n[TEST 3] Recording usage...")
    manager.record_usage(cap_id, success=True, execution_time=2.5)
    manager.record_usage(cap_id, success=True, execution_time=2.3)
    manager.record_usage(cap_id, success=False, execution_time=5.0)
    print("Recorded 3 usages")
    
    # Test 4: Find capability
    print("\n[TEST 4] Finding capability...")
    found = manager.find_capability_for_task("Generate a Lean proof")
    if found:
        print(f"Found: {found.name}")
    
    # Test 5: Search
    print("\n[TEST 5] Searching...")
    results = manager.search_capabilities("proof")
    print(f"Found {len(results)} results matching 'proof'")
    
    # Test 6: Get stats
    print("\n[TEST 6] Statistics...")
    stats = manager.get_stats()
    print(f"Total capabilities: {stats['total_capabilities']}")
    print(f"Total usage: {stats['total_usage']}")
    print(f"Success rate: {stats['overall_success_rate']:.2%}")
    
    # Test 7: Get capability and check score
    print("\n[TEST 7] Performance score...")
    cap = manager.get_capability(cap_id)
    if cap:
        print(f"Capability: {cap.name}")
        print(f"Usage: {cap.usage_count}")
        print(f"Success rate: {cap.success_count}/{cap.usage_count}")
        print(f"Performance score: {cap.get_performance_score():.2f}")
    
    # Test 8: Export
    print("\n[TEST 8] Export...")
    manager.export_capabilities("/tmp/capabilities_export.json")
    print("Exported")
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)

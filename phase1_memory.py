"""
SAIS Phase 1: Core Kernel
Module: Memory System (Short-term + Long-term)

The Memory System provides:
- Session context (short-term)
- Persistent storage (long-term)
- Semantic search capabilities
- Importance-based retention
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import os
import hashlib
import logging

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Classification of memory entries"""
    CONVERSATION = "conversation"
    CAPABILITY = "capability"
    KNOWLEDGE = "knowledge"
    ERROR = "error"
    EXECUTION_RESULT = "execution_result"
    EVOLUTION_PROPOSAL = "evolution_proposal"


@dataclass
class MemoryRecord:
    """
    Single memory entry
    
    Attributes:
        id: Unique identifier
        type: Type of memory (conversation, capability, etc.)
        content: The actual content
        embedding: Vector representation for similarity search (future)
        timestamp: When this was created
        tags: Search/categorization tags
        importance: Relevance score (0.0 to 1.0)
        linked_records: IDs of related memories
        metadata: Additional context
    """
    id: str
    type: MemoryType
    content: str
    embedding: Optional[List[float]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    importance: float = 0.5
    linked_records: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict"""
        data = asdict(self)
        data['type'] = self.type.value
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryRecord':
        """Create from JSON dict"""
        data['type'] = MemoryType(data['type'])
        if isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


@dataclass
class MemoryStats:
    """Statistics about memory system"""
    total_records: int
    by_type: Dict[str, int]
    total_size_bytes: int
    oldest_record: Optional[datetime]
    newest_record: Optional[datetime]


class MemorySystem:
    """
    Dual-layer memory system for SAIS.
    
    Layer 1: Short-Term Memory
    - Holds current session context
    - Discarded at session end (or pruned)
    - Quick access
    
    Layer 2: Long-Term Memory
    - Persistent storage (JSON files)
    - Shared across sessions
    - Searchable and retrievable
    
    Both layers use the same MemoryRecord format.
    """
    
    def __init__(self, 
                 storage_dir: str = "/tmp/sais_memory",
                 max_short_term_records: int = 1000,
                 max_embedding_dim: int = 768):
        """
        Initialize memory system.
        
        Args:
            storage_dir: Where to persist long-term memory
            max_short_term_records: Max records in session
            max_embedding_dim: Dimension of embeddings (when implemented)
        """
        self.storage_dir = storage_dir
        self.max_short_term = max_short_term_records
        self.max_embedding_dim = max_embedding_dim
        
        # Ensure storage directory exists
        os.makedirs(storage_dir, exist_ok=True)
        
        # Memory layers
        self.short_term: List[MemoryRecord] = []
        self.long_term: List[MemoryRecord] = []
        
        # Index for fast lookup
        self.record_index: Dict[str, MemoryRecord] = {}
        
        # Load existing long-term memory
        self._load_long_term_memory()
        
        logger.info(f"Memory system initialized. Storage: {storage_dir}")
        logger.info(f"Loaded {len(self.long_term)} long-term records")
    
    def store(self, 
              content: Any,
              record_type: MemoryType,
              tags: Optional[List[str]] = None,
              importance: float = 0.5,
              is_persistent: bool = True) -> str:
        """
        Store a memory record.
        
        Args:
            content: What to remember
            record_type: Type of memory
            tags: Search tags
            importance: Relevance (0-1)
            is_persistent: Save to disk?
            
        Returns:
            Record ID
        """
        import uuid
        
        record_id = str(uuid.uuid4())
        
        # Convert content to string if needed
        if isinstance(content, dict) or isinstance(content, list):
            content_str = json.dumps(content)
        else:
            content_str = str(content)
        
        record = MemoryRecord(
            id=record_id,
            type=record_type,
            content=content_str,
            tags=tags or [],
            importance=importance,
            metadata={
                "content_type": type(content).__name__,
                "size_bytes": len(content_str.encode('utf-8'))
            }
        )
        
        # Add to appropriate layer
        if is_persistent:
            self.long_term.append(record)
        else:
            self.short_term.append(record)
        
        # Update index
        self.record_index[record_id] = record
        
        # Enforce short-term limit
        if len(self.short_term) > self.max_short_term:
            self._prune_short_term()
        
        # Persist if needed
        if is_persistent:
            self._save_record_to_disk(record)
        
        logger.info(f"Memory stored: {record_type.value} (ID: {record_id[:8]}...)")
        return record_id
    
    def retrieve(self, 
                 record_id: str) -> Optional[MemoryRecord]:
        """
        Retrieve a specific record by ID.
        
        Args:
            record_id: Record identifier
            
        Returns:
            MemoryRecord or None
        """
        return self.record_index.get(record_id)
    
    def search(self,
               query: str,
               record_type: Optional[MemoryType] = None,
               limit: int = 5) -> List[MemoryRecord]:
        """
        Search memory by text query.
        
        Simple keyword matching (Phase 1).
        Phase 2 will add semantic search with embeddings.
        
        Args:
            query: Search term
            record_type: Filter by type
            limit: Max results
            
        Returns:
            List of matching records
        """
        query_lower = query.lower()
        results = []
        
        all_records = self.short_term + self.long_term
        
        for record in all_records:
            # Type filter
            if record_type and record.type != record_type:
                continue
            
            # Content match
            if query_lower in record.content.lower():
                results.append(record)
            # Tag match
            elif any(query_lower in tag.lower() for tag in record.tags):
                results.append(record)
        
        # Sort by importance and recency
        results.sort(
            key=lambda r: (r.importance, r.timestamp.timestamp()),
            reverse=True
        )
        
        return results[:limit]
    
    def search_by_tag(self,
                      tag: str,
                      limit: int = 5) -> List[MemoryRecord]:
        """
        Search memory by tag.
        
        Args:
            tag: Tag to search for
            limit: Max results
            
        Returns:
            Matching records
        """
        all_records = self.short_term + self.long_term
        results = [r for r in all_records if tag in r.tags]
        
        results.sort(
            key=lambda r: (r.importance, r.timestamp.timestamp()),
            reverse=True
        )
        
        return results[:limit]
    
    def search_by_type(self,
                       record_type: MemoryType,
                       limit: int = 10) -> List[MemoryRecord]:
        """
        Get all records of a specific type.
        
        Args:
            record_type: Type to filter
            limit: Max results
            
        Returns:
            Records of that type
        """
        all_records = self.short_term + self.long_term
        results = [r for r in all_records if r.type == record_type]
        
        results.sort(
            key=lambda r: r.timestamp.timestamp(),
            reverse=True
        )
        
        return results[:limit]
    
    def get_session_context(self, 
                           max_records: int = 10,
                           importance_threshold: float = 0.3) -> str:
        """
        Get relevant context for current session.
        
        Used to provide LLM with session context.
        
        Args:
            max_records: How many to include
            importance_threshold: Minimum importance
            
        Returns:
            Formatted context string
        """
        all_records = self.short_term + self.long_term
        
        # Filter by importance and recency
        relevant = [
            r for r in all_records
            if r.importance >= importance_threshold
        ]
        
        # Sort by recency
        relevant.sort(key=lambda r: r.timestamp.timestamp(), reverse=True)
        
        # Format as context
        context_parts = []
        for record in relevant[:max_records]:
            context_parts.append(
                f"[{record.type.value}] {record.content[:200]}"
            )
        
        return "\n".join(context_parts)
    
    def get_stats(self) -> MemoryStats:
        """
        Get memory statistics.
        
        Returns:
            MemoryStats object
        """
        all_records = self.short_term + self.long_term
        
        by_type = {}
        for record in all_records:
            type_name = record.type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
        
        total_size = sum(
            record.metadata.get('size_bytes', 0)
            for record in all_records
        )
        
        timestamps = [r.timestamp for r in all_records if all_records]
        
        return MemoryStats(
            total_records=len(all_records),
            by_type=by_type,
            total_size_bytes=total_size,
            oldest_record=min(timestamps) if timestamps else None,
            newest_record=max(timestamps) if timestamps else None,
        )
    
    def link_records(self, 
                     from_id: str,
                     to_id: str) -> bool:
        """
        Create a link between two records.
        
        Args:
            from_id: Source record ID
            to_id: Target record ID
            
        Returns:
            Success
        """
        from_record = self.record_index.get(from_id)
        to_record = self.record_index.get(to_id)
        
        if not from_record or not to_record:
            return False
        
        if to_id not in from_record.linked_records:
            from_record.linked_records.append(to_id)
        
        if from_record.type in [MemoryType.KNOWLEDGE, MemoryType.CAPABILITY]:
            self._save_record_to_disk(from_record)
        
        return True
    
    def get_linked_records(self, 
                          record_id: str) -> List[MemoryRecord]:
        """
        Get all records linked to a given record.
        
        Args:
            record_id: Record to find links for
            
        Returns:
            Linked records
        """
        record = self.record_index.get(record_id)
        if not record:
            return []
        
        linked = []
        for linked_id in record.linked_records:
            linked_record = self.record_index.get(linked_id)
            if linked_record:
                linked.append(linked_record)
        
        return linked
    
    def export_memory(self, 
                      output_file: str) -> bool:
        """
        Export all long-term memory to JSON.
        
        Args:
            output_file: Where to save
            
        Returns:
            Success
        """
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "total_records": len(self.long_term),
                "records": [r.to_dict() for r in self.long_term]
            }
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Memory exported to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return False
    
    def import_memory(self, 
                      input_file: str) -> bool:
        """
        Import memory from JSON file.
        
        Args:
            input_file: Where to load from
            
        Returns:
            Success
        """
        try:
            with open(input_file, 'r') as f:
                data = json.load(f)
            
            for record_data in data.get('records', []):
                record = MemoryRecord.from_dict(record_data)
                self.long_term.append(record)
                self.record_index[record.id] = record
            
            logger.info(f"Imported {len(self.long_term)} records from {input_file}")
            return True
        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            return False
    
    # ===== Private Methods =====
    
    def _load_long_term_memory(self) -> None:
        """Load long-term memory from disk"""
        try:
            # Try to load from index file first
            index_file = os.path.join(self.storage_dir, "index.json")
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    data = json.load(f)
                    for record_data in data.get('records', []):
                        record = MemoryRecord.from_dict(record_data)
                        self.long_term.append(record)
                        self.record_index[record.id] = record
                logger.info(f"Loaded {len(self.long_term)} records from index")
        except Exception as e:
            logger.warning(f"Could not load index: {str(e)}")
    
    def _save_record_to_disk(self, record: MemoryRecord) -> None:
        """Save individual record to disk"""
        try:
            # Save to index file
            index_file = os.path.join(self.storage_dir, "index.json")
            
            # Load existing
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"records": []}
            
            # Update or add record
            data['records'] = [
                r for r in data['records']
                if r['id'] != record.id
            ]
            data['records'].append(record.to_dict())
            
            # Save
            with open(index_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"Could not save record to disk: {str(e)}")
    
    def _prune_short_term(self) -> None:
        """Remove low-importance records from short-term"""
        # Keep highest importance
        self.short_term.sort(key=lambda r: r.importance, reverse=True)
        self.short_term = self.short_term[:self.max_short_term // 2]
        logger.info("Pruned short-term memory")


if __name__ == "__main__":
    print("=" * 60)
    print("SAIS Phase 1: Memory System Test")
    print("=" * 60)
    
    # Initialize
    memory = MemorySystem()
    
    # Test 1: Store different types
    print("\n[TEST 1] Storing memories...")
    
    id1 = memory.store(
        "User asked about machine learning",
        MemoryType.CONVERSATION,
        tags=["ml", "learning"],
        importance=0.8
    )
    print(f"Stored conversation: {id1[:8]}...")
    
    id2 = memory.store(
        {"name": "ML Basics", "status": "learned"},
        MemoryType.CAPABILITY,
        tags=["ml", "basics"],
        importance=0.9
    )
    print(f"Stored capability: {id2[:8]}...")
    
    id3 = memory.store(
        "Failed to generate proof - out of memory",
        MemoryType.ERROR,
        tags=["error", "proof"],
        importance=0.7
    )
    print(f"Stored error: {id3[:8]}...")
    
    # Test 2: Retrieve
    print("\n[TEST 2] Retrieving memories...")
    record = memory.retrieve(id1)
    print(f"Retrieved: {record.content}")
    
    # Test 3: Search
    print("\n[TEST 3] Searching memories...")
    results = memory.search("learning", limit=3)
    print(f"Found {len(results)} records matching 'learning'")
    for r in results:
        print(f"  - {r.type.value}: {r.content[:50]}...")
    
    # Test 4: Search by tag
    print("\n[TEST 4] Searching by tag...")
    results = memory.search_by_tag("ml", limit=5)
    print(f"Found {len(results)} records with tag 'ml'")
    
    # Test 5: Search by type
    print("\n[TEST 5] Searching by type...")
    results = memory.search_by_type(MemoryType.ERROR)
    print(f"Found {len(results)} error records")
    
    # Test 6: Get stats
    print("\n[TEST 6] Memory statistics...")
    stats = memory.get_stats()
    print(f"Total records: {stats.total_records}")
    print(f"By type: {stats.by_type}")
    print(f"Total size: {stats.total_size_bytes} bytes")
    
    # Test 7: Link records
    print("\n[TEST 7] Linking records...")
    memory.link_records(id2, id1)
    linked = memory.get_linked_records(id2)
    print(f"Found {len(linked)} linked records")
    
    # Test 8: Session context
    print("\n[TEST 8] Session context...")
    context = memory.get_session_context(max_records=3)
    print("Session context:")
    print(context)
    
    # Test 9: Export/Import
    print("\n[TEST 9] Export/Import...")
    memory.export_memory("/tmp/memory_export.json")
    print("Exported memory")
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)

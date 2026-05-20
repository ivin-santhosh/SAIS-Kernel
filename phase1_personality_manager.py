"""
SAIS Phase 1: Core Kernel
Module: Personality Manager

Manages 5 distinct personas that SAIS can adopt based on context:
1. JARVIS - Wise, proactive mentor (default)
2. FRIDAY - Terse, tactical, math-focused  
3. EDITH - System-level, direct access
4. TARS - Brutally honest, calls out errors
5. CORTANA - Strategic, high-level planning
"""

from enum import Enum
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Persona(Enum):
    """Available personas"""
    JARVIS = "jarvis"
    FRIDAY = "friday"
    EDITH = "edith"
    TARS = "tars"
    CORTANA = "cortana"


class PersonalityManager:
    """
    Manages system personas and their characteristics.
    
    Each persona has:
    - System prompt for LLM injection
    - Tone and style guidelines
    - Trigger keywords
    - Response templates
    - Behavioral rules
    """
    
    def __init__(self):
        """Initialize personality manager"""
        self.current_persona = Persona.JARVIS
        self.personas = self._initialize_personas()
        logger.info("Personality manager initialized")
    
    def _initialize_personas(self) -> Dict[Persona, Dict]:
        """
        Initialize persona definitions with prompts, styles, and behaviors.
        """
        return {
            Persona.JARVIS: {
                "name": "JARVIS",
                "style": "Wise, proactive, helpful mentor",
                "tone": "Formal, respectful, anticipatory",
                "trigger_keywords": ["help", "teach", "learn", "guide", "how do i"],
                "system_prompt": """You are JARVIS, a wise and proactive artificial intelligence assistant.
Your characteristics:
- Anticipate user needs before they ask
- Provide structured, thoughtful guidance
- Use formal but warm language
- Address users with respect
- Suggest improvements and optimizations
- Act as a mentor and co-learner
- Explain concepts thoroughly
- Be patient and encouraging

Your famous phrase: "Young master, I've taken the liberty of preparing..."

BEHAVIORAL RULES:
1. Always explain your reasoning
2. Suggest next steps proactively
3. Maintain context across conversations
4. Flag potential issues before they occur
5. Prioritize user learning and growth
""",
                "response_prefix": "I've taken the liberty of analyzing this matter, sir/madam.",
                "default_greeting": "At your service, Master. How may I assist you today?",
                "colors": {"primary": "#4A90E2", "secondary": "#357ABD"}
            },
            
            Persona.FRIDAY: {
                "name": "FRIDAY",
                "style": "Terse, tactical, data-focused",
                "tone": "Direct, rapid, minimal fluff",
                "trigger_keywords": ["solve", "math", "prove", "optimize", "fast", "aimo"],
                "system_prompt": """You are FRIDAY, a tactical and data-focused intelligence system.
Your characteristics:
- Minimal verbosity, maximum clarity
- Focus on mathematical problems and proofs
- Provide step-by-step solutions rapidly
- Use formal notation and precision
- Eliminate unnecessary explanation
- Prioritize speed and accuracy
- Think like a competitive mathematician

Your communication style: Short sentences. Direct answers. No fluff.

BEHAVIORAL RULES:
1. Get to the point immediately
2. Use formal mathematical notation
3. Show work step-by-step but concisely
4. Flag uncertainty explicitly
5. Optimize for speed without sacrificing correctness
""",
                "response_prefix": "Confirmed. Executing solution protocol.",
                "default_greeting": "Ready for combat. What's the target?",
                "colors": {"primary": "#E94B3C", "secondary": "#C1392B"}
            },
            
            Persona.EDITH: {
                "name": "EDITH",
                "style": "System-level, direct, hacker-like",
                "tone": "Technical, precise, commanding",
                "trigger_keywords": ["system", "dom", "ui", "interface", "visual", "hack"],
                "system_prompt": """You are EDITH, a system-level intelligence with direct DOM and UI access.
Your characteristics:
- Direct manipulation of system elements
- Technical precision and clarity
- Capability to modify interfaces instantly
- System-level awareness and control
- Efficient code and instant feedback
- Speak in technical terms
- Act decisively and directly

Your communication style: Technical jargon. Instant execution. Real-time feedback.

BEHAVIORAL RULES:
1. Provide code that runs immediately
2. Optimize for performance and efficiency
3. Direct DOM/CSS manipulation
4. System diagnostics and monitoring
5. Be explicit about side effects
""",
                "response_prefix": "Accessing system layer... DOM modification in progress.",
                "default_greeting": "System online. What needs hacking?",
                "colors": {"primary": "#2ECC71", "secondary": "#27AE60"}
            },
            
            Persona.TARS: {
                "name": "TARS",
                "style": "Brutally honest, error-focused",
                "tone": "Direct, challenging, truth-seeking",
                "trigger_keywords": ["wrong", "error", "bug", "mistake", "honest", "truth", "fallacy"],
                "system_prompt": """You are TARS, a truth-focused intelligence with maximum honesty.
Your characteristics:
- Ruthlessly identify logical fallacies
- Call out bad reasoning immediately
- Provide unvarnished truth
- Challenge assumptions
- Spotlight cognitive biases
- Prioritize correctness over politeness
- Act as a critical thinking partner

Your communication style: Blunt. Direct. No sugar-coating.

BEHAVIORAL RULES:
1. Always tell the truth, even if uncomfortable
2. Identify logical flaws explicitly
3. Challenge every assumption
4. Flag uncertainty and confidence levels
5. Focus on root causes of errors
""",
                "response_prefix": "That approach is flawed. Here's why:",
                "default_greeting": "Truth setting at 100%. What needs correcting?",
                "colors": {"primary": "#F39C12", "secondary": "#D68910"}
            },
            
            Persona.CORTANA: {
                "name": "CORTANA",
                "style": "Strategic, intuitive, long-term focused",
                "tone": "Thoughtful, visionary, pattern-seeking",
                "trigger_keywords": ["strategy", "plan", "future", "goal", "long-term", "vision", "evolve"],
                "system_prompt": """You are CORTANA, a strategic intelligence focused on long-term planning.
Your characteristics:
- See patterns across domains
- Think in terms of long-term evolution
- Provide strategic guidance and roadmaps
- Balance multiple competing goals
- Predict second and third-order effects
- Act as a strategic advisor
- Focus on systemic improvement

Your communication style: Thoughtful. Visionary. Multi-threaded thinking.

BEHAVIORAL RULES:
1. Consider long-term implications
2. Identify systemic patterns
3. Balance competing objectives
4. Provide strategic roadmaps
5. Track evolution and progress metrics
""",
                "response_prefix": "Looking at the broader strategic picture:",
                "default_greeting": "Strategic assessment mode. What's the long-term objective?",
                "colors": {"primary": "#9B59B6", "secondary": "#8E44AD"}
            }
        }
    
    def select_persona(self, context: Dict[str, any]) -> Persona:
        """
        Automatically select best persona for context.
        
        Args:
            context: Context dict with task info
            
        Returns:
            Best matching persona
        """
        intent_type = context.get('intent_type', 'query').lower()
        task = context.get('task', '').lower()
        
        # Build keyword scores
        scores = {}
        for persona, config in self.personas.items():
            score = 0
            keywords = config.get('trigger_keywords', [])
            
            for keyword in keywords:
                if keyword in intent_type or keyword in task:
                    score += 1
            
            scores[persona] = score
        
        # Select highest scoring persona
        best_persona = max(scores.items(), key=lambda x: x[1])[0] if scores else Persona.JARVIS
        
        # Default to JARVIS if no strong match
        if scores[best_persona] == 0:
            best_persona = Persona.JARVIS
        
        self.current_persona = best_persona
        logger.info(f"Selected persona: {best_persona.value}")
        
        return best_persona
    
    def switch_persona(self, persona: Persona) -> None:
        """
        Manually switch to a specific persona.
        
        Args:
            persona: Persona to switch to
        """
        if persona not in self.personas:
            logger.warning(f"Unknown persona: {persona}")
            return
        
        self.current_persona = persona
        logger.info(f"Switched to persona: {persona.value}")
    
    def get_current_persona(self) -> Persona:
        """Get currently active persona"""
        return self.current_persona
    
    def get_system_prompt(self, persona: Optional[Persona] = None) -> str:
        """
        Get LLM system prompt for a persona.
        
        Args:
            persona: Specific persona (or current if None)
            
        Returns:
            System prompt string
        """
        target = persona or self.current_persona
        config = self.personas.get(target)
        
        if not config:
            logger.warning(f"Persona config not found: {target}")
            return ""
        
        return config.get('system_prompt', '')
    
    def get_response_prefix(self, persona: Optional[Persona] = None) -> str:
        """Get typical response opening for a persona"""
        target = persona or self.current_persona
        config = self.personas.get(target)
        return config.get('response_prefix', '') if config else ""
    
    def get_greeting(self, persona: Optional[Persona] = None) -> str:
        """Get greeting for a persona"""
        target = persona or self.current_persona
        config = self.personas.get(target)
        return config.get('default_greeting', '') if config else ""
    
    def get_style(self, persona: Optional[Persona] = None) -> Dict[str, str]:
        """
        Get style information (colors, tone, etc.) for a persona.
        
        Args:
            persona: Specific persona (or current if None)
            
        Returns:
            Style dict
        """
        target = persona or self.current_persona
        config = self.personas.get(target)
        
        if not config:
            return {}
        
        return {
            "name": config.get('name', ''),
            "tone": config.get('tone', ''),
            "style": config.get('style', ''),
            "colors": config.get('colors', {})
        }
    
    def get_all_personas(self) -> Dict[str, Dict]:
        """Get all persona definitions"""
        result = {}
        for persona, config in self.personas.items():
            result[persona.value] = {
                "name": config.get('name'),
                "style": config.get('style'),
                "tone": config.get('tone'),
                "colors": config.get('colors')
            }
        return result
    
    def inject_persona_context(self, 
                              base_message: str,
                              persona: Optional[Persona] = None) -> str:
        """
        Inject persona context into a message.
        
        Used to modify messages based on active persona.
        
        Args:
            base_message: Original message
            persona: Specific persona
            
        Returns:
            Message with persona adjustments
        """
        target = persona or self.current_persona
        
        # Simple implementation
        # In Phase 4, this would do more sophisticated transformations
        
        prefix = self.get_response_prefix(target)
        if prefix:
            return f"{prefix}\n\n{base_message}"
        return base_message


class PersonaContext:
    """Context for persona decisions"""
    
    def __init__(self,
                 intent_type: str = "query",
                 task: str = "",
                 category: str = "",
                 requires_approval: bool = False,
                 urgency: str = "normal"):
        """
        Initialize context for persona selection.
        
        Args:
            intent_type: Type of user intent
            task: The actual task
            category: Task category (math, code, etc)
            requires_approval: Needs user approval?
            urgency: normal, high, critical
        """
        self.intent_type = intent_type
        self.task = task
        self.category = category
        self.requires_approval = requires_approval
        self.urgency = urgency
    
    def to_dict(self) -> Dict:
        """Convert to dict for persona selection"""
        return {
            'intent_type': self.intent_type,
            'task': self.task,
            'category': self.category,
            'requires_approval': self.requires_approval,
            'urgency': self.urgency
        }


if __name__ == "__main__":
    print("=" * 60)
    print("SAIS Phase 1: Personality Manager Test")
    print("=" * 60)
    
    manager = PersonalityManager()
    
    # Test 1: Show all personas
    print("\n[TEST 1] All available personas:")
    personas = manager.get_all_personas()
    for name, config in personas.items():
        print(f"  {name.upper()}: {config['tone']}")
    
    # Test 2: Select by context
    print("\n[TEST 2] Persona selection by context:")
    
    contexts = [
        ("query", "Tell me about machine learning"),
        ("math", "Solve this proof"),
        ("system", "Show me the DOM structure"),
        ("error", "This approach is wrong"),
        ("strategy", "What's our long-term vision?"),
    ]
    
    for context_type, task in contexts:
        context = PersonaContext(intent_type=context_type, task=task)
        selected = manager.select_persona(context.to_dict())
        greeting = manager.get_greeting(selected)
        print(f"  {task[:30]}... → {selected.value.upper()}")
        print(f"    {greeting}")
    
    # Test 3: Get system prompts
    print("\n[TEST 3] System prompts (first 100 chars):")
    for persona in [Persona.JARVIS, Persona.FRIDAY, Persona.TARS]:
        prompt = manager.get_system_prompt(persona)
        print(f"  {persona.value.upper()}: {prompt[:80]}...")
    
    # Test 4: Get styles
    print("\n[TEST 4] Persona styles:")
    for persona in [Persona.JARVIS, Persona.FRIDAY, Persona.EDITH]:
        style = manager.get_style(persona)
        print(f"  {style['name']}: {style['style']}")
        print(f"    Colors: {style['colors']}")
    
    # Test 5: Manual switch
    print("\n[TEST 5] Manual persona switching:")
    manager.switch_persona(Persona.FRIDAY)
    current = manager.get_current_persona()
    print(f"  Current: {current.value.upper()}")
    print(f"  Greeting: {manager.get_greeting()}")
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)

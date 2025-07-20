class AgentCore:
    def __init__(self, memory, tools, persona_config):
        self.memory = memory  # VectorDB/LTM module
        self.tools = tools    # Plugin registry
        self.persona = persona_config  # YAML-defined behavior profile
        self.state = "idle"   # Active/Error/Processing
    
    def perceive(self, observation):
        """Process input through perception layer"""
        return self._preprocess(observation)
    
    def reason(self, context):
        """Invoke LLM with memory/tools context"""
        return self._llm_generate(context)
    
    def act(self, decision):
        """Execute tool/response action"""
        return self._execute(decision)

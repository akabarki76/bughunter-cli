# src/tools/__init__.py
TOOL_REGISTRY = {}

def register_tool(name):
    def decorator(cls):
        TOOL_REGISTRY[name] = cls
        return cls
    return decorator

class BaseTool:
    def __init__(self):
        if not self.is_installed():
            raise RuntimeError(f"{self.name} not installed")
    
    def run(self, target: str, output_file: str = None, **kwargs) -> str:
        raise NotImplementedError

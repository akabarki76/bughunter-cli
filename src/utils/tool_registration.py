from abc import ABC, abstractmethod

TOOL_REGISTRY = {}

class BaseTool(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, target: str, output_file: str = None, **kwargs):
        pass

def register_tool(name):
    def decorator(cls):
        TOOL_REGISTRY[name] = cls
        return cls
    return decorator

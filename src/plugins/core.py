# plugins/core.py
PLUGIN_REGISTRY = {}

def register_plugin(name, version, dependencies=None):
    def decorator(cls):
        PLUGIN_REGISTRY[name] = {
            "class": cls,
            "version": version,
            "dependencies": dependencies or []
        }
        print(f"Registered plugin: {name} v{version}")
        return cls
    return decorator
